from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResourceGroup(models.Model):
    _inherit = "resource.group"

    @api.model
    def _teamm2odoo_name(self):
        """ Look for record name beginning with teamm name """
        name = self._teamm2odoo_get_value("resource.group")
        record = self.search([("name", "=like", f"{name}%")])
        if not len(record):
            return name
        elif len(record) == 1:
            return record.name
        else:
            raise ValidationError(f"Multiple names begins with {name}: {record}")
