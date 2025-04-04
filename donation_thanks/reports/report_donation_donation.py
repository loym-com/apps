from datetime import date, datetime

from odoo import models, fields, api

class ReportDonationThanks(models.AbstractModel):
    _name = "report.donation_thanks.report_donation_donation"
    _description = "Donation thanks report"

    # PURPOSE: get today's date (not available in donation.donation)
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["donation.donation"].browse(docids)
        today = date.today()
        langs = self.env["res.lang"].search([])
        today_langs = {lang.code: today.strftime(lang.date_format) for lang in langs}
        return {
            "doc_ids": docids,
            "doc_model": "donation.donation",
            "docs": docs,
            "today": today_langs,
        }
