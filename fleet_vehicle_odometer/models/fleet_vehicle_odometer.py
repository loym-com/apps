import logging
import math
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FleetVehicleOdometer(models.Model):
    _name = "fleet.vehicle.odometer"
    _inherit = ["fleet.vehicle.odometer", "analytic.plan.mixin"]

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
    comment = fields.Char("Comment")
    distance = fields.Integer("Distance")
    value_int = fields.Integer("Odometer")

    @api.onchange("value_int")
    def _onchange_set_value(self):
        for record in self:
            record.value = float(record.value_int)

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

    def unlink(self):
        self._recompute_distance_before_unlink()
        return super().unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            self._recompute_distance_before_create(values)
        return super().create(vals_list)

    def write(self, values):
        recompute_distance = False
        for value in values:
            if value in ("date", "vehicle_id", "value"):
                recompute_distance = True
        if recompute_distance:
            for record in self:
                record._recompute_distance_before_unlink()
                values["date"] = values.get("date") or record.date
                values["vehicle_id"] = values.get("vehicle_id") or record.vehicle_id.id
                values["value"] = values.get("value") or record.value
                record._recompute_distance_before_create(values)
        return super().write(values)

    def _recompute_distance_before_unlink(self):
        for record in self:
            prev = self._get_record("prev")
            next = self._get_record("next")
            if prev and next:
                next.distance = next.value - prev.value
            elif next:
                next.distance = None

    def _recompute_distance_before_create(self, values):
        prev = self._get_record("prev", values)
        next = self._get_record("next", values)
        self._check_date(prev, next, values)
        self._set_distance(prev, next, values)

    def _check_date(self, prev, next, values):
        value = values.get("value") or self.value
        date = values["date"]
        if type(date) is str:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if prev and prev.date > date:
            raise UserError(
                _("Date should not be lower than {} for odometer value {}.").format(
                    str(prev.date), str(value)
                )
            )
        if next and next.date < date:
            raise UserError(
                _("Date should not be higher than {} for odometer value {}.").format(
                    str(next.date), str(value)
                )
            )

    def _set_distance(self, prev, next, values):
        if prev:
            values["distance"] = values["value"] - prev.value
        else:
            values["distance"] = 0
        if next:
            next.distance = next.value - values["value"]

    @api.onchange("value")
    def _onchange_set_distance(self):
        prev = self._get_record("prev")
        if prev:
            self.distance = self.value - prev.value
        else:
            self.distance = 0

    def _get_record(self, which, values=None):
        if values:
            assert type(values) == dict
        else:
            self.ensure_one()

        def _get(field_name):
            if values:
                return values[field_name]
            else:
                value = getattr(self, field_name)
                if hasattr(value, "id"):
                    value = getattr(value, "id")
                return value

        sign = {"prev": "<", "next": ">"}
        order = {"prev": "value desc", "next": "value"}
        id = self.ids[0] if self.ids and type(self.ids[0]) is int else 0

        return self.search(
            [
                ("vehicle_id", "=", _get("vehicle_id")),
                ("value", sign[which], _get("value")),
                ("id", "!=", id),
            ],
            order=order[which],
            limit=1,
        )
