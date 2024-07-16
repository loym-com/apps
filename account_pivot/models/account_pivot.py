from odoo import api, fields, models, tools


class AccountPivot(models.Model):
    _name = "account.pivot"
    _description = "Account Pivot"
    _auto = False

    @api.model
    def _compute_analytic_domain(self):
        if self.env.user.has_group("account.group_account_manager"):
            return []
        else:
            return [("user_id", "=", self.env.user.id)]

    account_id = fields.Many2one("account.account", string="Account", store=True)
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        store=True,
        domain=_compute_analytic_domain,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        store=True,
        index=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one("res.currency", string="Currency", store=True)
    date = fields.Date(string="Date", store=True)
    journal_id = fields.Many2one("account.journal", string="Journal", store=True)
    move_id = fields.Many2one("account.move", string="Journal Entry", store=True)
    name = fields.Char(string="Name", store=True)
    parent_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Parent Status',
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", store=True)
    product_id = fields.Many2one("product.product", string="Product", store=True)
    user_type_id = fields.Many2one(
        "account.account.type", string="Account Type", store=True
    )

    analytic_group_id = fields.Many2one(
        "account.analytic.group", string="Analytic Group", store=True
    )
    include_initial_balance = fields.Boolean(
        "Bring Accounts Balance Forward", store=True
    )

    day = fields.Integer("Day", store=True)
    week = fields.Integer("Week", store=True)
    month = fields.Integer("Month", store=True)
    quarter = fields.Integer("Quarter", store=True)
    year = fields.Integer("Year", store=True)

    balance = fields.Monetary("Acc+Bud(raw)", store=True)
    balance2 = fields.Monetary("Acc+Bud", store=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, "account_pivot")
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW account_pivot AS
             SELECT t0.id AS id,
                t0.account_id,
                t0.analytic_account_id,
                t0.balance,
                -t0.balance AS balance2,
                t0.company_id,
                t0.currency_id,
                t0.date,
                date_part('day', t0.date) AS day,
                date_part('week', t0.date) AS week,
                date_part('month', t0.date) AS month,
                date_part('quarter', t0.date) AS quarter,
                date_part('year', t0.date) AS year,
                t0.journal_id,
                t0.move_id,
                t0.name,
                t0.parent_state,
                t0.partner_id,
                t0.product_id,
                t1.user_type_id AS user_type_id,
                t2.include_initial_balance AS include_initial_balance,
                t3.group_id AS analytic_group_id
               FROM account_move_line t0
                LEFT JOIN account_account t1 ON t0.account_id = t1.id
                LEFT JOIN account_account_type t2 ON t1.user_type_id = t2.id
                LEFT JOIN account_analytic_account t3 ON t0.analytic_account_id = t3.id
                LEFT JOIN account_move t4 ON t0.move_id = t4.id
               WHERE t4.state in ('draft', 'posted')
            """
        )
