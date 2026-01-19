from odoo import api, models
from odoo.exceptions import UserError


class DonationTaxReceipt(models.Model):
    _inherit = "donation.tax.receipt"

    @api.model
    def get_donor_name_personid_total(self, company, personid_category_code, date_from, date_to, min_total=0):
        """
        Returns a list of dicts for partners who have a personal ID:
        - 'donor': res.partner record
        - 'name': res.partner.name
        - 'personid': res.partner.id_numbers.name (single per partner)
        - 'total': sum of donations within the given date range

        Raises UserError if a partner has multiple id_numbers in the category.
        """
        # 1. Get id_numbers of the given category with non-empty names
        id_numbers = self.env['res.partner.id_number'].search(
            [
                ('category_id.code', '=', personid_category_code),
                ('name', '!=', False),
                ('name', '!=', ''),
            ]
        )

        # 2. Check for duplicates per partner
        partners = id_numbers.mapped('partner_id')
        duplicate_partners = [p for p in partners if len(id_numbers.filtered(lambda i: i.partner_id == p)) > 1]
        if duplicate_partners:
            names = ", ".join([p.name for p in duplicate_partners])
            raise UserError(f"The following partners have multiple id_numbers in category {personid_category_code}: {names}")

        if not partners:
            return []

        # 3. Aggregate donations in DB using read_group
        donation_data = self.read_group(
            domain=[
                ('company_id', 'child_of', company.id),
                ('partner_id', 'in', partners.ids),
                ('donation_date', '>=', date_from),
                ('donation_date', '<=', date_to)
            ],
            fields=['partner_id', 'amount:sum'],
            groupby=['partner_id']
        )
        donation_data = [d for d in donation_data if d['amount'] > min_total]

        # 4. Map partner_id to id_number
        partner_personid_map = {i.partner_id.id: i.name for i in id_numbers}

        # 5. Build result
        result = []
        for data in donation_data:
            partner_id = data['partner_id'][0]  # read_group returns (id, display_name)
            partner = self.env['res.partner'].browse(partner_id)
            result.append({
                'donor': partner,
                'name': partner.name,
                'personid': partner_personid_map[partner_id],
                'total': data['amount']
            })

        return result
