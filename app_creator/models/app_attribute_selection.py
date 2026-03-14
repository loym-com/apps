from odoo import api, fields, models

class AppAttributeSelection(models.Model):
    _name = "app.attribute.selection"
    _description = "app.attribute.selection"

    name = fields.Char()
    code = fields.Char()
    attribute_id = fields.Many2one(
        comodel_name="app.attribute",
    )
