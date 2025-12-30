from odoo import http
from odoo.http import request

class FAQ(http.Controller):
    @http.route('/faq', type='http', auth='public', website=True)
    def faq_page(self, **kw):
        categories = request.env['faq.category'].search([])
        faqs = request.env['faq.faq'].search([])
        return request.render('interactive_faq.faq_page', {
            'categories': categories,
            'faqs': faqs,
        })