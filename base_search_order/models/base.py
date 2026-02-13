from odoo import models


class Base(models.AbstractModel):
    _inherit = "base"

    def _setup_complete(self):
        super()._setup_complete()
        model = self.env['ir.model']._get(self._name)
        if model and model._fields.get('order_custom') and model.order_custom:
            type(self)._order = model.order_custom  
        # if model:
        #     if model._fields.get('order_custom'):
        #         if model.order_custom:
        #             type(self)._order = model.order_custom  
