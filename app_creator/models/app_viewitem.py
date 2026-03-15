from odoo import api, fields, models
from odoo.exceptions import UserError


class AppViewitem(models.Model):
    _name = "app.viewitem"
    _description = "app.viewitem"
    _order = "sequence"

    @api.onchange("parent_id")
    def _default_view_id(self):
        for record in self:
            record.view_id = record.parent_id.view_id if record.parent_id else record.view_id

    @api.onchange("xml_tag_id", "ir_model_fields_id")
    def _onchange_xml_tag_id(self):
        # Auto-save to trigger recomputation of attr_ids.xml_attr_domain_ids
        self.write(
            {
                'xml_tag_id': self.xml_tag_id,
                'ir_model_fields_id': self.ir_model_fields_id,
            }
        )

    @api.depends("view_id", "view_id.view_type")
    def _compute_xml_tag_domain_ids(self):
        for rec in self:
            if rec.view_id:
                view_type = rec.view_id.view_type
            elif rec.parent_id and rec.parent_id.view_id:
                view_type = rec.parent_id.view_id.view_type

            if view_type == "form":
                domain = [('code', 'in', ("group", "field", "notebook", "page"))]
            elif view_type == "tree":
                domain = [('code', 'in', ("field",))]
            elif view_type == "kanban":
                domain = [('code', 'in', ("field",))]
            else:
                domain = []
            rec.xml_tag_domain_ids = self.env["app.xml.tag"].search(domain).ids

    xml_tag_id = fields.Many2one(
        comodel_name="app.xml.tag",
        string="Name",
    )
    xml_tag_domain_ids = fields.Many2many(
        comodel_name="app.xml.tag",
        compute="_compute_xml_tag_domain_ids",
    )
    display_name = fields.Char(
        related="xml_tag_id.name",
    )
    sequence = fields.Integer()
    ir_model_id = fields.Many2one(
        'ir.model', 
        string="Model",
        related='view_id.menuitem_id.ir_model_id',
    )
    ir_model_fields_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
    )
    view_type = fields.Selection(
        related="view_id.view_type",
    )
    attr_ids = fields.One2many(
        comodel_name="app.viewitem.attr",
        inverse_name="viewitem_id",
    )
    attr_text = fields.Text(
        string="Custom Attributes",
    )
    view_id = fields.Many2one(
        comodel_name="app.view",
    )
    parent_id = fields.Many2one(
        comodel_name="app.viewitem",
    )
    child_ids = fields.One2many(
        comodel_name="app.viewitem",
        inverse_name="parent_id",
        string="Fields/Tags",
    )
    child_text = fields.Text(
        string="Custom XML",
    )

    def action_open_viewitem(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'app.viewitem',
            'view_mode': 'form',
            # 'res_id': self.env.context.get('res_id'),
            "res_id": self.id,
        }
