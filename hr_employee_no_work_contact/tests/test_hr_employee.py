from odoo.tests.common import TransactionCase

class TestHrEmployeeSyncUser(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Contact',
            'email': 'contact@test.com',
            'mobile': '+1234567890',
        })

        # Create employee
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Employee',
            'work_contact_id': cls.partner.id,  # initial contact
        })

        # Create a user
        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
        })

    def test_sync_user_does_not_set_work_contact(self):
        # Call the method manually
        vals = self.employee._sync_user(self.user)

        # The returned dict should NOT contain work_contact_id
        self.assertNotIn('work_contact_id', vals, 
                         "_sync_user should not set work_contact_id")

    def test_sync_user_with_image_does_not_set_work_contact(self):
        vals = self.employee._sync_user(self.user, employee_has_image=True)
        self.assertNotIn('work_contact_id', vals,
                         "_sync_user with image should not set work_contact_id")
