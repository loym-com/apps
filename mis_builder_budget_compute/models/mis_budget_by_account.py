from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MisBudgetByAccount(models.Model):
    _name = "mis.budget.by.account"
    _inherit = ["mis.budget.by.account", "base.set.record.values.mixin"]

    def action_compute_budget_items(self):
        # Compute last year's Profit/Loss * budget_percent change in each account.tag
        self.ensure_one()

        accounts = self.env["account.account"].search(
            [("internal_group", "in", ["income", "expense"])]
        )
        account_entries = self.env['account.move.line'].search(
            [
                ('date', '>=', self.date_from.replace(year=self.date_from.year-1)),
                ('date', '<=', self.date_to.replace(year=self.date_to.year-1)),
                ("account_id", "in", accounts.ids),
            ]
        )
        # Useful for _set_record_values() method in BATCH
        # budget_items = self.env["mis.budget.by.account.item"].search(
        #     [
        #         ("budget_id", "=", self.id),
        #         ("date_from", "=", self.date_from),
        #         ("date_to", "=", self.date_to),
        #     ]
        # )

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
            # TODO: Re-use the budget items domain above?
            domain = [
                ("budget_id", "=", self.id),
                ("date_from", "=", self.date_from),
                ("date_to", "=", self.date_to),
                ("account_id", "=", account.id),
            ]
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
            # TODO: Improve the _set_record_values() method, do in batch for better performance.
            self._set_record_values(
                model_name="mis.budget.by.account.item",
                domain=domain,
                values=values,
            )
            # TODO: If a draft account entry would use a new account, and later the entry is deleted,
            # there will still be a budget item with this account which is no longer relevant.

        return {
            'name': 'MIS Budget Items (by accounts)',
            'type': 'ir.actions.act_window',
            'res_model': 'mis.budget.by.account.item',
            'view_mode': 'tree',
            "domain": [["budget_id", "=", self.id]]
        }
