import logging

from odoo import fields, models

from .tabelltrekk2025 import tabelltrekk as tabelltrekk20xx

YEAR = 2025

_logger = logging.getLogger(__name__)


class Tabelltrekk(models.Model):
    _name = "l10n.no.tabelltrekk"
    _description = "Tax tables with tax deduction amounts"

    year = fields.Integer("Year")
    tabellnummer = fields.Char("Tabellnummer", size=4)
    trekkperiode = fields.Char("Trekkperiode", size=1)
    tabelltype = fields.Char("Tabelltype", size=1)
    trekkgrunnlag = fields.Integer("Trekkgrunnlag")
    trekk = fields.Integer("Trekk")

    def post_init_hook_import_tax_deduction_tables(self):
        year_exists = self.search([("year", "=", YEAR)], limit=1)
        if not year_exists:
            lines = tabelltrekk20xx.splitlines()
            count = 0
            sql = (
                sql_base
            ) = """INSERT INTO l10n_no_tabelltrekk (
                year, tabellnummer, trekkperiode, tabelltype, trekkgrunnlag, trekk
            ) VALUES """
            for line in lines:
                sql += """
                    (%s, %s, %s, %s, %s, %s),""" % (
                    YEAR,
                    line[:4],
                    line[4],
                    line[5],
                    line[6:][:6],
                    line[12:][:6],
                )
                # execute sql[:-1] without the last comma
                count += 1
                if count >= 1000:
                    self.env.cr.execute(sql[:-1])
                    count = 0
                    sql = sql_base
            if sql != sql_base:
                self.env.cr.execute(sql[:-1])
            self.invalidate_model()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def l10n_no_get_tax_deduction(
        self, year, trekkperiode, tabelltype, trekkgrunnlag, andel_av_trekk
    ):
        """
        #year: Integer
        #trekkperiode: String [('1','maaned'),('2','14 dager'),('3','uke'),
        #   ('4','4 dager'),('5','3 dager'),('6',2 dager'),('7','1 dag')]
        #tabelltype: String [('0','Loenn'),('1','Pensjon')]
        #trekkgrunnlag: Integer
        #andel_av_trekk: Float (halv skatt i desember)
        """
        # def l10n_no_get_tax_deduction(self, context, year=2018, trekkperiode='1',
        #   tabelltype='0', trekkgrunnlag=10000, andel_av_trekk=1):
        _logger.debug("l10n_no_get_tax_deduction")

        trekkprosent = self.l10n_no_trekkprosent / 100.0 or 0.00
        # if trekkprosent:
        #     trekkprosent = float(trekkprosent.value) / 100.0
        # else:
        #     trekkprosent = 0.0

        trekktabell = self.l10n_no_trekktabell
        if trekktabell:
            trekkgrunnlag = int(trekkgrunnlag / 100.0) * 100
            domain = [
                    ("year", "=", year),
                    ("tabellnummer", "=", trekktabell),
                    ("trekkperiode", "=", trekkperiode),
                    ("tabelltype", "=", tabelltype),
                    ("trekkgrunnlag", "=", trekkgrunnlag),
            ]
            _logger.info(f"domain 1: {domain}")
            record = self.env["l10n.no.tabelltrekk"].search(
                domain,
                limit=1,
            )
            if record:
                return -int(int(record.ensure_one().trekk) * andel_av_trekk)
            else:
                domain = [
                        ("year", "=", year),
                        ("tabellnummer", "=", trekktabell),
                        ("trekkperiode", "=", trekkperiode),
                        ("tabelltype", "=", tabelltype),
                ]
                _logger.info(f"domain 2: {domain}")
                record = self.env["l10n.no.tabelltrekk"].search(
                    domain,
                    order="trekkgrunnlag DESC",
                    limit=1,
                )
                if trekkgrunnlag > record.trekkgrunnlag:
                    return -int(
                        (
                            record.trekk
                            + (trekkgrunnlag - record.trekkgrunnlag) * trekkprosent
                        )
                        * andel_av_trekk
                    )
                else:
                    return 0
        else:
            trekk = -int(trekkgrunnlag * trekkprosent * andel_av_trekk)
            return trekk
