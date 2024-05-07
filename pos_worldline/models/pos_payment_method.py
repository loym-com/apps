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

    def proxy_worldline_request(self, data, operation):
        TerminalLog = self.env["pos.payment.terminal.log"]
        self.ensure_one()
        json_payload = json.dumps(data["payload"])
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'Integration-Key': self.worldline_key,
            'User-Agent' : 'MyECR 1.0',
            'Content-Length': str(len(json_payload))
        }
        dir_name = os.path.dirname(__file__)
        cert_relative_path = "ECR-REST.crt"
        cert_absolute_path = os.path.join(dir_name, cert_relative_path)

        pool = urllib3.HTTPSConnectionPool(
            self.worldline_host,
            assert_hostname=False, # Setting assert_hostname to False disables the hostname verification because URL will not match certificate.
            ca_certs=cert_absolute_path,
        )

        # LOGGING START
        desc = {
            "desc": "'Payments' to send from Odoo",
            "company": self.env.company.name,
            "user": self.env.user.login,
            # "REMOTE_ADDR": request.httprequest.environ["REMOTE_ADDR"],
            # "REMOTE_PORT": request.httprequest.environ["REMOTE_PORT"],
            "HTTP_HOST": request.httprequest.environ["HTTP_HOST"],
            # "PATH_INFO": request.httprequest.environ["PATH_INFO"],
            # "to_ip": self.worldline_host,
        }
        TerminalLog.create_log(desc, data["payload"])
        # LOGGING END

        req = pool.urlopen('POST', '/api/v1/Payments', body=json_payload, headers=headers)
        req_json = json.loads(req.data)
        # req_json = {
        #     "transactionOutcome": "Approved",
        #     "receipt": {
        #         "customer": {
        #             "plain": '\tFIQ - Test\n\tBergmannsveien 600\n\t3614 Kongsberg\n\tTfn: 123456789\n\tORG.NR: 825541012\n\nTERMINAL:\t\t203217333011101018149856\nBUTIKK:\t\t123456789 65842345\nDATO:2024-05-06\t\tTID:15:59\n\t\n\tKJØP\n\tGODKJENT\n\n\tIKKE KVITTERING FOR KJØP\n\n\nBELØP\t\tNOK 50,00\nTOTAL\t\tNOK 50,00\n\nContactless chip\nBankAxept\n**************1203\t\tPSN:02\n\n\tSAM K/1 3 000 DUM 786 911066\nKVITTERING:033206\t\tREF:307711749141\n\nATC:00103  AED:230201\t\t\nAID:D5780000021010\nTVR:8000008000\nARQC:0625FD24CA6EC896\n\n\tTA VARE PÅ KVITTERING, KUNDENS KOPI\n\n'
        #         }
        #     }
        # }

        # LOGGING START
        desc = {
            "desc": "Payments response from Worldline terminal",
            "host": self.worldline_host,
        }
        TerminalLog.create_log(desc, req_json)
        # LOGGING END

        transactionOutcome = req_json["transactionOutcome"]
        if transactionOutcome == "Approved":
            return req_json
        else:
            raise UserError("The transaction was {}.".format(transactionOutcome))
