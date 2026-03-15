from odoo import api, fields, models


class AppViewitem(models.Model):
    _name = "app.viewitem"
    _description = "app.viewitem"
    _order = "sequence"

    
    @api.model
    def _get_xml_tag_domain(self):
        id = self.env.context.get("active_id")
        self = self.browse(id) if id else self
        if self.menuitem_id:
            return [('code', 'in', ("form", "tree", "kanban"))]
        elif self.parent_id:
            parent_tag = self.parent_id.xml_tag_id
            if parent_tag.code == "form":
                return [('code', 'in', ("group", "field", "notebook", "page"))]
            elif parent_tag.code == "tree":
                return [('code', 'in', ("field",))]
            elif parent_tag.code == "kanban":
                return [('code', 'in', ("field",))]
        else:
            return []

    xml_tag_id = fields.Many2one(
        comodel_name="app.xml.tag",
        string="Name",
        domain=_get_xml_tag_domain,
        required=True,
    )
    display_name = fields.Char(
        related="xml_tag_id.name",
    )
    sequence = fields.Integer()
    ir_model_fields_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
    )
    # viewtype = fields.Selection(
    #     selection=[('form', 'Form'), ('list', 'List')],
    #     required=True,
    # )
    viewitem_attr_ids = fields.One2many(
        comodel_name="app.viewitem.attr",
        inverse_name="viewitem_id",
    )
    viewitem_attr_char = fields.Char(
        string="Custom Attributes",
    )
    # menuitem_id or parent_id should be set, but not both
    menuitem_id = fields.Many2one(
        comodel_name="app.menuitem",
    )
    parent_id = fields.Many2one(
        comodel_name="app.viewitem",
    )
    child_ids = fields.One2many(
        comodel_name="app.viewitem",
        inverse_name="parent_id",
    )

    def action_open_viewitem(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'app.viewitem',
            'view_mode': 'form',
            'res_id': self.id,
        }