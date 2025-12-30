# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AttendanceCorrectionRejectWizard(models.TransientModel):
    _name = 'attendance.correction.reject.wizard'
    _description = 'Attendance Correction Rejection Reason Wizard'

    reason = fields.Text(string='Alasan Penolakan', required=True)
    correction_id = fields.Many2one('hr.attendance.correction', string='Correction Request', required=True)

    def action_reject_with_reason(self):
        self.ensure_one()
        
        # Panggil fungsi reject di model utama
        self.correction_id.action_reject(self.reason)
        
        return {'type': 'ir.actions.act_window_close'}
