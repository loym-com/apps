from odoo import api, fields, models

class AppXmlAttr(models.Model):
    _name = "app.xml.attr"
    _description = "app.xml.attr"

    name = fields.Char()
    code = fields.Char()
    xml_tag_ids = fields.Many2many(
        comodel_name="app.xml.tag",
        relation="app_xml_tag_attr_rel",
        column1="attr_id",
        column2="tag_id",
        string="Used By Tags",
    )
    datatype_ids = fields.Many2many(
        comodel_name="app.datatype",
        relation="app_datatype_attr_rel",
    )
    option_ids = fields.One2many(
        comodel_name="app.xml.attr.option",
        inverse_name="xml_attr_id",
    )
