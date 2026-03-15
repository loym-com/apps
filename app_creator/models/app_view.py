from odoo import api, fields, models
from odoo.exceptions import UserError


class AppView(models.Model):
    _name = "app.view"
    _description = "app.view"
    _order = "sequence"

    @api.depends("view_type")
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.view_type

    @api.onchange("view_type")
    def _onchange_view_type(self):
        # Auto-save to trigger recomputation of attr_ids.xml_attr_domain_ids
        self.write({'view_type': self.view_type})

    sequence = fields.Integer()
    menuitem_id = fields.Many2one(
        comodel_name="app.menuitem",
    )
    view_type = fields.Selection(
        selection=[('form', 'Form'), ('tree', 'List')],
        string="View Type",
    )
    attr_ids = fields.One2many(
        comodel_name="app.viewitem.attr",
        inverse_name="view_id",
        string="Attributes",
    )
    attr_char = fields.Char(
        string="Custom Attributes",
    )
    viewitem_ids = fields.One2many(
        comodel_name="app.viewitem",
        inverse_name="view_id",
        string="Fields/Tags",
    )

    def action_open_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'app.view',
            'view_mode': 'form',
            # 'res_id': self.env.context.get('view_id'),
            'res_id': self.id,
        }

    def action_add_viewitem(self):
        self.ensure_one()
        viewitem = self.env["app.viewitem"].create({
            "view_id": self.id,
            "sequence": max(self.viewitem_ids.mapped("sequence") or [0]) + 10,
        })
        # viewitem = viewitem.with_context(viewitem_id=viewitem.id)
        return viewitem.action_open_viewitem()
