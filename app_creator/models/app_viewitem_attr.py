from odoo import api, fields, models

class AppViewitemAttr(models.Model):
    _name = "app.viewitem.attr"
    _description = "app.viewitem.attr"

    def _compute_name(self):
        for record in self:
            record.name = f"{record.attribute_id.name}: {record.value_selection.name if record.value_selection else record.value_char}"

    def _get_attr_domain(self):
        for r in self:
            if r.datatype:
                # Field attributes
                ids = self.env['app.xml.attr'].search([('datatype_ids', 'in', r.datatype)]).ids
                return [("id", "in", ids or [])]
            elif r.tag_code:
                # Tag attributes
                ids = self.env['app.xml.attr'].search([('xml_tag_ids.code', 'in', r.tag_code)]).ids
                return [("id", "in", ids or [])]
            else:
                return [("id", "in", [])]

    name = fields.Char(
        compute="_compute_name",
    )
    viewitem_id = fields.Many2one(
        comodel_name="app.viewitem",
    )
    tag_code = fields.Char(
        related="viewitem_id.xml_tag_id.code",
    )
    datatype = fields.Selection(
        related="viewitem_id.ir_model_fields_id.ttype",
    )
    xml_attr_id = fields.Many2one(
        comodel_name="app.xml.attr",
        domain=lambda self: self._get_attr_domain(),
    )
    value_option = fields.Many2one(
        comodel_name="app.xml.attr.option",
        domain="[('xml_attr_id', '=', xml_attr_id)]",
        string="Select",
    )
    value_char = fields.Char(
        string="Custom",
    )
