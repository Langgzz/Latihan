{
    'name': 'FAQ Helpdesk',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'Convert Helpdesk tickets to FAQs and rate solutions',
    'author': 'Muhamad & Copilot',
    'license': 'AGPL-3',
    'depends': ['website', 'dym_helpdesk_mgmt'],
    'data': [
        'security/ir.model.access.csv',
        'views/faq_views.xml',
        'views/helpdesk_views.xml',
        'views/website_templates.xml',
        'data/faq_demo.xml',
    ],
    'installable': True,
    'application': True,
}
