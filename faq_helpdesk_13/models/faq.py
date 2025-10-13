from odoo import models, fields

class FAQ(models.Model):
    _name = 'faq'
    _description = 'Frequently Asked Questions'

    name = fields.Char(string='Question', required=True)
    answer = fields.Text(string='Answer')
    category = fields.Char(string='Category')
    sub_category = fields.Char(string='Sub Category')
    count = fields.Integer(string=' Count',)
    helpdesk_ticket_ids = fields.Many2many(
        'dym.helpdesk.ticket',
        'faq_helpdesk_ticket_rel',
        'faq_id',
        'ticket_id',
        string='Related Tickets'
    )
    
    is_published = fields.Boolean(string='Published on Website', default=True)
    rating = fields.Float(string='Average Rating', compute='_compute_rating', store=True)
    rating_count = fields.Integer(string='Rating Count', compute='_compute_rating', store=True)

    def _compute_rating(self):
        for faq in self:
            ratings = self.env['faq.rating'].search([('faq_id', '=', faq.id)])
            faq.rating_count = len(ratings)
            faq.rating = sum(r.value for r in ratings) / len(ratings) if ratings else 0.0

class FAQRating(models.Model):
    _name = 'faq.rating'
    _description = 'FAQ Rating'

    faq_id = fields.Many2one('faq', string='FAQ', required=True)
    value = fields.Integer(string='Rating (1–5)', required=True)
