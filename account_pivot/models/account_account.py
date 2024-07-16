from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    include_initial_balance = fields.Boolean(
        "Bring Accounts Balance Forward",
        related="user_type_id.include_initial_balance",
        store=False,
        readonly=True,
    )
