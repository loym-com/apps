from odoo import fields, models


class PosPaymentLog(models.Model):
    _name = "pos.payment.terminal.log"
    _description = "Log for POS payment requests"
    # https://developer.samport.com/integration-guidelines/logging-page/

    description = fields.Char()
    log = fields.Char()
