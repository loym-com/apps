from odoo import api, fields, models

class ResourceGroupTag(models.Model):
    _name = "resource.group.tag"
    _description = "resource.group.tag"

    name = fields.Char()
    group_ids = fields.Many2many(
        comodel_name="resource.group",
        relation="resource_group_tag_rel",
        string="Groups",
    )
