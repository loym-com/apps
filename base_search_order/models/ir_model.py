# from odoo import models, api


# class IrModel(models.Model):
#     _inherit = 'ir.model'

#     def write(self, vals):
#         res = super().write(vals)
#         if 'order' in vals:
#             # Clear the cached search_order for updated models
#             from .search_order import _search_order_cache
#             for model_name in self.mapped('model'):
#                 _search_order_cache.pop(model_name, None)
#         return res
