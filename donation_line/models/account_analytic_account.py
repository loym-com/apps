import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    donation_description = fields.Char("Donation Description", translate=True)
