# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPartnerContactId(TransactionCase):
    def setUp(self):
        super().setUp()
        self.testpartner = self.env["res.partner"].create(
            {"name": "test", "is_driver": True}
        )

    def test_partner_contact_id(self):
        self.assertEqual(self.testpartner.is_driver, True)
