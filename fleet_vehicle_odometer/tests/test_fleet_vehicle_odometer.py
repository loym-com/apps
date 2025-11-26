from odoo.exceptions import UserError
from odoo.tests import TransactionCase

class TestFleetVehicleOdometer(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.VehicleBrand = cls.env["fleet.vehicle.model.brand"]
        cls.vehicle_brand = cls.VehicleBrand.create({
            "name": "Test Brand",
        })

        cls.VehicleModel = cls.env["fleet.vehicle.model"]
        cls.vehicle_model = cls.VehicleModel.create({
            "name": "Test Vehicle Model",
            "brand_id": cls.vehicle_brand.id,
        })

        cls.Vehicle = cls.env["fleet.vehicle"]
        cls.vehicle = cls.Vehicle.create({
            "name": "Test Vehicle",
            "model_id": cls.vehicle_model.id,
        })

        cls.AnalyticPlan = cls.env["account.analytic.plan"]
        cls.analytic_plan = cls.AnalyticPlan.create({
            "name": "Test Analytic Plan",
        })

        cls.Analytic = cls.env["account.analytic.account"]
        cls.aa1 = cls.Analytic.create({
            "name": "AA1",
            "plan_id": cls.analytic_plan.id,
        })
        cls.aa2 = cls.Analytic.create({
            "name": "AA2",
            "plan_id": cls.analytic_plan.id,
        })

        cls.Odometer = cls.env["fleet.vehicle.odometer"]
        cls.od1 = cls.Odometer.create({
            "vehicle_id": cls.vehicle.id,
            "value": 100,
            "date": "2025-01-01",
        })

    # ---------------------------------------------------------
    # Creation & basic compute
    # ---------------------------------------------------------

    def test_first_entry(self):
        """First record should have start=0 and distance = value."""
        self.assertEqual(self.od1.value_start, 0)
        self.assertEqual(self.od1.distance, 100)

    def test_create_next_entry(self):
        """Second odometer record should take previous value as start."""
        od2 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 150,
            "date": "2025-01-02",
        })
        self.assertEqual(od2.value_start, self.od1.value)
        self.assertEqual(od2.distance, 50)

    # ---------------------------------------------------------
    # Date validation
    # ---------------------------------------------------------

    def test_date_validation_error(self):
        """Should raise if date is older than the previous entry."""
        with self.assertRaises(UserError):
            self.Odometer.create({
                "vehicle_id": self.vehicle.id,
                "value": 150,
                "date": "2024-12-31",
            })

    # ---------------------------------------------------------
    # Missing value validation
    # ---------------------------------------------------------

    def test_missing_value_error(self):
        """Should raise if value is missing."""
        with self.assertRaises(UserError):
            self.Odometer.create({
                "vehicle_id": self.vehicle.id,
                "date": "2025-01-03",
            })

    # ---------------------------------------------------------
    # Write recomputation
    # ---------------------------------------------------------

    def test_write_recompute(self):
        od2 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 150,
            "date": "2025-01-02",
        })
        # Update od1 value
        self.od1.write({"value": 120})

        self.assertEqual(self.od1.distance, 120)
        self.assertEqual(od2.value_start, 120)
        self.assertEqual(od2.distance, 30)

    # ---------------------------------------------------------
    # Unlink recomputation
    # ---------------------------------------------------------

    def test_unlink_recompute(self):
        od2 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 150,
            "date": "2025-01-02",
        })
        od3 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 180,
            "date": "2025-01-03",
        })

        od2.unlink()

        # Now od3 should link to od1
        self.assertEqual(od3.value_start, self.od1.value)
        self.assertEqual(od3.distance, 80)

    # ---------------------------------------------------------
    # Analytic distance split
    # ---------------------------------------------------------

    def test_analytic_account_distance(self):
        od = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 200,
            "date": "2025-01-04",
            "analytic_account_ids": [(6, 0, [self.aa1.id, self.aa2.id])],
        })

        # distance = 100, count = 2 → ceil(100/2) = 50
        self.assertEqual(od.analytic_account_distance, 50)

    def test_analytic_no_accounts(self):
        od = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 220,
            "date": "2025-01-05",
        })
        self.assertEqual(od.analytic_account_distance, 0)

    # ---------------------------------------------------------
    # Prev/Next mechanics
    # ---------------------------------------------------------

    def test_prev_next_correct(self):
        od2 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 130,
            "date": "2025-01-02",
        })
        od3 = self.Odometer.create({
            "vehicle_id": self.vehicle.id,
            "value": 160,
            "date": "2025-01-03",
        })

        self.assertEqual(od2._get_prev(), self.od1)
        self.assertEqual(od2._get_next(), od3)
        self.assertEqual(self.od1._get_prev(), self.env["fleet.vehicle.odometer"])
        self.assertEqual(od3._get_next(), self.env["fleet.vehicle.odometer"])
