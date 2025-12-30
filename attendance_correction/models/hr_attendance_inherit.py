# hr_attendance_inherit.py

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    @api.model

    def create(self, vals):
        """
        Overrides the create method on hr.attendance.
        Automatically creates a draft correction request when an employee checks in.
        """
        # 1. Panggil method create standar (Check In)
        attendance = super(HrAttendanceInherit, self).create(vals)
        
        # 2. Buat record Correction baru (saat Check In)
        # Pastikan hanya diproses saat Check In (check_out belum terisi)
        if attendance.check_in and not attendance.check_out:
            correction_vals = {
                'employee_id': attendance.employee_id.id,
                'date': attendance.check_in.date(),
                'check_in_original': attendance.check_in,
                'check_in_new': attendance.check_in,
                
                # PERBAIKAN PENTING: Menggunakan kode kunci Selection yang valid
                'reason': 'auto_entry', 
                
                'attendance_id': attendance.id, 
                'state': 'draft'
            }
            self.env['hr.attendance.correction'].create(correction_vals)
        
        return attendance

    def write(self, vals):
        """
        Overrides the write method on hr.attendance.
        Updates the correction request when an employee checks out.
        """
        # Panggil method write standar
        result = super(HrAttendanceInherit, self).write(vals)

        # 2. Update record Correction yang sudah ada (saat Check Out)
        if 'check_out' in vals:
            for attendance in self:
                # Cari record correction yang terhubung dengan absensi ini
                correction = self.env['hr.attendance.correction'].search([('attendance_id', '=', attendance.id)], limit=1)
                
                if correction:
                    correction.write({
                        # Update field original dan new dengan waktu Check Out
                        'check_out_original': attendance.check_out, 
                        'check_out_new': attendance.check_out,
                    })
        return result