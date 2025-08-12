from dateutil.relativedelta import relativedelta

from odoo import fields, models, tools


class ResourceBookingGroup(models.Model):
    _name = "resource.booking.group"
    _description = "resource.booking.group"
    _auto = False

    id = fields.Char()
    group_id = fields.Many2one("resource.group", string="Resource Group")
    name = fields.Char()
    duration = fields.Float()
    start = fields.Datetime()
    stop = fields.Datetime()

    # SQL VIEW

    def init(self):
        tools.drop_view_if_exists(self._cr, "resource_booking_group")

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW resource_booking_group AS
            SELECT DISTINCT
                rb.id::text || '_' || rbc.id::text AS id,
                rr.group_id,
                rg.name,
                rb.duration,
                date_trunc('second', rb.start) AS start,
                date_trunc('second', rb.stop) AS stop
            FROM resource_booking rb
            JOIN resource_booking_combination rbc ON rb.combination_id = rbc.id
            JOIN resource_booking_combination_resource_resource_rel rbc_rr
                    ON rbc_rr.resource_booking_combination_id = rbc.id
            JOIN resource_resource rr ON rbc_rr.resource_resource_id = rr.id
            JOIN resource_group rg ON rr.group_id = rg.id;
            """
        )
