# -*- coding: utf-8 -*-
from odoo import models, fields

class AttendanceCorrectionLog(models.Model):
    _name = 'attendance.correction.log'
    _description = 'Attendance Correction Audit Log'
    _order = 'change_date desc'

    correction_id = fields.Many2one('hr.attendance.correction', string='Correction Ref', ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    
    check_in_before = fields.Datetime(string='Check In (Before)')
    check_out_before = fields.Datetime(string='Check Out (Before)')
    
    check_in_after = fields.Datetime(string='Check In (After)')
    check_out_after = fields.Datetime(string='Check Out (After)')
    
    changed_by = fields.Many2one('res.users', string='Changed By')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)