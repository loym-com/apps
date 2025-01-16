from odoo import fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    # This field is used in _search_resource_group_tag_ids()
    combination_ids = fields.Many2many(
        comodel_name="resource.booking.combination",
        # resource_booking_combination_resource_resource_rel
    )
