"""Model used to store raw Vipps webhook requests."""

from __future__ import annotations

from odoo import fields, models


class DonationVippsWebhook(models.Model):
    """Persist the webhook request exactly as it was received."""

    _name = "donation.vipps.webhook"
    _description = "Vipps Webhook"
    _order = "received_at desc"

    name = fields.Char(default=lambda self: self._default_name())
    received_at = fields.Datetime(default=fields.Datetime.now)
    method = fields.Char()
    path = fields.Char()
    remote_addr = fields.Char()
    headers = fields.Text()
    payload = fields.Text()
    processed = fields.Boolean(default=False)
    processing_error = fields.Text()

    def _default_name(self) -> str:
        """Generate a readable name for the stored webhook."""

        return f"Webhook {fields.Datetime.to_string(fields.Datetime.now())}"
