from odoo import models, fields


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    partner_id = fields.Many2one(
        "res.partner",
        domain="[]",
    )
