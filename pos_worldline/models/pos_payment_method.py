import json
import logging
import os
import requests
# import signal # TODO: Set timeout and error messages, e.g. in _check_worldline()
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request

# from odoo.addons.hw_drivers.iot_handlers.drivers.PrinterDriver import PrinterController

_logger = logging.getLogger(__name__)

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    worldline_host = fields.Char(help="Format: https://host:port")
    worldline_key = fields.Char()

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
            host = field("worldline_host")
            key = field("worldline_key")
            if not (host and key):
                raise UserError("Worldline host or key is missing.")
            # The next line will raise an error if the connection is wrong.
            response = self._worldline_do_request("GET", "/api/v1/DeviceInformation", None, host, key)

    def worldline_do_payment(self, payment):
        self.ensure_one()
        # client_id = payment["customData"]["client_id"]

        # """ Test 3.7 No Connection """
        # response = self._worldline_do_request("GET", "/api/v1/Payments/latest", None, client_id, ignore=[404])

        # if response.status not in [200, 404]:
        #     return {
        #         'status_code': response.status,
        #         'message': response.reason,
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
                'status_code': response.status,
                'message': response.reason,
            }
        else:
            return json.loads(response.data)

    def _worldline_do_request(self, method, url, body, host=None, key=None):
        """ Test 3.4 Communication Log """
        self._create_log(
            {
                "url": url,
                "direction": "request",
                "host": request.httprequest.environ["HTTP_HOST"],
                # "client_id": client_id,
                "log_json": body,
            }
        )

        body_json= json.dumps(body)
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'Integration-Key': key or self.worldline_key,
            'User-Agent' : 'Odoo 14.0',
            'Content-Length': str(len(body_json))
        }
        dir_name = os.path.dirname(__file__)
        cert_relative_path = "ECR-REST.crt"
        cert_absolute_path = os.path.join(dir_name, cert_relative_path)

        pool = urllib3.HTTPSConnectionPool(
            host or self.worldline_host,
            assert_hostname=False, # Setting assert_hostname to False disables the hostname verification because URL will not match certificate.
            ca_certs=cert_absolute_path,
        )
        response = pool.urlopen(
            method=method,
            url=url,
            body=body_json,
            headers=headers,
        )
        """ Test 3.4 Communication Log """
        response_json = {}
        if response.data:
            response_json = json.loads(response.data)
        if response_json.get("transactionOutcome"):
            status = response_json["transactionOutcome"]
        else:
            status = "{} {}".format(response.status, response.reason)

        values = {
            "url": url,
            "direction": "response",
            "host": self.worldline_host,
            # "client_id": client_id,
            "status": status,
            "log_json": response_json,
        }
        if url in ("/api/v1/Payments", "/api/v1/Payments/latest"):
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
