# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    @api.depends('work_contact_id', 'work_contact_id.mobile', 'work_contact_id.email')
    def _compute_work_contact_details(self):
        pass

    def _inverse_work_contact_details(self):
        pass
