from odoo import api, fields, models

class AppField(models.Model):
    _name = "app.field"
    _description = "app.field"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    menuitem_id = fields.Many2one(
        comodel_name="app.menuitem",
    )
    ir_model_id = fields.Many2one(
        'ir.model', 
        string="Model",
        related='menuitem_id.ir_model_id',
    )
    ir_model_fields_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
    )
    attribute_ids = fields.One2many(
        comodel_name="app.field.attribute",
        inverse_name="field_id",
    )
