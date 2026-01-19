    @api.model
    def get_donor_name_personid_total(self, company, date_from, date_to, min_total=0):
        """
        Returns a list of dicts for partners who have a personal ID (res.partner.person_id):
        - 'donor': res.partner record
        - 'name': res.partner.name
        - 'personid': res.partner.person_id
        - 'total': sum of donations within the given date range
        """
        # 1. Get partners with a person_id
        partners = self.env['res.partner'].search([('person_id', '!=', False)])
        if not partners:
            return []

        # 2. Aggregate donations using read_group
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

        # 3. Filter by min_total and build result
        result = []
        for data in donation_data:
            total = data['amount']
            if total <= min_total:
                continue
            partner_id = data['partner_id'][0]  # (id, display_name)
            partner = self.env['res.partner'].browse(partner_id)
            result.append({
                'donor': partner,
                'name': partner.name,
                'personid': partner.person_id,
                'total': total
            })

        return result
