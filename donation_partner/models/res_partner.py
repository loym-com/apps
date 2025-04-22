from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("donation_ids.thanks_printed")
    def _compute_donation_send_thanks(self):
        for partner in self:
            if partner.donation_ids.filtered(lambda d: not d.thanks_printed):
                partner.donation_send_thanks = "yes"
            else:
                partner.donation_send_thanks = "no"

    @api.depends("tax_receipt_ids.print_date")
    def _compute_tax_receipt_send(self):
        for partner in self:
            if partner.tax_receipt_ids.filtered(lambda d: not d.print_date):
                partner.tax_receipt_send = "yes"
            else:
                partner.tax_receipt_send = "no"

    # Stored selection to search on the <field>
    donation_send_thanks = fields.Selection(
        string="Send Donation Thanks",
        selection=[("yes", "Yes"), ("no", "No")],
        compute="_compute_donation_send_thanks",
        store=True,
        help="""Filter on donors who (don't) need a thanks.\n
                Send it e.g. together with a newsletter.""",
    )

   # Stored selection to search on the <field>
    tax_receipt_send = fields.Selection(
        string="Send Donation Tax Receipt",
        selection=[("yes", "Yes"), ("no", "No")],
        compute="_compute_tax_receipt_send",
        store=True,
        help="""Filter on donors who (don't) need a tax receipt.\n
                Send it e.g. together with a newsletter.""",
    )

#     @api.depends("donation_ids.thanks_printed")
#     def _compute_donation_send_thanks(self):
#         for partner in self:
#             partner.donation_send_thanks = bool(
#                 partner.donation_ids.filtered(lambda d: not d.thanks_printed)
#             )

#     @api.depends("donation_ids.thanks_template_id")
#     def _compute_donation_missing_report_template(self):
#         for partner in self:
#             partner.donation_missing_report_template = bool(
#                 partner.donation_ids.filtered(lambda d: not d.thanks_template_id)
#             )

#     @api.depends("tax_receipt_ids.print_date")
#     def _compute_tax_receipt_send(self):
#         for partner in self:
#             partner.tax_receipt_send = bool(
#                 partner.tax_receipt_ids.filtered(lambda d: not d.print_date)
#             )

    # @api.depends("tax_receipt_ids.thanks_template_id")
    # def _compute_tax_receipt_missing_report_template(self):
    #     for partner in self:
    #         partner.tax_receipt_missing_report_template = bool(
    #             partner.tax_receipt_ids.filtered(lambda d: not d.thanks_template_id)
    #         )

    donation_ids = fields.One2many(
        comodel_name="donation.donation",
        inverse_name="partner_id",
        string="Donations",
        help="All donations made by this donor.",
    )
    tax_receipt_ids = fields.One2many(
        comodel_name="donation.tax.receipt",
        inverse_name="partner_id",
        string="Tax Receipts",
        help="All tax receipts made by this donor.",
    )

    # # To search on these fields, they are stored.

    # donation_send_thanks = fields.Boolean(
    #     string="Send Donation Thanks",
    #     compute="_compute_donation_send_thanks",
    #     store=True,
    #     help="""Filter on donors who (don't) need a thanks.\n
    #             Send it e.g. together with a newsletter.""",
    # )
    # donation_missing_report_template = fields.Boolean(
    #     string="Donations missing report",
    #     compute="_compute_donation_missing_report_template",
    #     store=True,
    #     help="Filter on donors who are(n't) missing a report template on a donation.",
    # )
    # tax_receipt_send = fields.Boolean(
    #     string="Send Donation Tax Receipt",
    #     compute="_compute_tax_receipt_send",
    #     store=True,
    #     help="""Filter on donors who (don't) need a tax receipt.\n
    #             Send it e.g. together with a newsletter.""",
    # )
    # tax_receipt_missing_report_template = fields.Boolean(
    #     string="Tax receipts missing report",
    #     # compute="_compute_tax_receipt_missing_report_template",
    #     store=True,
    #     help="Filter on donors who are missing a report template on a tax receipt.",
    # )
