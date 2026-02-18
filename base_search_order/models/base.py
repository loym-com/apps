from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    # Plan A: Change search order per model.

    def _setup_complete(self):
        super()._setup_complete()
        model = self.env['ir.model']._get(self._name)
        if model and model._fields.get('order_custom') and model.order_custom:
            type(self)._order = model.order_custom  
        # if model:
        #     if model._fields.get('order_custom'):
        #         if model.order_custom:
        #             type(self)._order = model.order_custom  

    # Plan B: Use XML field context to change the search order.

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        ctx_order = self.env.context.get(f"{self._name} order")
        if ctx_order:
            order = ctx_order
        return super(Base, self)._search(domain, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
