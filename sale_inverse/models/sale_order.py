from dateutil.relativedelta import relativedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_status = fields.Selection(inverse="_inverse_invoice_status")

    def _inverse_invoice_status(self):
        for record in self:
            record.invoice_status = record.invoice_status
