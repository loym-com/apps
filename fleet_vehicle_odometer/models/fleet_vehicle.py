from odoo import _, api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    def action_register_odometer(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "fleet.fleet_vehicle_odometer_action"
        )
        action["views"] = [
            [self.env.ref("fleet_vehicle_odometer.fleet_vehicle_odometer_view_form_create").id, "form"]
        ]
        action["context"] = {
            "default_vehicle_id": self.id,
            "default_driver_id": self.env.user.partner_id.id
        }
        return action
