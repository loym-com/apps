import logging
import math
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FleetVehicleOdometer(models.Model):
    _name = "fleet.vehicle.odometer"
    _inherit = ["fleet.vehicle.odometer", "analytic.plan.mixin"]

    comment = fields.Char("Comment")
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account"
    )
    analytic_account_ids = fields.Many2many(
        "account.analytic.account", string="Analytic Accounts"
    )
    analytic_account_distance = fields.Integer(
        "Analytic Distance",
        compute="_compute_analytic_account_distance",
        store=True,
        help="Compute how many km for each analytic account"
    )
    distance = fields.Integer(
        "Distance",
        compute="_compute_start_and_distance_and_check_date",
        store=True,
    )
    value_start = fields.Integer(
        "Odometer Start",
        compute="_compute_start_and_distance_and_check_date",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        next = self._get_next()
        next._compute_start_and_distance_and_check_date()
        return records

    def write(self, values):
        super().write(values)
        next = self._get_next()
        next._compute_start_and_distance_and_check_date()

    def unlink(self):
        next = self._get_next()
        super().unlink()
        next._compute_start_and_distance_and_check_date()

    @api.depends("analytic_account_ids", "distance")
    def _compute_analytic_account_distance(self):
        for record in self:
            count = len(record.analytic_account_ids)
            if count:
                record.analytic_account_distance = math.ceil(
                    record.distance / count
                )
            else:
                record.analytic_account_distance = 0

    @api.depends("value", "vehicle_id")
    def _compute_start_and_distance_and_check_date(self):
        for rec in self:
            vehicle = rec.vehicle_id
            rec.value_start = 0
            rec.distance = 0
            if vehicle:
                prev = rec._get_prev()
                if prev:
                    if rec.date and prev.date and rec.date < prev.date:
                        raise UserError(
                            (
                                "Date of current odometer entry is earlier than previous one.\n"
                                "Vehicle: %s\n"
                                "Current entry -> Date: %s, Value: %s\n"
                                "Previous entry -> Date: %s, Value: %s"
                            ) % (
                                vehicle.display_name,
                                rec.date,
                                rec.value,
                                prev.date,
                                prev.value,
                            )
                        )
                    rec.value_start = prev.value
                rec.distance = max(0, rec.value - rec.value_start)

    def _get_next(self):
        """ Return the next record of each record. """
        return self._get_related(operator=">", order="value asc")

    def _get_prev(self):
        """ Return the next record of each record. """
        return self._get_related(operator="<", order="value desc")

    def _get_related(self, operator, order):
        result = self.env[self._name].browse()
        for rec in self:
            if rec.value:
                search_domain = [
                    ('vehicle_id', '=', rec.vehicle_id.id),
                    ('value', operator, rec.value),
                ]
            else:
                search_domain = [
                    ('vehicle_id', '=', rec.vehicle_id.id),
                ]
                related = self.search(
                search_domain,
                order=order,
                limit=1,
            )
            result |= related
        return result
