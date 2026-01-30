from odoo import api, fields, models
from calendar import monthrange


class PayslipRun(models.Model):
    _inherit = "hr.payslip.run"

    json = fields.Serialized()
    l10n_no_AgapliktUtenLoennsopplysningsplikt = fields.Integer(
        "Aga-plikt uten lønnsopplysningsplikt", sparse="json"
    )
    l10n_no_Loennsutbetalingsdato = fields.Date(
        "Lønnsutbetalingsdato", sparse="json"
    )
    date_start = fields.Date(
        compute="_compute_dates",
        readonly=False,
    )
    date_end = fields.Date(
        compute="_compute_dates",
        readonly=False,
    )

    @api.depends("l10n_no_Loennsutbetalingsdato")
    def _compute_dates(self):
        for record in self:
            if record.l10n_no_Loennsutbetalingsdato:
                date = record.l10n_no_Loennsutbetalingsdato
                # Set the date_start and date_end to first/last day of month
                record.date_start = date.replace(day=1)
                record.date_end = date.replace(
                    day=monthrange(date.year, date.month)[1]
                )
                # Update payslips in the run
                record.slip_ids.l10n_no_Loennsutbetalingsdato = date
            else:
                record.date_start = record.date_start
                record.date_end = record.date_end
