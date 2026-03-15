from odoo import api, fields, models

class AppXmlAttrOption(models.Model):
    _name = "app.xml.attr.option"
    _description = "app.xml.attr.option"

    name = fields.Char()
    code = fields.Char()
    xml_attr_id = fields.Many2one(
        comodel_name="app.xml.attr",
    )
