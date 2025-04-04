# from datetime import date, datetime

# from odoo import models, fields, api

# class ReportTaxReceipt(models.AbstractModel):
#     _name = "report.donation_thanks.report_donation_tax_receipt"
#     _description = "Donation tax receipt thanks report"

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env["donation.tax.receipt"].browse(docids)
#         today = date.today()
#         langs = self.env["res.lang"].search([])
#         today_langs = {lang.code: today.strftime(lang.date_format) for lang in langs}
#         return {
#             "doc_ids": docids,
#             "doc_model": "res.partner",
#             "docs": docs,
#             "today": today_langs,
#         }
