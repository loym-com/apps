import json

from datetime import date, datetime

from odoo.addons.base_sparse_field.models import fields

#
# Definition and implementation of serialized fields: override
#

def convert_to_cache(self, value, record, validate=True):
    # cache format: dict / list
    if value is False or value is None:
        value = {}
    if isinstance(value, (dict, list)):
        # Format date / datetime
        if isinstance(value, (dict)):
            for key, val in value.items():
                if isinstance(val, (date, datetime)):
                    value[key] = val.strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps(value)
    else:
        return (value or None)


fields.Serialized.convert_to_cache = convert_to_cache
