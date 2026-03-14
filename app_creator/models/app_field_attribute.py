from odoo import api, fields, models

class AppFieldAttribute(models.Model):
    _name = "app.field.attribute"
    _description = "app.field.attribute"

    def _compute_name(self):
        for record in self:
            record.name = f"{record.attribute_id.name}: {record.value_selection.name if record.value_selection else record.value_char}"

    name = fields.Char(
        compute="_compute_name",
    )
    viewtype = fields.Selection(
        selection=[('form', 'Form'), ('list', 'List')],
        required=True,
        default=lambda self: self.env.context.get('default_viewtype'),
    )
    field_id = fields.Many2one(
        comodel_name="app.field",
    )
    datatype = fields.Selection(
        related="field_id.ir_model_fields_id.ttype",
    )
    attribute_id = fields.Many2one(
        comodel_name="app.attribute",
        domain="[('datatype_ids.code', 'in', [datatype])]",
    )
    value_selection = fields.Many2one(
        comodel_name="app.attribute.selection",
        domain="[('attribute_id', '=', attribute_id)]",
        string="Select",
    )
    value_char = fields.Char(
        string="Custom",
    )
