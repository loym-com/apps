from odoo import api, fields, models, tools, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        """ Avoid the error "You need to add a line before posting. """
        account = self.env['account.account'].search([], limit=1)
        for move in self:
            if not move.line_ids.filtered(lambda line: line.display_type not in ('line_section', 'line_note')):
                move.line_ids.create({
                    'move_id': move.id,
                    'name': 'Auto-generated line',
                    'account_id': account.id,
                    'debit': 0.0,
                    'credit': 0.0,
                })
        return super()._post(soft=soft)
