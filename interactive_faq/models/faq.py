from odoo import models, fields, api

class FaqCategory(models.Model):
    _name = 'faq.category'
    _description = 'FAQ Category'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    icon = fields.Char('Icon Class', default='fa fa-question-circle')
    sequence = fields.Integer('Sequence', default=10)
    
class Faq(models.Model):
    _name = 'faq.faq'
    _description = 'FAQ'
    _order = 'sequence'

    name = fields.Char('Question', required=True)
    answer = fields.Html('Answer', required=True)
    category_id = fields.Many2one('faq.category', string='Category', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)