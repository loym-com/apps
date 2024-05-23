import datetime
import json
import time

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.http import request

# Inspired by https://developer.samport.com/integration-guidelines/logging-page/
class PosPaymentLog(models.Model):
    _name = "pos.payment.terminal.log"
    _description = "Log for POS payment requests"
    _order = "create_date desc"

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    url = fields.Char()
    direction = fields.Selection(
        selection=[("request", "Request"), ("response", "Response")],
    )
    host = fields.Char()
    status = fields.Char()
    client_id = fields.Char()
    receipt_no = fields.Char("Receipt No.")
    receipt_total = fields.Float()
    log = fields.Text()
