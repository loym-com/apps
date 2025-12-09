from odoo.tests.common import TransactionCase
from unittest.mock import patch


class TestHrEmployeeNoSync(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create partner/contact
        cls.partner = cls.env['res.partner'].create({
            'name': 'Contact',
            'email': 'contact@test.com',
            'mobile': '+1234567890',
        })

        # Create employee with linked partner
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Employee',
            'work_contact_id': cls.partner.id,
        })

    # ---------------------------------------------------------
    # No propagation employee -> partner
    # ---------------------------------------------------------
    def test_employee_updates_do_not_change_partner(self):
        self.employee.work_email = "employee@test.com"
        self.employee.mobile_phone = "+4711111111"

        self.assertEqual(self.partner.email, "contact@test.com")
        self.assertEqual(self.partner.mobile, "+1234567890")

    # ---------------------------------------------------------
    # No propagation partner -> employee
    # ---------------------------------------------------------
    def test_partner_updates_do_not_change_employee(self):
        self.partner.write({
            'email': 'changed_partner@test.com',
            'mobile': '+4722222222',
        })

        self.assertNotEqual(
            self.employee.work_email,
            self.partner.email,
            "Partner email propagated to employee"
        )
        self.assertNotEqual(
            self.employee.mobile_phone,
            self.partner.mobile,
            "Partner mobile propagated to employee"
        )

    # ---------------------------------------------------------
    # Compute must never run
    # ---------------------------------------------------------
    def test_compute_not_called(self):
        with patch(
            "odoo.addons.hr.models.hr_employee_base.HrEmployeeBase._compute_work_contact_details"
        ) as mocked_compute:

            self.partner.write({'email': 'compute_trigger@test.com'})
            self.env.flush_all()

            mocked_compute.assert_not_called()

    # ---------------------------------------------------------
    # Inverse must never run
    # ---------------------------------------------------------
    def test_inverse_not_called(self):
        with patch(
            "odoo.addons.hr.models.hr_employee_base.HrEmployeeBase._inverse_work_contact_details"
        ) as mocked_inverse:

            self.employee.write({'work_email': 'inverse_trigger@test.com'})
            mocked_inverse.assert_not_called()
