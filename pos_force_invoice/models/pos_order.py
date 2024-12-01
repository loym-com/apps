from odoo import api, fields, models, tools, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["to_invoice"] = True
        return super().create(vals_list)
