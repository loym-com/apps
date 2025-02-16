from odoo import fields, models


class Leave(models.Model):
    _inherit = "hr.leave"

    # Origin: hr_contract_leave
    # contract_id = fields.Many2one("hr.contract", string="Contract")
    # percent = fields.Float(help="40.0 means 40 percent leave, 60 percent work")

    l10n_no_type = fields.Selection(related="holiday_status_id.l10n_no_type")
    l10n_no_varslingsdato = fields.Date("Date warning")
    l10n_no_sluttdatoLoennsplikt = fields.Date("Salary end date")
