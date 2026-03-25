from odoo import api, fields, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    blocked = fields.Boolean(string='Blocked')
    note = fields.Text(string='Note')

    @api.constrains('blocked', 'active')
    def _check_blocked_active(self):
        for record in self:
            if record.blocked and record.active:
                raise models.ValidationError(f"'{record.display_name}' is blocked and cannot be active.")
