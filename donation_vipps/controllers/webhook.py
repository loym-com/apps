"""HTTP controller for storing Vipps webhook payloads."""

from __future__ import annotations

import json
import logging
from typing import Any

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VippsWebhookController(http.Controller):
    """Receive raw Vipps webhook requests and store them in the database."""

    def _get_remote_addr(self) -> str:
        """Return the client IP address if it is available."""

        access_route = request.httprequest.access_route
        if access_route:
            return access_route[0]
        return request.httprequest.remote_addr or ""

    def _get_headers(self) -> str:
        """Serialize request headers as pretty-printed JSON."""

        headers: dict[str, Any] = dict(request.httprequest.headers.items())
        return json.dumps(headers, indent=2, sort_keys=True, ensure_ascii=False)

    @http.route(
        "/vipps/webhook",
        auth="public",
        csrf=False,
        methods=["POST"],
        type="http",
    )
    def webhook(self, **kwargs):
        """Store the raw HTTP request and return HTTP 200."""

        payload = request.httprequest.get_data(as_text=True)
        webhook = request.env["donation.vipps.webhook"].sudo().create(
            {
                "method": request.httprequest.method,
                "path": request.httprequest.path,
                "remote_addr": self._get_remote_addr(),
                "headers": self._get_headers(),
                "payload": payload,
            }
        )
        _logger.info(
            "Stored Vipps webhook %s from %s on %s",
            webhook.display_name,
            webhook.remote_addr,
            webhook.path,
        )
        return request.make_response("", status=200)
