import json
import logging
import os
# import signal # TODO: Set timeout and error messages, e.g. in _check_worldline()
import ssl
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request

# from odoo.addons.hw_drivers.iot_handlers.drivers.PrinterDriver import PrinterController

_logger = logging.getLogger(__name__)

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    worldline_host_internal = fields.Char(
        string="Terminal host",
        help=(
            "URL for the terminal from the local network.\n"
            "Format: host"
        ),
    )
    worldline_host_port_external = fields.Char(
        string="External host:port",
        help=(
            "URL for the terminal from the internet, via a local service.\n"
            "If empty, run Odoo in the local network.\n"
            "Format: host:port"
        )
    )
    worldline_key = fields.Char(default="853919076C353385", help="Key for FIQ as")

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [("worldline", "Worldline")]

    @api.model
    def create(self, vals_list):
        if type(vals_list) is dict:
            vals_list = [vals_list]
        for values in vals_list:
            self._check_worldline(values)
        return super().create(vals_list)

    def write(self, values):
        for record in self:
            record._check_worldline(values)
        return super().write(values)

    def _check_worldline(self, values):
        """
        Do not save a worldline payment method if the connection fails!
        If the user will start a pos session, and the connection fails:
        - The user cannot close the session.
        - The user cannot fix the worldline payment method.
        """
        def field(field_name):
            # Create / Write: Get the updated field value (what it will be after saving).
            if field_name in values:
                return values[field_name]
            else:
                return getattr(self, field_name)
        if field("use_payment_terminal") == "worldline":
            internal = field("worldline_host_internal")
            external = field("worldline_host_port_external")
            key = field("worldline_key")
            if not (internal and key):
                raise UserError("Worldline key or internal url is missing.")
            # The next line will raise an error if the connection is wrong.
            response = self._worldline_do_request(
                "GET", "/api/v1/DeviceInformation", {}, key, internal, external
            )

    def worldline_do_payment(self, payment):
        self.ensure_one()
        # client_id = payment["customData"]["client_id"]

        # """ Test 3.7 No Connection """
        # response = self._worldline_do_request("GET", "/api/v1/Payments/latest", {}, client_id, ignore=[404])

        # if response.status not in [200, 404]:
        #     return {
        #         "status_code": response.status,
        #         "message": response.reason,
        #     }

        # # DO PAYMENT? OR IS PAYMENT ALREADY DONE?
        # if response.status == 404:
        #     # 404: /Payments/latest not found; first payment since "Dagsavslutt"
        #     do_payment = True
        # else:
        #     response_dict = json.loads(response.data)
        #     log_exists = bool(
        #         self.env["pos.payment.terminal.log"].search_count(
        #             [
        #                 ("url", "in", ["/api/v1/Payments", "/api/v1/Payments/latest"]),
        #                 # ("client_id", "!=", payment["customData"]["client_id"]),
        #                 ("receipt_no", "=", response_dict["receiptNumber"]),
        #             ]
        #         )
        #     )
        #     do_payment = log_exists # No payment happened during a loss of connection.
        # if do_payment:

        response = self._worldline_do_request("POST", "/api/v1/Payments", payment)
        if response.status not in [200, 404]:
            return {
                "status_code": response.status,
                "message": response.reason,
            }
        else:
            return json.loads(response.data)

    def _worldline_do_request(
            self, method, path, body={}, key=None, internal_host=None, external_host_port=None
        ):
        """ Test 3.4 Communication Log """
        self._create_log(
            {
                "url": path,
                "direction": "request",
                "host": request.httprequest.environ["HTTP_HOST"],
                # "client_id": client_id,
                "log_json": body,
            }
        )

        # REQUEST VARIABLES
        if external_host_port:
            host, port = external_host_port.split(":")
            port = int(port)
            body["internal_host"] = internal_host
            cert_file = False
            cert_reqs=ssl.CERT_NONE
        else:
            host = internal_host
            port = 443
            cert_file = os.path.join(
                os.path.dirname(__file__),
                "ECR-REST.crt",
            )
            cert_reqs=ssl.CERT_REQUIRED
        body_json= json.dumps(body)
        headers = {
            "content-type": "application/json; charset=utf-8",
            "Integration-Key": key or self.worldline_key,
            "User-Agent" : "Odoo 16.0",
            "Content-Length": str(len(body_json))
        }

        ####################### Also in app.py ##############################
        # REQUEST
        # The request needs to use IP address + "ECR-REST.crt".
        # urllib3: 2 args: assert_hostname & ca_certs
        # requests: 1 arg: verify (cannot verify cert only, without hostname)
        pool = urllib3.HTTPSConnectionPool(
            host,
            port=port,
            assert_hostname=False,
            ca_certs=cert_file,
            cert_reqs=cert_reqs,
        )
        response = pool.urlopen(
            method=method,
            url=f"https://{host}:{port}{path}",
            body=body_json,
            headers=headers,
        )
        #####################################################################

        """ Test 3.4 Communication Log """
        response_json = {}
        if response.data:
            # data like "<html>Not found</html>" cannot load
            response_json = json.loads(response.data)
        if response_json.get("transactionOutcome"):
            status = response_json["transactionOutcome"]
        else:
            status = "{} {}".format(response.status, response.reason)

        values = {
            "url": path,
            "direction": "response",
            "host": host,
            # "client_id": client_id,
            "status": status,
            "log_json": response_json,
        }
        if path in ("/api/v1/Payments", "/api/v1/Payments/latest"):
            _json = response_json
            if _json:
                if _json.get("receiptNumber"):
                    values["receipt_no"] = _json["receiptNumber"]
                if _json.get("amounts") and _json["amounts"].get("total"):
                    values["receipt_total"] = _json["amounts"]["total"]
        self._create_log(values)

        return response

    def _create_log(self, values):
        values["log"] = json.dumps(values.pop("log_json"), indent=4)
        record = self.env["pos.payment.terminal.log"].create(values)
        # The log is important, so save it immediately
        self.env.cr.commit()
        return record
