import json
import logging
import os
import requests
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError, Warning
from odoo.http import request

# from odoo.addons.hw_drivers.iot_handlers.drivers.PrinterDriver import PrinterController

_logger = logging.getLogger(__name__)

STATUS = {
    400: "Bad request. Please check your Worldline credentials.",
    401: "Authentication failed. Please check your Worldline credentials.",
    # """ Test 3.5 Terminal Busy """
    503: "The terminal was busy and did not process your request. Please try again.",
}

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
        def field(field_name, value=None):
            # Create / Write: Get the value after saving.
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
            response = self._worldline_do_request("GET", "/api/v1/DeviceInformation", None, None, host, key)

    def worldline_do_payment(self, payment):
        self.ensure_one()
        client_id = payment["customData"]["client_id"]

        """ Test 3.7 No Connection """
        response = self._worldline_do_request("GET", "/api/v1/Payments/latest", None, client_id, ignore=[404])
        if response.data:
            response_json = json.loads(response.data)

        # do_payment ?
        if response.status == 404:
            # First payment since "Dagsavslutt"
            do_payment = True
        else:
            log_exists = bool(
                self.env["pos.payment.terminal.log"].search_count(
                    [
                        ("url", "in", ["/api/v1/Payments", "/api/v1/Payments/latest"]),
                        ("status", "=", "Approved"),
                        ("client_id", "!=", payment["customData"]["client_id"]),
                        ("receipt_no", "=", response_json["receiptNumber"]),
                    ]
                )
            )
            do_payment = log_exists # No payment happened during a loss of connection.
        if do_payment:
            response = self._worldline_do_request("POST", "/api/v1/Payments", payment, client_id)
            response_json = json.loads(response.data)

        # ### TEST
        # response_json = {
        #     "transactionOutcome": "Approved",
        #     "receipt": {
        #         "customer": {
        #             "plain": '\tFIQ - Test\n\tBergmannsveien 600\n\t3614 Kongsberg\n\tTfn: 123456789\n\tORG.NR: 825541012\n\nTERMINAL:\t\t203217333011101018149856\nBUTIKK:\t\t123456789 65842345\nDATO:2024-05-06\t\tTID:15:59\n\t\n\tKJØP\n\tGODKJENT\n\n\tIKKE KVITTERING FOR KJØP\n\n\nBELØP\t\tNOK 50,00\nTOTAL\t\tNOK 50,00\n\nContactless chip\nBankAxept\n**************1203\t\tPSN:02\n\n\tSAM K/1 3 000 DUM 786 911066\nKVITTERING:033206\t\tREF:307711749141\n\nATC:00103  AED:230201\t\t\nAID:D5780000021010\nTVR:8000008000\nARQC:0625FD24CA6EC896\n\n\tTA VARE PÅ KVITTERING, KUNDENS KOPI\n\n'
        #         }
        #     }
        # }

        transactionOutcome = response_json["transactionOutcome"]
        if transactionOutcome == "Approved":
            """ Test 3.2 Approved Payment  """
            return response_json
        else:
            """ Test 3.3 Declined Payment  """
            raise Warning("The transaction was {}.".format(transactionOutcome))

    def _worldline_do_request(self, method, url, body, client_id, host=None, key=None, ignore=[]):
        """ Test 3.4 Communication Log """
        self._create_log(
            {
                "url": url,
                "direction": "request",
                "host": request.httprequest.environ["HTTP_HOST"],
                "client_id": client_id,
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
        response_json = {}
        if response.data:
            response_json = json.loads(response.data)
        if response_json.get("transactionOutcome"):
            status = response_json["transactionOutcome"]
        else:
            status = "{} {}".format(response.status, response.reason)

        """ Test 3.4 Communication Log """
        values = {
            "url": url,
            "direction": "response",
            "host": self.worldline_host,
            "client_id": client_id,
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

        status = response.status
        ignore.append(200)
        if status not in ignore:
            if status in STATUS:
                raise Warning(STATUS[status])
            else:
                raise Warning("{} {}".format(status, response.reason))
        return response

    def _create_log(self, values):
        values["log"] = json.dumps(values.pop("log_json"), indent=4)
        record = self.env["pos.payment.terminal.log"].create(values)
        # The log is important, so save it immediately
        self.env.cr.commit()
        return record
