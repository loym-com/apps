# Copyright 2021 AppsToGROW
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

import base64
import calendar
from datetime import datetime
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from . import saft_1_10 as saft


def decimal_string(myfloat):
    return "{:.2f}".format(myfloat)


def set_balance(obj, opening_balance, closing_balance):
    if opening_balance >= 0:
        obj.OpeningDebitBalance = decimal_string(opening_balance)
    else:
        obj.OpeningCreditBalance = decimal_string(-opening_balance)
    if closing_balance >= 0:
        obj.ClosingDebitBalance = decimal_string(closing_balance)
    else:
        obj.ClosingCreditBalance = decimal_string(-closing_balance)
    return obj


class Company(models.Model):
    _inherit = "res.company"

    l10n_no_partner_saft_id = fields.Many2one("res.partner", "SAF-T Contact Person")


class Tax(models.Model):
    _inherit = "account.tax"

    l10n_no_standard_tax_code = fields.Selection(
        [
            ("0", "0 No VAT treatment"),
            ("1", "1 Input VAT deductible (domestic) - Regular rate"),
            ("3", "3 Output VAT - Regular rate"),
            ("5", "5 No output VAT - Zero rate"),
            (
                "6",
                "6 Not liable to VAT treatment, "
                    "turnover outside the scope of the VAT legislation",
            ),
            ("7", "7 No VAT treatment - no turnover according to the VAT legislation"),
            ("11", "11 Input VAT deductible (domestic) - Reduced rate, middle"),
            ("12", "12 Input VAT deductible (domestic) - Reduced rate, raw fish"),
            ("13", "13 Input VAT deductible (domestic) - Reduced rate, low"),
            ("14", "14 Input VAT deductible (payed on import) - Regular rate"),
            ("15", "15 Input VAT deductible (payed on import) - Reduced rate, middle"),
            ("20", "20 No VAT treatment"),
            ("21", "21 Basis on import of goods - Regular rate"),
            ("22", "22 Basis on import of goods - Reduced rate, middle"),
            ("31", "31 Output VAT - Reduced rate, middle"),
            ("32", "32 Output VAT - Reduced rate, raw fish"),
            ("33", "33 Output VAT - Reduced rate, low"),
            ("51", "51 Domestic sales of reverce charge /VAT obligation - Zero rate"),
            ("52", "52 Export of goods and services - Zero rate"),
            ("81", "81 Importation of goods, VAT deductible - Regular rate"),
            ("82", "82 Importation of goods, without deduction of VAT - Regular rate"),
            ("83", "83 Importation of goods, VAT deductible - Reduced rate, middle"),
            (
                "84",
                "84 Importation of goods, without deduction of VAT - Reduced rate, middle",
            ),
            ("85", "85 Importation of goods, not applicable for VAT - Zero rate"),
            ("86", "86 Services purchased from abroad, VAT deductible - Regular rate"),
            (
                "87",
                "87 Services purchased from abroad, without deduction of VAT - Regular rate",
            ),
            (
                "88",
                "88 Services purchased from abroad, VAT deductible - Reduced rate, low",
            ),
            (
                "89",
                "89 Services purchased from abroad, "
                    "without deduction of VAT - Reduced rate, low",
            ),
            (
                "91",
                "91 Purchase of emissions trading or gold, VAT deductible - Regular rate",
            ),
            (
                "92",
                "92 Purchase of emissions trading or gold, "
                    "without deduction of VAT - Regular rate",
            ),
        ],
        "Standard Tax Code",
    )


# TODO The wizard should download the SAF-T XML file directly. Then this class may be deleted.
class Saft(models.Model):
    _name = "l10n_no_account_saft.xml"
    _description = "l10n_no_account_saft.xml"

    @api.depends("month_from", "month_to")
    def _compute_saft_filename(self):
        self.ensure_one()

        name = "SAF-T from {month_from} to {month_to}.xml".format(
            month_from=self.month_from, month_to=self.month_to
        )
        self.saft_filename = name

    @api.depends("saft_xml")
    def _compute_saft_binary(self):
        self.saft_binary = base64.b64encode(bytes(self.saft_xml, "utf-8"))
        # pass

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        store=True,
        index=True,
        default=lambda self: self.env.company,
    )
    month_from = fields.Char()
    month_to = fields.Char()
    date_from = fields.Date()
    date_to = fields.Date()
    timestamp = fields.Datetime(readonly=True)
    saft_xml = fields.Text(readonly=True)
    saft_filename = fields.Char(compute=_compute_saft_filename)
    saft_binary = fields.Binary(compute=_compute_saft_binary, string="SAF-T Binary")


class SaftWizard(models.TransientModel):
    _name = "l10n_no_account_saft.xml.wizard"
    _description = "l10n_no_account_saft.xml.wizard"

    month_from = fields.Char()
    month_to = fields.Char()

    def create_xml(self):
        # Verify periods
        try:
            date_from = datetime.strptime(self.month_from + "-01", "%Y-%m-%d")
            year = int(self.month_to[:4])
            month = int(self.month_to[-2:])
            date = calendar.monthrange(year, month)[1]
            date_to = datetime.strptime(self.month_to + "-" + str(date), "%Y-%m-%d")
        except:
            raise UserError(_("The period should have this format: yyyy-mm"))

        # Create record with xml
        d = {
            "month_from": self.month_from,
            "month_to": self.month_to,
            "date_from": date_from,
            "date_to": date_to,
        }
        record = self.env["l10n_no_account_saft.xml"].create(d)
        audit_file_class = AuditFile(record)
        audit_file = audit_file_class.AuditFile()

        config = SerializerConfig(indent="  ")
        serializer = XmlSerializer(config=config)
        record.saft_xml = serializer.render(audit_file)

        return {
            "type": "ir.actions.act_window",
            "res_model": "l10n_no_account_saft.xml",
            "res_id": record.id,
            "view_mode": "form",
        }

class AuditFile:
    def __init__(self, saft_record):
        self.company = saft_record.company_id
        self.date_from = saft_record.date_from
        self.date_to = saft_record.date_to

    def AuditFile(self):
        audit_file = saft.AuditFile()
        audit_file.header = self.Header()
        audit_file.master_files = self.MasterFiles()
        audit_file.general_ledger_entries = self.GeneralLedgerEntries()
        return audit_file

    def Header(self):
        h = saft.HeaderStructure()
        h.audit_file_version = "1.10"
        h.audit_file_country = "NO"
        h.audit_file_date_created = datetime.now().strftime("%Y-%m-%d")
        h.software_company_name = "Norske Apps2GROW AS"
        h.software_id = "Odoo"
        h.software_version = "14.0"
        h.company = self.Company()
        h.default_currency_code = "NOK"
        h.selection_criteria = saft.SelectionCriteriaStructure()
        h.selection_criteria.period_start = self.date_from.month
        h.selection_criteria.period_start_year = self.date_from.year
        h.selection_criteria.period_end = self.date_to.month
        h.selection_criteria.period_end_year = self.date_to.year
        h.header_comment = ""
        # h.tax_accounting_basis = "A"
        return h

    def Company(self):
        p = saft.CompanyStructure()
        return self.Partner(p, self.company.partner_id)

    def MasterFiles(self):
        mf = saft.AuditFile.MasterFiles()
        Line = self.company.env["account.move.line"]

        # accounts

        balance_accounts = self.company.env["account.account"].search(
            [("internal_group", "in", ["asset", "equity", "liability"])]
        )

        opening_balance_records = Line.read_group(
            domain=[
                ("date", "<", self.date_from),
                ("account_id", "!=", False),
                ("account_id", "in", balance_accounts.ids),
            ],
            fields=["account_id", "balance"],
            groupby=["account_id"],
        )
        opening_balance = {
            r["account_id"][0]: r["balance"] for r in opening_balance_records
        }
        closing_balance_records = Line.read_group(
            domain=[
                ("account_id", "!=", False),
                ("date", "<=", self.date_to),
                "|",
                ("date", ">=", self.date_from), # profit/loss account types
                ("account_id", "in", balance_accounts.ids),
            ],
            fields=["account_id", "balance"],
            groupby=["account_id"],
        )
        closing_balance = {
            r["account_id"][0]: r["balance"] for r in closing_balance_records
        }

        mf.general_ledger_accounts = saft.AuditFile.MasterFiles.GeneralLedgerAccounts()
        for account in self.company.env["account.account"].search([]):
            mf.general_ledger_accounts.account.append(
                self.Account(
                    account,
                    opening_balance.get(account.id, 0),
                    closing_balance.get(account.id, 0),
                )
            )

        # customers

        receivable_accounts = self.company.env["account.account"].search(
            [("account_type", "=", "asset_receivable")]
        )
        opening_balance_records = Line.read_group(
            domain=[
                ("date", "<", self.date_from),
                ("account_id", "in", [r.id for r in receivable_accounts]),
                ("partner_id", "!=", None),
            ],
            fields=["partner_id", "balance"],
            groupby=["partner_id"],
        )
        opening_balance = {
            r["partner_id"][0]: r["balance"] for r in opening_balance_records
        }
        closing_balance_records = Line.read_group(
            domain=[
                ("date", "<=", self.date_to),
                ("account_id", "in", [r.id for r in receivable_accounts]),
                ("partner_id", "!=", None),
            ],
            fields=["partner_id", "balance"],
            groupby=["partner_id"],
        )
        closing_balance = {
            r["partner_id"][0]: r["balance"] for r in closing_balance_records
        }

        mf.customers = saft.AuditFile.MasterFiles.Customers()

        for customer in self.company.env["res.partner"].browse(
            [d["partner_id"][0] for d in closing_balance_records]
        ):
            mf.customers.customer.append(
                self.Customer(
                    customer,
                    opening_balance.get(customer.id, 0),
                    closing_balance.get(customer.id, 0),
                )
            )

        # suppliers

        payable_accounts = self.company.env["account.account"].search(
            [("account_type", "=", "asset_payable")]
        )
        opening_balance_records = Line.read_group(
            domain=[
                ("date", "<", self.date_from),
                ("account_id", "in", [r.id for r in payable_accounts]),
                ("partner_id", "!=", None),
            ],
            fields=["partner_id", "balance"],
            groupby=["partner_id"],
        )
        opening_balance = {
            r["partner_id"][0]: r["balance"] for r in opening_balance_records
        }
        closing_balance_records = Line.read_group(
            domain=[
                ("date", "<=", self.date_to),
                ("account_id", "in", [r.id for r in payable_accounts]),
                ("partner_id", "!=", None),
            ],
            fields=["partner_id", "balance"],
            groupby=["partner_id"],
        )
        closing_balance = {
            r["partner_id"][0]: r["balance"] for r in closing_balance_records
        }

        mf.suppliers = saft.AuditFile.MasterFiles.Suppliers()

        for supplier in self.company.env["res.partner"].browse(
            [d["partner_id"][0] for d in closing_balance_records]
        ):
            mf.suppliers.supplier.append(
                self.Supplier(
                    supplier,
                    opening_balance.get(supplier.id, 0),
                    closing_balance.get(supplier.id, 0),
                )
            )

        # other

        mf.tax_table = saft.AuditFile.MasterFiles.TaxTable()
        for tax in self.company.env["account.tax"].search(
            [("type_tax_use", "in", ["sale", "purchase"])]
        ):
            mf.tax_table.tax_table_entry.append(self.TaxTableEntry(tax))

        mf.AnalysisTypeTable = saft.AuditFile.MasterFiles.AnalysisTypeTable()
        for analytic in self.company.env["account.analytic.account"].search([]):
            mf.AnalysisTypeTable.analysis_type_table_entry.append(
                self.AnalysisTypeTableEntry(analytic)
            )

        # mf.owners = saft.AuditFile.MasterFiles.Owners()
        # for owner in self.company.env[''].browse():
        #     mf.owners.append(self.Owner(owner))

        return mf

    def Account(self, account, opening_balance, closing_balance):
        a = saft.AuditFile.MasterFiles.GeneralLedgerAccounts.Account()
        a.account_id = account.code
        a.account_description = account.name
        a.account_type = "GL"
        a.account_creation_date = account.create_date.strftime("%Y-%m-%d")
        set_balance(a, opening_balance, closing_balance)
        return a

    def Customer(self, partner, opening_balance, closing_balance):
        p = saft.AuditFile.MasterFiles.Customers.Customer()
        p.customer_id = partner.id
        p.account_id = partner.property_account_receivable_id.code
        set_balance(p, opening_balance, closing_balance)
        return self.Partner(p, partner)

    def Supplier(self, partner, opening_balance, closing_balance):
        p = saft.AuditFile.MasterFiles.Suppliers.Supplier()
        p.supplier_id = partner.id
        p.account_id = partner.property_account_payable_id.code
        set_balance(p, opening_balance, closing_balance)
        return self.Partner(p, partner)

    def Partner(self, p, partner):
        p.registration_number = partner.vat and partner.vat[2:] or ""
        p.name = partner.name  # required
        p.address.append(self.Address(partner))  # required
        p.contact.append(self.Contact(partner))
        for child in partner.child_ids:
            if child.type == "contact":
                p.contact.append(self.Contact(child))
            elif child.zip and child.city:
                p.address.append(self.Address(child))
        if partner.vat:  # then we assume that the partner is VAT registered
            p.tax_registration.append(self.TaxRegistration(partner))
        # p.bank_account.append(self.BankAccount(partner))
        # p.PartyInfo
        return p

    def Address(self, partner):
        a = saft.AddressStructure()
        if partner.street:
            a.street_name = partner.street
        if partner.street2:
            a.additional_address_detail = partner.street2
        a.city = partner.city or "unknown"  # required
        a.postal_code = partner.zip or "unknown"  # required
        if partner.state_id.name:
            a.region = partner.state_id.name
        if partner.country_id.code:
            a.country = partner.country_id.code
        a.address_type = "PostalAddress"
        return a

    def Contact(self, partner):
        c = saft.ContactInformationStructure()
        c.contact_person = saft.PersonNameStructure()
        c.contact_person.first_name = partner.name.split(" ")[0]
        c.contact_person.last_name = partner.name.split(" ")[0]
        if len(partner.name.split(" ")) >= 2:
            c.contact_person.last_name = partner.name.split(" ")[-1]
        c.telephone = partner.phone
        c.email = partner.email
        c.website = partner.website
        c.mobile_phone = partner.mobile
        return c

    def TaxRegistration(self, partner):
        t = saft.TaxIdstructure()
        t.tax_registration_number = partner.vat[2:] + "MVA"
        t.tax_authority = "Skatteetaten"
        # t.TaxVerificationDate
        # # The date that the tax registration details referred to above were last
        #  checked or when the tax registration was completed in the
        #  VAT register (Merverdiavgiftsregisteret).
        return t

    def BankAccount(self, partner):
        b = saft.BankAccountStructure()
        if partner.bank_ids:
            bank_account = partner.bank_ids[0]
            b.bank_account_number = bank_account.acc_number
            b.bic = bank_account.bank_bic
            b.currency_code = bank_account.currency_id.name
            # b.general_ledger_account_id
        return b

    def PartyInfo(self, partner, partner_type):
        p = saft.PartyInfoStructure()
        p.payment_terms = saft.PartyInfoStructure.PaymentTerms()
        # if partner_type == 'customer':
        #     p.payment_terms.days = partner.property_payment_term_id...
        # elif partner_type == 'supplier':
        #     p.payment_terms.days = partner.property_supplier_payment_term_id...
        # p.payment_terms.cash_discount_days = partner.
        # p.payment_terms.cash_discount_rate = partner.
        # p.payment_terms.free_billing_month = partner.
        # p.nace_code = '63.110'
        p.currency_code = partner.currency_id.name
        p.type_value = "Company" if partner.is_company else "Private"
        p.status = "Active" if partner.active else "Archived"
        return p

    def TaxTableEntry(self, tax):
        t = saft.AuditFile.MasterFiles.TaxTable.TaxTableEntry()
        t.tax_type = "MVA"
        t.description = "Merverdiavgift"
        tax_details = tax.children_tax_ids or [tax]
        for tax_detail in tax_details:
            t.tax_code_details.append(self.TaxCodeDetails(tax_detail))
        return t

    def TaxCodeDetails(self, tax_detail):
        d = saft.AuditFile.MasterFiles.TaxTable.TaxTableEntry.TaxCodeDetails()
        d.tax_code = tax_detail.id
        d.description = tax_detail.name
        d.tax_percentage = tax_detail.amount
        d.country = "NO"
        d.standard_tax_code = tax_detail.l10n_no_standard_tax_code
        d.base_rate = [100]  # TODO

    def AnalysisTypeTableEntry(self, analytic):
        a = saft.AuditFile.MasterFiles.AnalysisTypeTable.AnalysisTypeTableEntry()
        a.analysis_type = str(analytic.plan_id.id)
        a.analysis_type_description = analytic.plan_id.display_name
        a.analysis_id = analytic.id
        a.analysis_iddescription = analytic.name
        return a

    def Owner(self):
        o = saft.AuditFile.MasterFiles.Owners.Owner()
        return o

    def GeneralLedgerEntries(self):
        e = saft.AuditFile.GeneralLedgerEntries()
        e.number_of_entries = self.company.env["account.move"].search_count(
            [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        )
        lines = self.company.env["account.move.line"].search(
            [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        )
        e.total_debit = decimal_string(sum(line.debit for line in lines))
        e.total_credit = decimal_string(sum(line.credit for line in lines))
        for journal in self.company.env["account.journal"].search([]):
            e.journal.append(self.Journal(journal))
        return e

    def Journal(self, journal):
        j = saft.AuditFile.GeneralLedgerEntries.Journal()
        j.journal_id = journal.code
        j.description = journal.name
        j.type_value = journal.code  # ?
        for move in self.company.env["account.move"].search(
            [
                ("journal_id", "=", journal.id),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
            ]
        ):
            j.transaction.append(self.Transaction(move))
        return j

    def Transaction(self, move):
        t = saft.AuditFile.GeneralLedgerEntries.Journal.Transaction()
        t.transaction_id = move.name
        t.period = int(move.date.strftime("%m"))
        t.period_year = int(move.date.strftime("%Y"))
        t.transaction_date = move.date.strftime("%Y-%m-%d")
        # t.source_id = move.
        # t.transaction_type = move.
        t.description = move.ref
        # t.batch_id = move.
        t.system_entry_date = move.create_date.strftime("%Y-%m-%d")
        t.glposting_date = move.write_date.strftime("%Y-%m-%d")
        # t.system_id = move.
        for idx, line in enumerate(move.line_ids):
            t.line.append(self.Line(idx, line))
        return t

    def Line(self, idx, line):
        l = saft.AuditFile.GeneralLedgerEntries.Journal.Transaction.Line()
        l.record_id = idx + 1
        l.account_id = line.account_id.code
        if line.analytic_distribution:
            for analytic_id, percent in line.analytic_distribution.items():
                analytic = line.env["account.analytic.account"].browse(int(analytic_id))
                a = saft.AnalysisStructure()
                a.analysis_type = str(analytic.plan_id.id)
                a.analysis_id = str(analytic.id)
                a.analysis_amount = decimal_string(line.balance * percent / 100)
                l.analysis.append(a)
        l.value_date = line.move_id.date.strftime("%Y-%m-%d")
        # l.source_document_id
        l.description = line.name or ""
        if line.partner_id:
            l.description = "{} (partner: {})".format(
                l.description, line.partner_id.name
            ).strip()
        if line.debit:
            l.DebitAmount = self.AmountStructure(amount=line.debit)
        else:  # required with debit or credit
            l.CreditAmount = self.AmountStructure(amount=line.credit)
        for tax in line.tax_ids:
            l.tax_information.append(self.TaxInformation(line, tax))
        # l.reference_number
        # l.cid
        l.system_entry_time = datetime.now().strftime("%Y-%m-%d")
        # l.owner_id
        return l

    def TaxInformation(self, line, tax):
        t = saft.TaxInformationStructure()
        t.tax_type = "MVA"
        # t.tax_code
        t.tax_percentage = int(tax.amount)
        t.tax_base = line.debit + line.credit
        t.tax_amount = self.AmountStructure(
            amount=decimal_string(t.tax_base * tax.amount / 100)
        )
        return t

    def AmountStructure(self, amount):
        a = saft.AmountStructure()
        a.amount = amount
        return a
