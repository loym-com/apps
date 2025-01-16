from odoo import api, fields, models

class ResourceGroup(models.Model):
    _name = "resource.group"
    _description = "resource.group"

    name = fields.Char()
    resource_ids = fields.One2many(
        comodel_name="resource.resource",
        inverse_name="group_id",
    )
    tag_ids = fields.Many2many(
        comodel_name="resource.group.tag",
        relation="resource_group_tag_rel",
        string="Tags",
    )
