import logging
import math
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FleetVehicleOdometer(models.Model):
    _inherit = "fleet.vehicle.odometer"
    # _inherit = ["fleet.vehicle.odometer", "analytic.plan.mixin"]

    analytic_plan_id = fields.Many2one(
        comodel_name="account.analytic.plan",
        domain="[('parent_id', '!=', False)]",
    )

    comment = fields.Char("Comment")
    destination = fields.Char("Destination")
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
    value = fields.Integer(
        string="Odometer Stop",
    )
    value_start = fields.Integer(
        "Odometer Start",
        compute="_compute_start_and_distance_and_check_date",
        store=True,
    )
    product_variant_price = fields.Float(
        related="vehicle_id.product_id.lst_price",
        string="Unit Price",
    )
    user_ids = fields.Many2many(
        comodel_name="res.users",
        compute="_compute_user_ids",
        string="Users",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        next = records._get_next()
        (records | next)._compute_start_and_distance_and_check_date()
        return records

    def write(self, vals):
        old_next = self._get_next()
        res = super().write(vals)
        new_next = self._get_next()
        if 'vehicle_id' in vals or 'value' in vals:
            (self | old_next | new_next)._compute_start_and_distance_and_check_date()
        return res

    def unlink(self):
        next = self._get_next()
        super().unlink()
        next.exists()._compute_start_and_distance_and_check_date()

    @api.onchange("vehicle_id")
    def _set_driver_id_to_current_user_partner(self):
        for rec in self:
            if rec.vehicle_id and not rec.driver_id:
                rec.driver_id = self.env.user.employee_id.address_home_id

    @api.onchange("analytic_plan_id")
    def _reset_analytic(self):
        for rec in self:
            rec.analytic_account_id = False
            rec.analytic_account_ids = rec.analytic_plan_id.account_ids.filtered(lambda a: a.partner_id == rec.driver_id)

    @api.depends("analytic_account_ids.partner_id")
    def _compute_user_ids(self):
        for record in self:
            users = self.env["res.users"].search([
                ("employee_id.address_home_id", "in", record.analytic_account_ids.mapped("partner_id.id"))
            ])
            record.user_ids = users

    @api.constrains("value")
    def _check_value(self):
        for rec in self:
            if not rec.value or rec.value < 0:
                raise UserError(
                    _("Odometer value must be positive for vehicle %s.") % rec.vehicle_id.display_name
                )

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

    @api.onchange("vehicle_id", "value")
    def _compute_start_and_distance_and_check_date(self):
        for rec in self:
            vehicle = rec.vehicle_id
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
                else:
                    rec.value_start = 0
                rec.distance = max(0, rec.value - rec.value_start)
            else:
                rec.value_start = 0
                rec.distance = 0

    def _get_next(self):
        """ Return the next record of each record. """
        return self._get_related(operator=">", order="value asc")

    def _get_prev(self):
        """ Return the previous record of each record. """
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
