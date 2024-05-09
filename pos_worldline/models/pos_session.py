from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _validate_session(self):
        self.ensure_one()
        for payment_method in self.payment_method_ids:
            if payment_method.use_payment_terminal == "worldline":
                payment_method.worldline_do_capture()
        return super()._validate_session()
