import json
import logging
import os
import pprint
import requests
import urllib3

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    worldline_host = fields.Char(help="Format: https://host:port")
    worldline_key = fields.Char()

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [("worldline", "Worldline")]

    def proxy_worldline_request(self, data, operation):
        self.ensure_one()
        json_payload = json.dumps(data["payload"])

        _logger.info('request to worldline\n%s', pprint.pformat(json_payload))

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
        req = pool.urlopen('POST', '/api/v1/Payments', body=json_payload, headers=headers)
        req_json = json.loads(req.data)

        transactionOutcome = req_json["transactionOutcome"]
        if transactionOutcome == "Approved":
            return req_json
        else:
            raise UserError("The transaction was {}.".format(transactionOutcome))
