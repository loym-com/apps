from odoo import api, fields, models

class SelfService(models.Model):
    _name = "self.service"
    _description = "self.service"
    _order = "date desc, create_date desc"

    @api.depends('create_date')
    def _compute_display_name(self):
        for record in self:
            record.display_name = " ".join(
                [
                    str(record.product_id.name),
                    str(record.create_date.date()),
                    str(record.user_id.name),
                ]
            )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.self_service_step:
            self.quantity = float(self.product_id.self_service_step)

    @api.depends('quantity', 'product_variant_price')
    def _compute_cost(self):
        for record in self:
            record.cost = record.quantity * record.product_variant_price

    display_name = fields.Char(compute='_compute_display_name')

    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('is_self_service', '=', True)]",
    )
    product_description_sale = fields.Text(
        related="product_id.description_sale",
        string="Description",
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        related="product_id.uom_id",
    )
    product_variant_price = fields.Float(
        related="product_id.lst_price",
        string="Unit Price",
    )
    product_self_service_step = fields.Selection(
        related="product_id.self_service_step",
    )
    quantity = fields.Float()
    cost = fields.Float(
        string="Cost",
        compute='_compute_cost',
        store=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    date = fields.Date(
        default=fields.Date.context_today,
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account"
    )
