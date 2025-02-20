from odoo import api, fields, models


class Contact(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(
        selection=[('person', 'Individual or family'), ('company', 'Company')],
    )

    def _get_contact_name(self, partner, name):
        if partner.parent_id.is_company:
            return super()._get_contact_name(partner, name)
        else:
            return name
