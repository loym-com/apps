from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MisBudgetByAccount(models.Model):
    _name = "mis.budget.by.account"
    _inherit = ["mis.budget.by.account", "base.set.record.values.mixin"]

    compute_date_ranges = fields.Many2many("date.range", string="Compute Ranges")

    def action_compute_budget_items(self):
        # Compute last year's Profit/Loss * budget_percent change in each account.tag
        self.ensure_one()

        accounts = self.env["account.account"].search(
            [("internal_group", "in", ["income", "expense"])]
        )
        for range in self.compute_date_ranges:
            account_entries = self.env['account.move.line'].search(
                [
                    ('date', '>=', range.date_start.replace(year=self.date_from.year-1)),
                    ('date', '<=', range.date_end.replace(year=self.date_to.year-1)),
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
                # Multiplication based on account tags
                for tag in account.tag_ids:
                    percent = tag.budget_input_ids.filtered(lambda i: i.date_range_id == range).budget_percent
                    total *= (1.0 + percent)
                # TODO: Re-use the budget items domain above?
                domain = [
                    ("budget_id", "=", self.id),
                    ("computed", "=", True),
                    ("date_from", "=", range.date_start),
                    ("date_to", "=", range.date_end),
                    ("account_id", "=", account.id),
                ]
                values = {
                    "budget_id": self.id,
                    "computed": True,
                    "name": "",
                    "account_id": account.id,
                    "date_range_id": range.id,
                    "date_from": range.date_start,
                    "date_to": range.date_end,
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
