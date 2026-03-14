from odoo import api, fields, models

class AppAttribute(models.Model):
    _name = "app.attribute"
    _description = "app.attribute"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    code = fields.Char()
    datatype_ids = fields.Many2many(
        comodel_name="app.datatype",
        relation="app_datatype_attribute_rel",
    )
    selection_ids = fields.One2many(
        comodel_name="app.attribute.selection",
        inverse_name="attribute_id",
    )
