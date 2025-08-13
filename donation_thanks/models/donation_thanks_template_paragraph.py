import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DonationThanksTemplateParagraph(models.Model):
    _name = "donation.thanks.template.paragraph"
    _order = "sequence, id"

    paragraph = fields.Char()
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    template_id = fields.Many2one(
        comodel_name="donation.thanks.template",
        string="Template",
        required=True,
        ondelete="cascade",
    )
