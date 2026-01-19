# Copyright 2021 AppsToGROW
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
from datetime import datetime
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from . import gavefrivilligorganisasjon_2_0 as gave


class DonationWizard(models.TransientModel):
    _name = "l10n_no_donation.xml.wizard"
    _description = "Donation XML Wizard"

    @api.depends("year")
    def _compute_donation_filename(self):
        for wizard in self:
            wizard.donation_filename = (
                f"Skattefradrag_{wizard.year}.xml" if wizard.year else False
            )

    @api.depends("donation_xml")
    def _compute_donation_binary(self):
        for wizard in self:
            if wizard.donation_xml:
                wizard.donation_binary = base64.b64encode(
                    wizard.donation_xml.encode("utf-8")
                )
            else:
                wizard.donation_binary = False

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        store=True,
        index=True,
        default=lambda self: self.env.company,
    )
    year = fields.Integer(
        default=lambda self: datetime.now().year - 1,
        string="Year",
        required=True,
    )
    donation_xml = fields.Text(readonly=True)
    donation_filename = fields.Char(compute=_compute_donation_filename)
    donation_binary = fields.Binary(
        compute=_compute_donation_binary, string="Donation Binary"
    )

    def create_xml(self):
        try:
            date_from = datetime.strptime(str(self.year) + "-01-01", "%Y-%m-%d")
            date_to = datetime.strptime(str(self.year) + "-12-31", "%Y-%m-%d")
        except:
            raise UserError(_("The year should have this format: yyyy"))

        donor_data = self.env["donation.tax.receipt"].get_donor_name_personid_total(
            self.company_id, "l10n_no_personid", date_from, date_to, min_total=500
        )
        donor_file = DonorFile(self.env, self.year, donor_data)
        self.donation_xml = self._create_xml_generateds(donor_file.donor_file)

    def _get_donations(self, date_from, date_to):
        id_category = self.env.ref("l10n_no_donation.l10n_no_personid")
        contacts_with_id = self.env["res.partner.id_number"].search(
            [("category_id", "=", id_category.id)]
        ).mapped("partner_id")
        donors = self.env["donation.tax.receipt"].search(
            [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        ).mapped("partner_id")

    def _create_xml_generateds(self, donor_file):
        xml_io = StringIO()
        donor_file.export(xml_io, level=0)
        return xml_io.getvalue()


class DonorFile:
    def __init__(self, env, year, donor_data):
        self.env = env
        self.year = year
        self.donor_data = donor_data # list of dicts: donor, name, personid, total
        self.donor_file = self.DonorFile()

    def DonorFile(self):
        # gavefrivilligorganisasjon_2_0.py#L1136 Melding
        # def export(self, outfile, level, namespaceprefix_='',
        # namespacedef_='xmlns="urn:ske:fastsetting:innsamling:gavefrivilligorganisasjon:v2"
        # xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        # xsi:schemaLocation="urn:ske:fastsetting:innsamling:gavefrivilligorganisasjon:v2
        # gavefrivilligorganisasjon_v2_0.xsd"', name_='melding', pretty_print=True):
        donation_file = gave.Melding()
        donation_file.add_leveranse(self.Leveranse())
        return donation_file

    def Leveranse(self):
        l = gave.Leveranse()
        l.kildesystem = "Odoo 16.0"
        l.oppgavegiver = self.Oppgavegiver()
        l.inntektsaar = self.year
        # TODO: unique reference
        l.oppgavegiversLeveranseReferanse = "unik_referanse"
        # TODO: select 'ordinaer' or 'ingenoppgaver'
        l.leveransetype = "ordinaer"
        # Donation statistics
        count = 0
        total = 0
        # Filter donors with personal id number

        for donor in self.donor_data:
            l.add_oppgave(self.Oppgave(donor))
            count += 1
            total += int(donor['total'])
        l.oppgaveoppsummering = gave.Oppgaveoppsummering()
        l.oppgaveoppsummering.antallOppgaver = count
        l.oppgaveoppsummering.sumBeloep = total
        return l

    def Oppgavegiver(self):
        og = gave.Oppgavegiver()
        og.organisasjonsnummer = self.env.company.vat
        og.organisasjonsnavn = self.env.company.name
        og.kontaktinformasjon = self.Kontaktinformasjon()
        return og

    def Kontaktinformasjon(self):
        k = gave.Kontaktinformasjon()
        # TODO: error handling if partner is missing
        partner = self.env.company.l10n_no_donation_partner_id
        k.navn = partner.name
        k.telefonnummer = partner.phone
        k.varselEpostadresse = partner.email
        k.varselSmsMobilnummer = partner.mobile
        return k

    def Oppgave(self, donor):
        o = gave.OppgaveGave()
        o.oppgaveeier = self.Oppgaveeier(donor)
        # TODO: compute the total donation
        o.beloep = int(donor['total'])
        return o

    def Oppgaveeier(self, donor):
        oe = gave.Oppgaveeier()
        # TODO: error handling
        oe.foedselsnummer = donor['personid']
        oe.navn = donor['name']
        return oe
