from odoo import api, fields, models

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    group_id = fields.Many2one(
        comodel_name="resource.group",
        string="Group",
    )
    group_tag_ids = fields.Many2many(
        comodel_name="resource.group.tag",
        related="group_id.tag_ids",
        string="Tags",
    )
