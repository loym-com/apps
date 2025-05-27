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