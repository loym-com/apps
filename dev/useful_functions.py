from odoo import models

def get(self, field, vals={}):
    """Get value of field from vals or self"""
    if vals.get(field):
        return vals[field]
    else:
        value = getattr(self, field)
        if isinstance(value, models.Model):
            return value.id
        else:
            return value
