import json
import logging
import os
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    worldline_host = fields.Char(help="Format: https://host:port")
    worldline_key = fields.Char()

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [("worldline", "Worldline")]

    def worldline_do_capture(self):
        """ Test 3.6 Capture / End of day """
        self.ensure_one()
        response = self._worldline_do_request("POST", "/api/v1/Captures", None, None)
        # TODO: print receipt

    def worldline_do_payment(self, payment):
        self.ensure_one()
        client_id = payment["customData"]["client_id"]

        """ Test 3.7 No Connection """
        response = self._worldline_do_request("GET", "/api/v1/Payments/latest", None, client_id)
        response_json = json.loads(response.data)

        if response.status == 404:
            # First payment since "Dagsavslutt"
            log_exists = False
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
        if log_exists:
            # No payment has happened during a loss of connection.
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

        """ Test 3.5 Terminal Busy """
        if response.status == 503:
            raise UserError("The terminal was busy and did not process your request, please try again.")

        transactionOutcome = response_json["transactionOutcome"]
        if transactionOutcome == "Approved":
            """ Test 3.2 Approved Payment  """
            return response_json
        else:
            """ Test 3.3 Declined Payment  """
            raise UserError("The transaction was {}.".format(transactionOutcome))

    def _worldline_do_request(self, method, url, body, client_id):
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
            'Integration-Key': self.worldline_key,
            'User-Agent' : 'Odoo 14.0',
            'Content-Length': str(len(body_json))
        }
        dir_name = os.path.dirname(__file__)
        cert_relative_path = "ECR-REST.crt"
        cert_absolute_path = os.path.join(dir_name, cert_relative_path)

        pool = urllib3.HTTPSConnectionPool(
            self.worldline_host,
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
            # response_json is missing if previous payment is still going on.
            assert response_json
            values["receipt_no"] = response_json["receiptNumber"]
            values["receipt_total"] = response_json["amounts"]["total"]
        self._create_log(values)
        return response

    def _create_log(self, values):
        values["log"] = json.dumps(values.pop("log_json"), indent=4)
        record = self.env["pos.payment.terminal.log"].create(values)
        # The log is important, so save it immediately
        self.env.cr.commit()
        return record
