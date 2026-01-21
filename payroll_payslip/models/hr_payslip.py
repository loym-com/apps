import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def _compute_name(self):
        # Temporary
        from datetime import datetime, time
        import babel
        from odoo import tools

        for record in self:
            lang = record.employee_id.lang
            if lang:
                record = record.with_context(lang=lang)
            # super(HrPayslip, record)._compute_name()

            # Temporary (until I can translate in OCA)
            if lang == "nb_NO":
                expr = "Lønnsslipp til %(name)s for %(dt)s"
            else:
                expr = "Salary Slip of %(name)s for %(dt)s"
            record.name = expr % {
                "name": record.employee_id.name,
                "dt": tools.ustr(
                    babel.dates.format_date(
                        date=datetime.combine(record.date_from, time.min),
                        format="MMMM-y",
                        locale=record.env.context.get("lang") or "en_US",
                    )
                ),
            }

    def get_lines_dict(self):
        lines_dict = {}

        for payslip in self:
            lang = payslip.employee_id.lang
            if lang:
                payslip = payslip.with_context(lang=payslip.employee_id.lang)
            lines_dict.update(super(HrPayslip, payslip).get_lines_dict())

        return lines_dict
