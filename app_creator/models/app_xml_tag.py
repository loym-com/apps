from odoo import api, fields, models

class AppXmlTag(models.Model):
    _name = "app.xml.tag"
    _description = "app.xml.tag"

    name = fields.Char()
    code = fields.Char()
    xml_attr_ids = fields.Many2many(
        comodel_name="app.xml.attr",
        relation="app_xml_tag_attr_rel",
        column1="tag_id",
        column2="attr_id",
        string="Allowed Attributes",
    )
