import base64
import csv
import logging
import io
import re
import requests
import pytz

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

# TODO: replace KEY & VALUE with teamm.alias
# KEY = {
#     "Record ID - Contact - Hubspot": "hubspot contact id",
#     "Ordre nr. ": "sale.order",
# }
# VALUE = {
#     "NEWSTART Smal": "NEWSTART Sølv",
#     "Unlocx Pain Relife": "Unlocx Pain Relief",
#     "Stressmestrings seminar": "Stressmestring",
#     "! Not entered": "",
#     "Del rom": "Share room",
#     "Privat": "Private",
# }

class TeamM(models.Model):
    _name = "teamm"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char()
    src = fields.Selection(
        [
            ('api', 'API'),
            ('csv_file', 'CSV File'),
            ('csv_field', 'CSV Field'),
        ],
        string="Data Source",
    )
    src_begin = fields.Integer(string="Begin With")
    src_end = fields.Integer(string="End With")
    model_ids = fields.One2many(
        "teamm.model",
        "teamm_id",
        string="Models",
        copy=True,
        help="Active models will be imported. Import one at a time to see the result."
        "Description, Primary Key and Values are only for documentation."
    )
    alias_ids = fields.One2many(
        "teamm.alias",
        "teamm_id",
        string="Aliases",
        copy=True,
    )
    url = fields.Char()
    param_ids = fields.One2many("teamm.param", "teamm_id", string="Params")
    csv_file = fields.Binary(string='CSV File')
    csv_file_name = fields.Char(string='CSV Filename')
    csv = fields.Text()
    csv_delimiter = fields.Char(default=",")
    date_format = fields.Char()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_import(self):
        method_name = "action_import_" + self.src
        method = getattr(self, method_name, None)
        return method()

    def action_import_api(self):
        self.ensure_one()
        Param = self.env["ir.config_parameter"].sudo()
        headers = {
            "X-API-SECRET-KEY": Param.get_param("X-API-SECRET-KEY"),
            "X-API-PUBLIC-KEY": Param.get_param("X-API-PUBLIC-KEY"),
            "X-API-APP-ID": Param.get_param("X-API-APP-ID"),
        }
        params = {p.key: p.value for p in self.param_ids if p.type == "api"}
        response = requests.get(self.url, headers=headers, params=params)
        if response.status_code != 200:
            raise UserError(response.text)
        return self._action_import(response.json())

    def action_import_csv_file(self):
        if self.csv_file:
            file_data = base64.b64decode(self.csv_file)
            csv_file = io.StringIO(file_data.decode('utf-8'))
            csv_reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
            return self._action_import([line for line in csv_reader])
        
    def action_import_csv_field(self):
        csv_file = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
        return self._action_import([line for line in csv_reader])
    
    def action_clear_csv(self):
        self.csv = ""

    def action_select_all_models(self):
        for model in self.model_ids:
            model.is_active = True

    def action_deselect_all_models(self):
        for model in self.model_ids:
            model.is_active = False

    def _action_import(self, teamm_values_list):
        _logger.info(f"{self.name} begin import")
        aliases = {
            alias_name: alias_record.name or ""
            for alias_record in self.alias_ids
            for alias_name in [a.strip() for a in alias_record.aliases.split(",")]
        }
        record_ids = []
        begin, end = self.src_begin, self.src_end
        model_names = self.model_ids.filtered("is_active").mapped("name")
        for model_name in model_names:
            record_ids = []
            for i, teamm_values in enumerate(teamm_values_list, start=1):
                if (begin and begin > i) or (end and end < i):
                    continue
                # Keys: replace alias, strip first/last spaces, lowercase
                # Values: replace alias, strip first/last spaces
                teamm_values = {
                    # Mismatch between CSV header and rows may cause error here
                    aliases.get(key.strip(), key).strip().lower():
                    aliases.get(val.strip(), val).strip()
                    for key, val in teamm_values.items()
                }
                teamm_values["discounts"] = self.convert_discounts(teamm_values, aliases)
                teamm_params = {p.key: p.value for p in self.param_ids if p.type == "code"}
                Model = self.env[model_name].with_context(
                    teamm=self,
                    teamm_values=teamm_values,
                    teamm_params=teamm_params,
                )
                records = Model._teamm2odoo()
                record_ids.extend(records.ids)
        _logger.info(f"{self.name} end import")
        if len(model_names) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Imported from Team M",
                "res_model": model_names[0],
                "views": [[False, "tree"], [False, "form"]],
                "domain": [("id", "in", record_ids)],
            }

    def convert_discounts(self, teamm_values, aliases):
        total_discount = teamm_values.get("total discount")
        if not total_discount or total_discount == "0":
            return []
        else:
            total_discount = total_discount[1:]  # remove minus

        # Get string
        discounts = teamm_values.get("discounts")
        # Convert to list
        discounts = discounts.split(", ")
        # Final discounts
        final_discounts = []
        for discount in discounts:
            if "total discount" in discount.lower():
                continue
            if ": " in discount:
                name, amount = discount.split(": ")
            else:
                name = discount
                amount = total_discount
            # Remove codes
            name = re.sub(r'\s*\(.*?\)\s*', '', name)
            # Replace aliases
            name = aliases.get(name, name)
            # Convert percentages
            amount = self._replace_discount_amount(teamm_values, amount)
            # Exclude "Total discount"
            if name != "Total discount":
                final_discounts.append((name, amount))

        known_discount = sum(amount for _, amount in final_discounts)
        unknown_discount = float(total_discount) - known_discount
        if unknown_discount:
            name = self.param_ids.filtered(
                lambda p: p.type == "code" and p.key == "default_discount"
            ).value
            final_discounts.append((name, unknown_discount))
        return final_discounts

    def _replace_discount_amount(self, teamm_values, amount):
        """
        amount: string
        return: float
        """
        try:
            if amount[-1] == "%":
                amount = float(teamm_values["subtotal"]) * float(amount[:-1]) / 100
            else:
                amount = float(amount)
            return amount
        except:
            hubspot_deal_id = teamm_values.get("hubspot deal id")
            raise ValidationError(f"Discount error on deal {hubspot_deal_id}")

    #
    # Used by other models
    #
    
    def _get_date(self, key):
        datestring = self._teamm2odoo_get_value(key)
        if datestring:
            date_format = self.env.context["teamm"].date_format
            if not date_format:
                raise UserError("Missing Date Format")
            return datetime.strptime(datestring, date_format).date()
    
    def _get_datetime(self, key):
        date_string = self._teamm2odoo_get_value(key)
        date_format = self.env.context["teamm"].date_format
        naive_date = datetime.strptime(date_string, date_format)
        naive_date = naive_date.replace(hour=0, minute=0, second=0, microsecond=0)
        user_timezone = pytz.timezone(self.env.user.tz)
        local_date = user_timezone.localize(naive_date)
        utc_date = local_date.astimezone(pytz.utc)
        naive_date = utc_date.replace(tzinfo=None)
        return naive_date
