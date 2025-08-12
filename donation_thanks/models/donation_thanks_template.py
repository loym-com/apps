import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DonationThanksTemplate(models.Model):
    _inherit = "donation.thanks.template"

    model = fields.Selection(
        string="Model",
        selection=[
            ("donation.donation", "Donation"),
            ("donation.thanks", "Donation Thanks"),
            ("donation.tax.receipt", "Donation Tax Receipt"),
        ]
    )
    attachment_ids = fields.One2many(
        string="Attachments",
        comodel_name="ir.attachment",
        inverse_name="res_id",
        context={"default_res_model": "donation.thanks.template"},
    )
    img_text = fields.Text(
        string="Image Text",
        translate=True,
    )

    def action_goto_report_donation_thanks(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Donation Thanks Report",
            "res_model": "ir.actions.report",
            "view_mode": "form",
            "res_id": self.env.ref(
                "donation_thanks.action_report_donation_thanks"
            ).id,
        }

    def action_goto_report_donation_tax_receipt(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Donation Tax Receipt Report",
            "res_model": "ir.actions.report",
            "view_mode": "form",
            "res_id": self.env.ref(
                "donation_thanks.action_report_donation_tax_receipt"
            ).id,
        }

    # DEPRECATED
    image_height = fields.Integer("Image Height")
    image_width = fields.Integer("Image Width")
    image_text = fields.Html(
        sanitize=False, # Gives the best UI for translation
        translate=True,
    )
    text1 = fields.Html(
        sanitize=False, # Gives the best UI for translation
        translate=True,
    )
    text2 = fields.Html(
        sanitize=False, # Gives the best UI for translation
        translate=True,
    )