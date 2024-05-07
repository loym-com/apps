import datetime
import json

from odoo import fields, models
from odoo.exceptions import UserError

# Inspired by https://developer.samport.com/integration-guidelines/logging-page/
class PosPaymentLog(models.Model):
    _name = "pos.payment.terminal.log"
    _description = "Log for POS payment requests"
    _order = "timestamp desc"

    timestamp = fields.Datetime()
    description = fields.Text()
    log = fields.Text()

    def create_log(self, desc_json, log_json):
        desc_str = json.dumps(desc_json, indent=4)
        log_str = json.dumps(log_json, indent=4)
        record = self.env["pos.payment.terminal.log"].create(
            {
                "timestamp": datetime.datetime.now(),
                "description": desc_str,
                "log": log_str,
            }
        )
        return record

    def action_export_log(self):
        log = []
        for record in self:
            log.append(record.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'))
            log.append(record.description)
            log.append(record.log)
            log.append("")
        raise UserError("\n".join(log))
