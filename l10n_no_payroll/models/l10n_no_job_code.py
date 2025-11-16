import inspect
import os

from odoo import api, fields, models


class JobCode(models.Model):
    _name = "l10n.no.job.code"
    _description = "Norwegian Profession Codes"
    _rec_name_search = ["code", "name"]

    code = fields.Char()
    name = fields.Char()

    @api.depends("name", "code")
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.name:
                rec.display_name = f"{rec.code} {rec.name}"
            else:
                rec.display_name = rec.code or rec.name or ""

    def post_init_hook_import_job_codes(self):
        directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        file_path =  os.path.join(directory_path, '../data/l10n.no.job.code.csv')
        with open(file_path, "r") as file:
            import_record = self.env['base_import.import'].create(
                {
                    "file": file.read(),
                    "file_name": "l10n.no.job.code.csv",
                    "file_type": "text/csv",
                    "res_model": "l10n.no.job.code",
                }
            )
            import_record.execute_import(
                columns=["code", "parentCode", "level", "name", "shortName", "notes", "validFrom", "validTo"],
                fields=["code", False, False, "name", False, False, False, False],
                # options changed:
                # - separator ;
                # - encoding utf-8
                # - limit 10000
                options={
                    'headers': True,
                    'advanced': False,
                    'keep_matches': False,
                    'name_create_enabled_fields': {},
                    'skip': 0,
                    'limit': 10000,
                    'encoding': 'utf-8',
                    'separator': ';',
                    'quoting': '"',
                    'sheet': '',
                    'date_format': '',
                    'datetime_format': '',
                    'float_thousand_separator': ',',
                    'float_decimal_separator': '.',
                    'fields': [],
                },
            )
