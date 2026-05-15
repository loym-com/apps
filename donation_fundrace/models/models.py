import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DonationFundraceSponsorship(models.Model):
    _name = "donation.fundrace.sponsorship"
    _description = "donation.fundrace.sponsorship"

    @api.depends("amount_per_lap", "laps", "amount_fixed")
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = (
                record.amount_per_lap * record.laps + record.amount_fixed
            )

    @api.depends("amount_total", "currency_id.inverse_rate")
    def _compute_amount_total_nok(self):
        for record in self:
            record.amount_total_nok = record.amount_total * record.currency_id.inverse_rate

    @api.depends("runner_id.laps")
    def _compute_laps(self):
        for record in self:
            record.laps = record.runner_id.laps

    amount_fixed = fields.Integer("Fixed amount")
    amount_per_lap = fields.Integer("Amount per lap")
    amount_total = fields.Integer(
        "Total amount", readonly=True, store=True, compute="_compute_amount_total"
    )
    amount_total_nok = fields.Integer(
        "Total amount NOK",
        readonly=True,
        store=False,
        compute="_compute_amount_total_nok",
    )
    currency_id = fields.Many2one("res.currency", string="Currency")
    laps = fields.Integer("Laps", readonly=True, store=True, compute="_compute_laps")
    name = fields.Char("Name")
    payment = fields.Char("Payment")
    runner_id = fields.Many2one("donation.fundrace.partner", string="Runner")
    sponsor_id = fields.Many2one("donation.fundrace.partner", string="Sponsor")
    event_id = fields.Many2one("event.event", string="Event")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        store=True,
        index=True,
        default=lambda self: self.env.company,
    )


class DonationFundracePartner(models.Model):
    _name = "donation.fundrace.partner"
    _description = "donation.fundrace.partner"
    _inherits = {"res.partner": "partner_id"}

    @api.depends("runners.amount_total_nok")
    def _compute_runners_total_nok(self):
        for record in self:
            total_nok = 0
            for runners in record.runners:
                total_nok += runners.amount_total_nok
            record.runners_total_nok = total_nok

    @api.depends("sponsors.amount_total_nok")
    def _compute_sponsors_total_nok(self):
        for record in self:
            total_nok = 0
            for sponsors in record.sponsors:
                total_nok += sponsors.amount_total_nok
            record.sponsors_total_nok = total_nok

    laps = fields.Integer("Amount of laps")
    runners = fields.One2many(
        "donation.fundrace.sponsorship", "sponsor_id", string="Runners sponsored"
    )
    runners_total_nok = fields.Integer(
        "Runners sponsored total",
        readonly=True,
        store=False,
        compute="_compute_runners_total_nok",
    )
    sponsors = fields.One2many(
        "donation.fundrace.sponsorship", "runner_id", string="Sponsors"
    )
    sponsors_total_nok = fields.Integer(
        "Sponsors total NOK",
        readonly=True,
        store=False,
        compute="_compute_sponsors_total_nok",
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="restrict"
    )
    event_id = fields.Many2one("event.event", string="Event")
