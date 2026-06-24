from odoo import _, api, fields, models


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    commercial_partner_id = fields.Many2one(
        related="partner_id",
        store=False,
    )

    def _prepare_donation_move(self):
        """ Set account.move.line analytic_distribution """
        vals = super()._prepare_donation_move()
        # Keep the same line ordering as core: one product move line per non in-kind
        # and non-zero donation line, then counterpart line(s).
        donation_lines = self.line_ids.filtered(
            lambda l: not l.in_kind and not self.currency_id.is_zero(l.amount)
        )
        donation_iter = iter(donation_lines)

        for command in vals.get("line_ids", []):
            if not (isinstance(command, (list, tuple)) and len(command) == 3):
                continue
            if command[0] != 0 or not isinstance(command[2], dict):
                continue

            line_vals = command[2]
            if line_vals.get("display_type") != "product":
                continue

            donation_line = next(donation_iter, False)
            analytic_account = donation_line and getattr(
                donation_line, "analytic_account_id", False
            )
            if analytic_account:
                line_vals["analytic_distribution"] = {str(analytic_account.id): 100.0}

        return vals
