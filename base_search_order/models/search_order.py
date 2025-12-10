from odoo import api, models

import logging
_logger = logging.getLogger(__name__)

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

# ---------------------------
# Patch BaseModel.search
# ---------------------------

_original_search = models.Model.search

def patched_search(self, domain, offset=0, limit=None, order=None, count=False):
    if not order:
        order = _get_model_search_order(self.env, self._name)
    return _original_search(self, domain, offset=offset, limit=limit, order=order, count=count)

models.Model.search = patched_search

# ---------------------------
# Patch BaseModel.name_search
# ---------------------------

_original_name_search = models.Model.name_search

@api.model
def patched_name_search(self, name='', args=None, operator='ilike', limit=100):
    ids = self._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=None)
    domain = [('id', 'in', ids)]
    recs = patched_search(self, domain)
    return recs.name_get()

models.Model.name_search = patched_name_search

# -----------------------
# Patch BaseModel._search
# -----------------------

_original__search = models.Model._search

@api.model
def patched__search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    """
    Inject the model-level order into context if `order` is not explicitly set.
    This affects _name_search(), search(), and all downstream calls.
    """
    if not order:
        # get default order from ir.model
        order = _get_model_search_order(self.env, self._name)

    # call original
    return _original__search(
        self,
        domain,
        offset=offset,
        limit=limit,
        order=order,
        count=count,
        access_rights_uid=access_rights_uid,
    )

# Apply patch
models.Model._search = patched__search
