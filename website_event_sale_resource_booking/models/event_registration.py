from odoo import fields,models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _get_website_registration_allowed_fields(self):
        allowed_fields = super()._get_website_registration_allowed_fields()
        return allowed_fields | {"product_id", "resource_booking_combination_id"}
