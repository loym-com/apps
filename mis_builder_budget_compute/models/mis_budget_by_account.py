from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MisBudgetByAccount(models.Model):
    _inherit = "mis.budget.by.account"

    def action_compute_budget_items(self):
        # Compute last year's Profit/Loss * budget_percent change in each account.tag
        self.ensure_one()
        if self.item_ids:
            raise UserError("Cannot compute budget items: items already exist.")

        accounts = self.env["account.account"].search(
            [("internal_group", "in", ["income", "expense"])]
        )
        account_entries = self.env['account.move.line'].search([
            ('date', '>=', self.date_from.replace(year=self.date_from.year-1)),
            ('date', '<=', self.date_to.replace(year=self.date_to.year-1)),
            ("account_id", "in", accounts.ids),
        ])

        account_totals = {}
        for entry in account_entries:
            account = entry.account_id
            amount = entry.balance
            if account in account_totals:
                account_totals[account] += amount
            else:
                account_totals[account] = amount

        values_list = []
        for account, total in account_totals.items():
            for tag in account.tag_ids:
                total *= (1.0 + tag.budget_percent)
            values = {
                "budget_id": self.id,
                "name": "",
                "account_id": account.id,
                "date_range_id": self.date_range_id,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "balance": total,
                # analytic_account_id,
                # analytic_tag_ids,
            }
            values_list.append(values)

        self.item_ids.create(values_list)
        return {
            'name': 'MIS Budget Items (by accounts)',
            'type': 'ir.actions.act_window',
            'res_model': 'mis.budget.by.account.item',
            'view_mode': 'tree',
            "domain": [["budget_id", "=", self.id]]
        }
