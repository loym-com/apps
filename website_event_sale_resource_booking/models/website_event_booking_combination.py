import logging

from collections import defaultdict
from datetime import datetime

from odoo import api, fields, models, tools
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting

_logger = logging.getLogger(__name__)


class EventBookingCombination(models.Model):
    _name = "website.event.booking.combination"
    _description = "website.event.booking.combination"
    _auto = False
    _inherits = {"product.product": "product_id"}
    _inherit = [
        "website.sale.product.mixin",
        "website.searchable.mixin",
    ]

    id = fields.Char()
    event_id = fields.Many2one("event.event")
    date_begin = fields.Datetime("Begin")
    date_end = fields.Datetime("End")
    product_id = fields.Many2one("product.product", required=True, ondelete="cascade")
    combination_id = fields.Many2one("resource.booking.combination")

    # Computed fields

    available = fields.Boolean(compute="_compute_available", search="_search_available")
    resource_group_tag_ids = fields.Many2many(
        "resource.group.tag",
        compute="_compute_resource_group_tag_ids",
        search="_search_resource_group_tag_ids",
    )
    product_attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        relation="resource_booking_type_product_attribute_value_rel",
        related="resource_booking_type_id.product_attribute_value_ids",
    )

    def _compute_available(self):
        # records_per_event = self.grouped("event_id") # 17.0
        records_per_event = defaultdict(lambda: self.env["website.event.booking.combination"])
        for record in self:
            records_per_event[record.event_id] |= record

        bookings = self.env["resource.booking"].search(
            [("start", "!=", False), ("stop", "!=", False)]
        )

        for event, records in records_per_event.items():
            filtered_bookings = bookings.filtered(
                lambda b:
                (b.start >= event.date_begin and b.start < event.date_end)
                or
                (b.stop > event.date_begin and b.stop <= event.date_end)
            )
            for record in records:
                # Available if no intersection of resources
                record.available = not bool(
                    record.combination_id.resource_ids
                    &
                    filtered_bookings.combination_id.resource_ids
                )
    
    def _search_available(self, operator, value):
        compare = {
            "=": "in",
            "!=": "not in",
        }
        assert operator in compare and value in (True, False)
        future = self.search([("event_id.date_end", ">", datetime.now())])
        filtered = future.filtered(lambda r: r.available == value)
        return [("id", compare[operator], filtered.ids)]

    def _compute_resource_group_tag_ids(self):
        for record in self:
            record.resource_group_tag_ids = record.combination_id.resource_ids.group_id.tag_ids.ids

    def _search_resource_group_tag_ids(self, operator, value):
        tags = self.env["resource.group.tag"].search(
            [
                "|",
                ("name", operator, value),  # search view
                ("id", operator, value),    # /shop
            ]
        )
        combinations = tags.group_ids.resource_ids.combination_ids
        return [("combination_id", "in", combinations.ids)]

    # SQL VIEW

    def init(self):
        tools.drop_view_if_exists(self._cr, "website_event_booking_combination")

        pp = self.env["product.product"]
        pt = self.env["product.template"]
        ee = self.env["event.event"]
        rbt = self.env["resource.booking.type"]
        rbc = self.env["resource.booking.combination"]

        # Get all stored columns (except "id") of the first model
        # Add missing columns of the next models.
        models = [("pp", pp), ("pt", pt), ("ee", ee), ("rbt", rbt), ("rbc", rbc)]

        column_name_expr = [
            ("id", "ee.id::text || '_' || pp.id::text || '_' || rbc.id::text"),
            ("event_id", "ee.id"),
            ("product_id", "pp.id"),
            ("combination_id", "rbc.id"),
        ]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type:
                    if name not in [c[0] for c in column_name_expr]:
                        column_name_expr.append((name, code + "." + name))
        select = ["{} AS {}".format(expr, name) for name, expr in column_name_expr]

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW website_event_booking_combination AS
            SELECT {", ".join(select)}
            FROM event_event ee
            JOIN product_template pt ON ee.product_tmpl_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            JOIN resource_booking_type rbt ON pp.resource_booking_type_id = rbt.id
            JOIN resource_booking_type_combination_rel rbt_rbc ON rbt_rbc.type_id = rbt.id
            JOIN resource_booking_combination rbc ON rbt_rbc.combination_id = rbc.id
            """
        )
