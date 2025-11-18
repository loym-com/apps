from odoo.tests.common import TransactionCase

class TestResUsersSyncFields(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a user
        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
        })

    def test_get_employee_fields_to_sync_returns_empty(self):
        fields_to_sync = self.user._get_employee_fields_to_sync()
        self.assertEqual(fields_to_sync, [],
                         "_get_employee_fields_to_sync should return an empty list")

    def test_super_method_returns_defaults(self):
        """Optional: test the original method for reference"""
        from odoo.addons.hr.models.res_users import User as OriginalResUsers
        default_fields = OriginalResUsers._get_employee_fields_to_sync(self.user)
        self.assertEqual(default_fields, ['name', 'email', 'image_1920', 'tz'],
                         "Original _get_employee_fields_to_sync should return default fields")
