import logging

from collections import defaultdict
from itertools import groupby

from odoo import Command, fields, models

_logger = logging.getLogger(__name__)


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    thanks_id = fields.Many2one(
        string="Thanks",
        comodel_name="donation.thanks",
        readonly=True,
    )

    def action_create_thanks(self):
        thanks_ids = []
        thanks_donations = defaultdict(self.env["donation.donation"].browse)
        # Odoo 17
        # grouped_donations = self.grouped(lambda d: (d.partner_id, d.thanks_template_id))
        # for (partner, template), donations in grouped_donations.items():
        # Odoo 16
        grouped_donations = self.read_group(
            [("id", "in", self.ids)],
            ["partner_id", "thanks_template_id"],
            ["partner_id", "thanks_template_id"],
            lazy=False,
        )
        for group in grouped_donations:
            partner = self.env["res.partner"].browse(group["partner_id"][0])
            template = self.env["donation.thanks.template"]
            if group.get("thanks_template_id"):
                template = template.browse(group["thanks_template_id"][0])
            donations = self.search(group["__domain"])
            # End Odoo 16
            # Create a new thanks record for each combination of (parent) partner and thanks template
            if partner.parent_id:
                partner = partner.parent_id
            thanks_donations[(partner.id, template.id)] |= donations
        for (partner_id, template_id), donations in thanks_donations.items():
            thanks = self.env["donation.thanks"].create({
                "partner_id": partner_id,
                "thanks_template_id": template_id,
                "donation_ids": [
                    Command.set(donations.sorted(key="donation_date", reverse=True).ids)
                ],
            })
            thanks_ids.append(thanks.id)

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "donation_thanks.donation_thanks_action"
        )
        action["domain"] = [("id", "in", thanks_ids)]
        return action
