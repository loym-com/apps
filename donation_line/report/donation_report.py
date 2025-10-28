from psycopg2 import sql

from odoo import api, fields, models, tools


class DonationReport(models.Model):
    _inherit = "donation.report"

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        "Analytic Account",
        readonly=True,
    )

    def _select(self):
        return sql.SQL(
            """
            SELECT min(l.id) AS id,
                d.donation_date,
                l.product_id,
                l.analytic_account_id, -- NEW
                l.in_kind,
                l.tax_receipt_ok,
                l.product_detailed_type,
                pt.categ_id AS product_categ_id,
                d.company_id,
                d.payment_mode_id,
                d.partner_id,
                d.country_id,
                d.campaign_id,
                d.company_currency_id,
                d.thanks_printed,
                d.thanks_template_id,
                sum(l.amount_company_currency) AS amount_company_currency,
                sum(l.tax_receipt_amount) AS tax_receipt_amount
                """
        )

    def _group_by(self):
        return sql.SQL(
            """
            GROUP BY l.product_id,
                l.analytic_account_id, -- NEW
                l.in_kind,
                l.tax_receipt_ok,
                pt.categ_id,
                d.donation_date,
                d.partner_id,
                d.country_id,
                d.campaign_id,
                d.company_id,
                d.payment_mode_id,
                d.thanks_printed,
                d.thanks_template_id,
                d.company_currency_id
            """
        )

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        query = sql.SQL("CREATE OR REPLACE VIEW {0} AS ({1} FROM {2} {3} {4})").format(
            sql.Identifier(self._table),
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
        )  # pylint: disable=sql-injection
        self._cr.execute(query)
