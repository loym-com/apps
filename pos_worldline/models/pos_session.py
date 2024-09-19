import json
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = 'pos.session'

    worldline_print = fields.Text()

    def _validate_session(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        self.ensure_one()
        for worldline in self.payment_method_ids.filtered(
            lambda pm: pm.use_payment_terminal == "worldline"
        ):
            self._worldline_do_capture(worldline)
        return super()._validate_session(balancing_account, amount_to_balance, bank_payment_method_diffs)

    def _worldline_do_capture(self, payment_method):
        """ Test 3.6 Capture / End of day """
        # Send Capture request to terminal
        response = payment_method._worldline_do_request("POST", "/api/v1/Captures")
        # Print receipt
        try:
            print = json.loads(response.data)["receipt"]["merchant"]["plain"]
            print = print.replace("\\n", "\n")
            print = print.replace("\\t", "\t")
            self.worldline_print = print
        except json.JSONDecodeError as e:
            message = f"{self.name} validation: JSON decoding error: {e}"
            _logger.error(message)
            # This doesn't work, since the UI changes from POS to WEB.
            self.env.user.notify_danger(message=message)




        """
        point_of_sale printers.js
        data["receipt"] should be an image! js converts html to image.
        """
        # response_json = json.loads(response.data)
        # data = {
        #     "action": "print_receipt",
        #     "receipt": response_json["receipt"]["merchant"]["escpos"], # plain / escpos
        # }
        # data_json = json.dumps(data)
        # headers = {
        #     "Content-Type": "application/json",
        # }
        # url = "http://{}:8069/hw_proxy/default_printer_action".format(
        #     session.config_id.proxy_ip
        # )




        # response = requests.post(url, json=data_json, headers=headers)
        # raise UserError(str(response.status_code) + response.reason + response.text)
        # 400BAD REQUESTInvalid JSON-RPC data

        """
        w3schools

        Parse JSON - Convert from JSON to Python

        my_json = '{ "name":"John", "age":30, "city":"New York"}'
        my_dict = json.loads(my_json)


        Convert from Python to JSON

        my_dict = {
        "name": "John",
        "age": 30,
        "city": "New York"
        }
        my_json = json.dumps(my_dict)


        """

        # try:
        #     response = requests.post(url, data=data_json)
        #     # You can process the response here if needed
        #     return response.text
        # except requests.exceptions.RequestException as e:
        #     return f"Error: {e}"
