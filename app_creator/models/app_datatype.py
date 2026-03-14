from odoo import api, fields, models

class AppDatatype(models.Model):
    _name = "app.datatype"
    _description = "app.datatype"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    code = fields.Char()
    attribute_ids = fields.Many2many(
        comodel_name="app.attribute",
        relation="app_datatype_attribute_rel",
    )
