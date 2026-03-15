from odoo import api, fields, models

class AppDatatype(models.Model):
    _name = "app.datatype"
    _description = "app.datatype"

    name = fields.Char()
    code = fields.Char()
    xml_attr_ids = fields.Many2many(
        comodel_name="app.xml.attr",
        relation="app_datatype_attr_rel",
    )
