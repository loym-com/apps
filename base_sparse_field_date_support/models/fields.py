import json

from datetime import date, datetime

from odoo.addons.base_sparse_field.models import fields

#
# Definition and implementation of serialized fields: override
#


def convert_to_cache(self, value, record, validate=True):
    # cache format: date / datetime
    if value is False or value is None:
        value = {}
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return (value or None)


fields.Serialized.convert_to_cache = convert_to_cache

# # HENRIK

# @monkey_patch(fields.Field)
# def _inverse_sparse(self, records):
#     for record in records:
#         values = record[self.sparse]
#         value = self.convert_to_read(record[self.name], record, use_name_get=False)
#         if value:
#             ##########################################################
#             from datetime import date, datetime
#             if isinstance(value, date) or isinstance(value, datetime):
#                 value = value.strftime('%Y-%m-%d %H:%M:%S')
#             ##########################################################
#             if values.get(self.name) != value:
#                 values[self.name] = value
#                 record[self.sparse] = values
#         else:
#             if self.name in values:
#                 values.pop(self.name)
#                 record[self.sparse] = values
