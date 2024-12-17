from odoo import api, fields, models, SUPERUSER_ID


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    split_transactions = fields.Boolean(default=True)

    @api.constrains("split_transactions")
    def _split_transactions(self):
        for record in self:
            if record.split_transactions == False:
                record.split_transactions = True
