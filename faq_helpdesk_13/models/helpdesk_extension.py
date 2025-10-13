from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'dym.helpdesk.ticket'

    faq_ids = fields.Many2many(
        'faq',
        'faq_helpdesk_ticket_rel',
        'ticket_id',
        'faq_id',
        string='Related FAQs'
    )

    def action_convert_to_faq(self):
        for ticket in self:
            faq = self.env['faq'].create({
                'name': ticket.name,
                'answer': ticket.description,
                'category': ticket.team_id.name if ticket.team_id else 'General',
                'helpdesk_ticket_ids': [(6, 0, [ticket.id])],
                'is_published': False,
            })
            ticket.faq_ids = [(4, faq.id)]
