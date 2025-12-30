# -*- coding: utf-8 -*-
{
    'name': 'Attendance Correction Request',
    'version': '13.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage employee attendance correction requests',
    'description': """
        Allow employees to request attendance corrections.
        Includes approval workflow and audit trails.
    """,
    'author': 'YourName',
    'depends': ['base', 'hr', 'hr_attendance', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/attendance_correction_views.xml',
        #'views/correction_security_views.xml',
        'views/rejection_reason_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}