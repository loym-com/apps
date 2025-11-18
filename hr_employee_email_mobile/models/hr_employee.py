from odoo import api, fields, models


class HrEmployee(models.AbstractModel):
    _inherit = "hr.employee"

    def _sync_user(self, user, employee_has_image=False):
        """ Don't set a work contact."""
        vals = super()._sync_user(user, employee_has_image)
        vals.pop('work_contact_id', None)
        return vals
