from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_employee_fields_to_sync(self):
        """Get values to sync to the related employee when the User is changed.
        """
        return []
