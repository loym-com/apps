import logging
import pprint
import requests

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
        TIMEOUT = 30

        _logger.info('request to worldline\n%s', pprint.pformat(data))

        if operation == "Payment":
            # Fredheim
            endpoint = "{}/pay".format(self.worldline_host)
        else:
            endpoint = "{}/api/v1/{}".format(self.worldline_host, operation)

        test_response = {
            "transactionOutcome": "Approved",
            "customer": {
                "plain": "Plain response",
                "escpos": "Escpos response",
            }
        }
        # return test_response

        req = requests.post(endpoint, json=data, timeout=TIMEOUT)

        # Authentication error doesn't return JSON
        if req.status_code == 401:
            return {
                'error': {
                    'status_code': req.status_code,
                    'message': req.text
                }
            }

        # if req.text == 'ok':
        #     return True

        return req.json()

