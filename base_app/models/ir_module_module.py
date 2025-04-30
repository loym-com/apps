# -*- coding: utf-8 -*-

import logging
import csv
import os

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

PRICELESS = 1000.0

class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    price_user_group = fields.Char(default="base.group_user")
    price = fields.Monetary(default=PRICELESS, string="EUR/year")
    price1 = fields.Monetary(default=PRICELESS, string="1 user")
    price2 = fields.Monetary(default=PRICELESS, string="2-5 users")
    price3 = fields.Monetary(default=PRICELESS, string="6-25 users")
    price4 = fields.Monetary(default=PRICELESS, string="26-100 users")
    price5 = fields.Monetary(default=PRICELESS, string="101-300 users")
    price6 = fields.Monetary(default=PRICELESS, string="301-1000 users")
    price7 = fields.Monetary(default=PRICELESS, string="1001-3000 users")
    price8 = fields.Monetary(default=PRICELESS, string="3001-10000 users")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.ref("base.EUR").id,
    )

    def _compute_price(self):
        for record in self:
            user_group_xmlid = record.price_user_group or "base.group_user"
            user_group = self.env.ref(record.price_user_group)
            user_count = self.env["res.users"].search_count(
                [("groups_id", "in", [user_group.id])]
            )

            def convert(count):
                if count < 1:
                    return 0
                elif count == 1:
                    return 1
                elif count <= 5:
                    return 2
                elif count <= 25:
                    return 3
                elif count <= 100:
                    return 4
                elif count <= 300:
                    return 5
                elif count <= 1000:
                    return 6
                elif count <= 3000:
                    return 7
                else:
                    return 8

            record.price = getattr(record, f"price{convert(user_count)}", PRICELESS)

    def import_prices(self):

        # Automatically locate the CSV file in the same directory as this Python file
        csv_path = os.path.join(os.path.dirname(__file__), "prices.csv")
        if not os.path.exists(csv_path):
            raise ValidationError(f"File not found: {csv_path}")

        # Read the CSV file into memory
        prices_data = {}
        with open(csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            for row in reader:
                if len(row) < 10:
                    _logger.warning(f"Skipping invalid row: {row}")
                    continue

                module_name = row[0]
                price_user_group = row[1]
                prices = [float(price.replace(",", ".")) for price in row[2:10]]
                prices_data[module_name] = {
                    "price_user_group": price_user_group,
                    "prices": prices,
                }

        # Loop through self and update records based on the CSV data
        for record in self:
            module_data = prices_data.get(record.name)
            if not module_data:
                module_data = {
                    "price_user_group": "base.group_user",
                    "prices": [PRICELESS] * 8,
                }
            eur = self.env.ref("base.EUR")
            record.write({
                "price_user_group": module_data["price_user_group"],
                "currency_id": eur.id,
                "price1": module_data["prices"][0],
                "price2": module_data["prices"][1],
                "price3": module_data["prices"][2],
                "price4": module_data["prices"][3],
                "price5": module_data["prices"][4],
                "price6": module_data["prices"][5],
                "price7": module_data["prices"][6],
                "price8": module_data["prices"][7],
            })
        self._compute_price()
