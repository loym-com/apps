from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    country_group_ids = fields.Many2many(
        string="Country Groups",
        readonly=True,
        related="country_id.country_group_ids",
        comodel_name="res.country.group",
        relation="res_partner_country_group_rel",
        column1="partner_id",
        column2="country_group_id",
    )

    # Compute methods

    @api.depends("donation_ids.thanks_printed")
    def _compute_donation_send_thanks(self):
        for partner in self:
            partner.donation_send_thanks = bool(
                partner.donation_ids.filtered(lambda d: not d.thanks_printed)
            )

    @api.depends("donation_thanks_ids.print_date")
    def _compute_donation_thanks_send(self):
        for partner in self:
            partner.donation_thanks_send = bool(
                partner.donation_thanks_ids.filtered(lambda d: not d.print_date)
            )

    @api.depends("donation_tax_receipt_ids.print_date")
    def _compute_donation_tax_receipt_send(self):
        for partner in self:
            partner.donation_tax_receipt_send = bool(
                partner.donation_tax_receipt_ids.filtered(lambda d: not d.print_date)
            )

    # To search on these fields, they are stored.

    donation_send_thanks = fields.Boolean(
        string="Send DONATION Thanks",
        compute="_compute_donation_send_thanks",
        store=True,
        help="""Filter on donors who (don't) need a thanks.\n
                Send it e.g. together with a newsletter.""",
    )
    donation_thanks_send = fields.Boolean(
        string="DONATION THANKS to send",
        compute="_compute_donation_thanks_send",
        store=True,
        help="""Filter on donors with(out) a thanks to send.\n
                Send it e.g. together with a newsletter.""",
    )
    donation_tax_receipt_send = fields.Boolean(
        string="DONATION TAX RECEIPT to send",
        compute="_compute_donation_tax_receipt_send",
        store=True,
        help="""Filter on donors who (don't) need a tax receipt.\n
                Send it e.g. together with a newsletter.""",
    )

    # The boolean fields above depend on the One2many fields below.

    donation_ids = fields.One2many(
        comodel_name="donation.donation",
        inverse_name="partner_id",
        string="Donations",
        help="All donations made by this donor.",
    )
    donation_thanks_ids = fields.One2many(
        comodel_name="donation.thanks",
        inverse_name="partner_id",
        string="Donation Thanks",
        help="All donations thanks to this donor.",
    )
    donation_tax_receipt_ids = fields.One2many(
        comodel_name="donation.tax.receipt",
        inverse_name="partner_id",
        string="Tax Receipts",
        help="All tax receipts for this donor.",
    )

    # Actions

    def action_donation_ids_to_send_thanks(self):
        xml_id = "donation.donation_action"
        act = self.env["ir.actions.actions"]._for_xml_id(xml_id)
        act["domain"] = [("partner_id", "in", self.ids), ("thanks_printed", "=", False)]
        return act

    def action_donation_thanks_ids_to_send(self):
        xml_id = "donation_thanks.donation_thanks_action"
        action = self.env["ir.actions.actions"]._for_xml_id(xml_id)
        action["domain"] = [("partner_id", "in", self.ids), ("print_date", "=", False)]
        return action

    def action_donation_tax_receipt_ids_to_send(self):
        xml_id = "donation_base.donation_tax_receipt_action"
        action = self.env["ir.actions.actions"]._for_xml_id(xml_id)
        action["domain"] = [("partner_id", "in", self.ids), ("print_date", "=", False)]
        return action
