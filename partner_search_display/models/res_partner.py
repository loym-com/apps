# Copyright 2026 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        result = super().name_search(name=name, args=args, operator=operator, limit=limit)
        # Fetch all partner records for the IDs in the result
        partner_ids = [res[0] for res in result]
        partners_sudo = self.browse(partner_ids).sudo() # to read employee_count

        # Modify the text representation based on employee and partner_share fields
        updated_result = []
        for p_sudo in partners_sudo:
            text_repr = result[partner_ids.index(p_sudo.id)][1]
            if p_sudo.employees_count:
                text_repr = f"{_('(Employee) ')} {text_repr}"
            elif not p_sudo.partner_share:
                text_repr = f"{_('(User) ')} {text_repr}"
            updated_result.append((p_sudo.id, text_repr))

        return updated_result
