from odoo import api, models

# Cache for search_order values
_search_order_cache = {}

def _get_model_search_order(env, model_name):
    """Fetch search_order from ir.model, with cache, skip ir.model itself"""
    if model_name == "ir.model":
        return None
    if model_name not in _search_order_cache:
        ir_model = env['ir.model'].sudo().search([('model', '=', model_name)], limit=1)
        if ir_model and ir_model.order:
            _search_order_cache[model_name] = ir_model.order
        else:
            _search_order_cache[model_name] = None
    return _search_order_cache[model_name]

# def clear_search_order_cache(model_names=None):
#     """Clear cache manually, optionally for specific models"""
#     global _search_order_cache
#     if model_names:
#         for model_name in model_names:
#             _search_order_cache.pop(model_name, None)
#     else:
#         _search_order_cache = {}

# ---------------------------
# Patch BaseModel.search
# ---------------------------

_original_search = models.Model.search

def patched_search(self, domain, offset=0, limit=None, order=None, count=False):
    if order is None:
        order = _get_model_search_order(self.env, self._name)
    return _original_search(self, domain, offset=offset, limit=limit, order=order, count=count)

models.Model.search = patched_search

# ---------------------------
# Patch BaseModel.name_search
# ---------------------------

_original_name_search = models.Model.name_search

@api.model
def patched_name_search(self, name='', args=None, operator='ilike', limit=100):
    # args = args or []
    # # name_search internally calls search(), which is now patched
    # return _original_name_search(self, name=name, args=args, operator=operator, limit=limit)

    ids = self._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=None)
    domain = [('id', 'in', ids)]
    recs = patched_search(self, domain)
    return recs.name_get()

models.Model.name_search = patched_name_search
