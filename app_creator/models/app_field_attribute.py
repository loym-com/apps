from odoo import api, fields, models

class AppFieldAttribute(models.Model):
    _name = "app.field.attribute"
    _description = "app.field.attribute"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    view = fields.Selection(
        selection=[('form', 'Form'), ('list', 'List')],
    )
    field_id = fields.Many2one(
        comodel_name="app.field",
    )
    attribute_id = fields.Many2one(
        comodel_name="app.attribute",
    )
    value_char = fields.Char(
    )
