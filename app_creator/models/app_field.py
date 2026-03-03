from odoo import api, fields, models

class AppField(models.Model):
    _name = "app.field"
    _description = "app.field"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence"

    def _compute_name(self):
        for record in self:
            record.name = record.ir_model_fields_id.display_name if record.ir_model_fields_id else ""

    name = fields.Char(
        compute="_compute_name",
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
    sequence = fields.Integer(default=10)
