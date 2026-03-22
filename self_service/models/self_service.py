from odoo import api, fields, models

class SelfService(models.Model):
    _name = "self.service"
    _description = "self.service"

    @api.depends('create_date')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.create_date

    @api.depends('quantity', 'product_list_price')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.product_list_price

    display_name = fields.Datetime(compute='_compute_display_name')

    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('is_self_service', '=', True)]",
    )
    product_description_sale = fields.Text(
        related="product_id.description_sale",
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        related="product_id.uom_id",
    )
    product_list_price = fields.Float(
        related="product_id.list_price",
    )
    quantity = fields.Integer()
    total = fields.Float(compute='_compute_total', store=True)

    user_id = fields.Many2one(
        comodel_name="res.users",
    )
    date = fields.Date()
