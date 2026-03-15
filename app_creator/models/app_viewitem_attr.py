from odoo import api, fields, models

class AppViewitemAttr(models.Model):
    _name = "app.viewitem.attr"
    _description = "app.viewitem.attr"

    def _compute_name(self):
        for record in self:
            record.name = f"{record.attribute_id.name}: {record.value_selection.name if record.value_selection else record.value_char}"

    @api.depends("view_id", "view_id.view_type", "viewitem_id", "viewitem_id.xml_tag_id.code", "viewitem_id.ir_model_fields_id.ttype")
    def _compute_xml_attr_domain_ids(self):
        # view_id = self.env.context.get("view_id")
        # view = self.env["app.view"].browse(view_id)
        # viewitem_id = self.env.context.get("viewitem_id")
        # viewitem = self.env["app.viewitem"].browse(viewitem_id)
        for rec in self:
            view = rec.view_id
            viewitem = rec.viewitem_id
            if viewitem and viewitem.ir_model_fields_id.ttype:
                # Field attributes
                domain = [('datatype_ids', '=', viewitem.ir_model_fields_id.ttype)]
            elif viewitem and viewitem.xml_tag_id and viewitem.xml_tag_id.code:
                # Viewitem tag attributes
                domain = [('xml_tag_ids.code', '=', viewitem.xml_tag_id.code)]
            elif view and view.view_type:
                # View tag attributes
                domain = [('xml_tag_ids.code', '=', view.view_type)]
            else:
                domain = []
            rec.xml_attr_domain_ids = self.env["app.xml.attr"].search(domain).ids
        # return [("id", "in", ids)]

    name = fields.Char(
        compute="_compute_name",
    )
    view_id = fields.Many2one(
        comodel_name="app.view",
    )
    view_type = fields.Selection(
        related="view_id.view_type",
    )
    viewitem_id = fields.Many2one(
        comodel_name="app.viewitem",
    )
    viewitem_tag_code = fields.Char(
        related="viewitem_id.xml_tag_id.code",
    )
    datatype = fields.Selection(
        related="viewitem_id.ir_model_fields_id.ttype",
    )
    xml_attr_id = fields.Many2one(
        comodel_name="app.xml.attr",
    )
    xml_attr_domain_ids = fields.Many2many(
        comodel_name="app.xml.attr",
        compute="_compute_xml_attr_domain_ids",
    )
    value_option = fields.Many2one(
        comodel_name="app.xml.attr.option",
        domain="[('xml_attr_id', '=', xml_attr_id)]",
        string="Select",
    )
    value_char = fields.Char(
        string="Custom",
    )
