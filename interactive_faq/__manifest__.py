{
    'name': 'Interactive FAQ',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'Interactive FAQ module with search functionality',
    'description': """
        This module adds an interactive FAQ section with:
        * Searchable questions and answers
        * Category filtering
        * Interactive UI with expandable answers
    """,
    'author': 'Langgzz',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/faq_views.xml',
        'views/faq_templates.xml',
    ],
    'qweb': [],
    'assets': {
        'web.assets_frontend': [
            '/interactive_faq/static/src/css/faq.css',
            '/interactive_faq/static/src/js/faq.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}