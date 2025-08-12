import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _prepare_donation_context(self):
        context = super()._prepare_donation_context()
        # FIXME (test, and see donation_line)
        context["default_line_ids"][0][2]["analytic_account_id"] = False
        context["default_line_ids"][0][2]["description"] = False
        return context
