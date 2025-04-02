from datetime import date

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_print_donation_thanks(self):
        today = date.today()
        langs = self.env["res.lang"].search([])
        today_langs = {lang.code: today.strftime(lang.date_format) for lang in langs}
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': 'donation_thanks.report_donation_donation',
            'report_file': 'donation_thanks.report_donation_donation',
            'paperformat_id': self.env.ref('donation_thanks.paperformat_a5').id,
            'context': {'today': today_langs},
        }
