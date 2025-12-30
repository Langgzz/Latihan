# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class HrAttendanceCorrection(models.Model):
    _name = 'hr.attendance.correction'
    _description = 'Attendance Correction Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    attendance_id = fields.Many2one('hr.attendance', string='Original Attendance Record', copy=False)
    
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, default=lambda self: self.env.user.employee_id, readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', store=True)
    
    date = fields.Date(string='Correction Date', required=True, default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    
    # Original Data (Readonly)
    check_in_original = fields.Datetime(string='Original Check In', readonly=True)
    check_out_original = fields.Datetime(string='Original Check Out', readonly=True)
    
    # New Data (Correction)
    check_in_new = fields.Datetime(string='New Check In', readonly=True, states={'draft': [('readonly', False)]})
    check_out_new = fields.Datetime(string='New Check Out', readonly=True, states={'draft': [('readonly', False)]})
    
    # Reason (Selection)
    reason = fields.Selection([
        ('auto_entry', '  '),
        ('forgot_record', 'Lupa Melakukan Absensi'),
        ('system_device_error', 'Kendala Teknis Pada Sistem Atau Perangkat'),
        ('failed_location_capture', 'Terjadi Error Pada GPS '),
    ], string='Reason', required=True, readonly=True, states={'draft': [('readonly', False)]}, tracking=True)
    
    # === FIELD UNTUK 2 TAHAP APPROVAL ===
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('atasan_approved', 'Atasan Approved'), # Level 1
        ('approved', 'Approved'),         # Level 2 (Final)
        ('rejected', 'Rejected')
    ], string='Status', default='draft', track_visibility='onchange')
    
    # Level 1 Approver: Atasan
    atasan_approver_id = fields.Many2one('res.users', string='Atasan Approved By', readonly=True, copy=False)
    atasan_approval_date = fields.Datetime(string='Atasan Approval Date', readonly=True, copy=False)

    # Level 2 Approver: HRD (Final)
    hrd_approver_id = fields.Many2one('res.users', string='HRD Approved By', readonly=True, copy=False)
    hrd_approval_date = fields.Datetime(string='HRD Approval Date', readonly=True, copy=False)

    # === PERBAIKAN: MENAMBAHKAN KEMBALI FIELD ATTACHMENT ===
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', readonly=True, states={'draft': [('readonly', False)]})
    
    # Relasi ke Log
    log_ids = fields.One2many('attendance.correction.log', 'correction_id', string='Audit Logs', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.attendance.correction') or _('New')
        return super(HrAttendanceCorrection, self).create(vals)

    @api.onchange('employee_id', 'date')
    def _onchange_employee_date(self):
        """ Otomatis cari data absensi yang sudah ada """
        if self.employee_id and self.date:
            attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', self.employee_id.id),
                ('check_in', '>=', self.date),
                ('check_in', '<', fields.Date.add(self.date, days=1))
            ], limit=1)
            
            if attendance:
                self.check_in_original = attendance.check_in
                self.check_out_original = attendance.check_out
            else:
                self.check_in_original = False
                self.check_out_original = False

    def action_submit(self):
        for rec in self:
            if rec.state != 'draft':
                continue
            
            vals = {'state': 'submitted'}
            
            # Penomoran otomatis jika masih 'New'
            if rec.name == _('New') or not rec.name:
                vals['name'] = self.env['ir.sequence'].next_by_code('hr.attendance.correction') or _('New')
            # Simpan perubahan state (akan memicu akses kontrol normal)
            rec.write(vals)

    def action_atasan_approve(self):
        """ Fungsi untuk Persetujuan Level 1 (Atasan) """
        # Menggunakan ID Grup Kustom yang sudah Anda buat
        if not self.env.user.has_group('attendance_correction.group_atasan_approver'):
            raise UserError(_("Anda tidak memiliki hak untuk menyetujui di tahap Atasan."))

        for rec in self:
            if rec.state != 'submitted':
                raise UserError(_("Permintaan harus berstatus Submitted untuk disetujui Atasan."))
                
            rec.write({
                'state': 'atasan_approved',
                'atasan_approver_id': self.env.user.id,
                'atasan_approval_date': fields.Datetime.now()
            })

    def action_hrd_approve(self):
        """ Fungsi untuk Persetujuan Level 2 (HRD) & Update Absensi Final """
        for rec in self:
            if rec.state != 'atasan_approved':
                raise UserError(_("Permintaan harus berstatus Atasan Approved untuk disetujui HRD."))

            # Cek dan tutup attendance record lama yang belum ada check_out
            old_open_attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_out', '=', False)
            ], limit=1)
            
            if old_open_attendance:
                # Tutup record lama dengan check_in + 8 jam (standar workday)
                close_time = old_open_attendance.check_in + timedelta(hours=8)
                old_open_attendance.write({'check_out': close_time})

            attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_in', '>=', rec.date),
                ('check_in', '<', fields.Date.add(rec.date, days=1))
            ], limit=1)

            # Siapkan values untuk update/create
            vals = {
                'employee_id': rec.employee_id.id,
                'check_in': rec.check_in_new,
            }
            
            # Hanya tambah check_out jika ada nilai
            if rec.check_out_new:
                vals['check_out'] = rec.check_out_new
            elif attendance and attendance.check_out:
                # Pertahankan check_out lama jika ada
                vals['check_out'] = attendance.check_out

            if attendance:
                old_in = attendance.check_in
                old_out = attendance.check_out
                # Jika check_out ada dan berada sebelum check_in, anggap itu keesokan harinya
                if vals.get('check_out') and vals.get('check_out') < vals.get('check_in'):
                    vals['check_out'] = vals['check_out'] + timedelta(days=1)

                attendance.write(vals)
            else:
                old_in = False
                old_out = False
                # Adjust overnight check_out as well when creating a new attendance
                if vals.get('check_out') and vals.get('check_out') < vals.get('check_in'):
                    vals['check_out'] = vals['check_out'] + timedelta(days=1)

                self.env['hr.attendance'].create(vals)

            self.env['attendance.correction.log'].create({
                'correction_id': rec.id,
                'employee_id': rec.employee_id.id,
                'check_in_before': old_in or rec.check_in_original, 
                'check_out_before': old_out or rec.check_out_original,
                'check_in_after': rec.check_in_new,
                'check_out_after': rec.check_out_new,
                'changed_by': self.env.user.id,
                'change_date': fields.Datetime.now(),
            })

            rec.write({
                'state': 'approved',
                'hrd_approver_id': self.env.user.id,
                'hrd_approval_date': fields.Datetime.now()
            })

    def action_reject(self, reason=False):
        for rec in self:
            if not reason:
                # Open the wizard if no reason is provided
                return {
                    'name': _('Tolak Permintaan Koreksi'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'attendance.correction.reject.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_correction_id': rec.id},
                }
            
            # If reason is provided (from wizard), proceed with rejection
            rec.state = 'rejected'
            rec.message_post(body=_('Permintaan ditolak. Alasan: %s') % reason)

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'