# Copyright 2021 AppsToGROW
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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

        record.saft_xml = self._create_xml_generateds(audit_file)

        return {
            "type": "ir.actions.act_window",
            "res_model": "l10n_no_account_saft.xml",
            "res_id": record.id,
            "view_mode": "form",
        }

    def _create_xml_generateds(self, audit_file):
        xml_io = StringIO()
        audit_file.export(xml_io, level=0)
        return xml_io.getvalue()


class AuditFile:
    def __init__(self, saft_record):
        self.company = saft_record.company_id
        self.date_from = saft_record.date_from
        self.date_to = saft_record.date_to

    def AuditFile(self):
        # saft_1_10.py#L1120 AuditFile
        # def export(self, outfile, level, namespaceprefix_='', namespacedef_='
        #  xmlns="urn:StandardAuditFile-Taxation-Financial:NO"
        #  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        #  xsi:schemaLocation="urn:StandardAuditFile-Taxation-Financial:NO
        #  Norwegian_SAF-T_Financial_Schema_v_1.10.xsd" ',
        #  name_='AuditFile', pretty_print=True):
        audit_file = saft.AuditFile()
        audit_file.Header = self.Header()
        audit_file.MasterFiles = self.MasterFiles()
        audit_file.GeneralLedgerEntries = self.GeneralLedgerEntries()
        return audit_file

    def Header(self):
        h = saft.HeaderType()
        h.AuditFileVersion = "1.10"
        h.AuditFileCountry = "NO"
        h.AuditFileDateCreated = datetime.now()
        h.SoftwareCompanyName = "Norske Apps2GROW AS"
        h.SoftwareID = "Odoo"
        h.SoftwareVersion = "14.0"
        h.Company = self.Company()
        h.DefaultCurrencyCode = "NOK"
        h.SelectionCriteria = saft.SelectionCriteriaStructure()
        h.SelectionCriteria.PeriodStart = self.date_from.month
        h.SelectionCriteria.PeriodStartYear = self.date_from.year
        h.SelectionCriteria.PeriodEnd = self.date_to.month
        h.SelectionCriteria.PeriodEndYear = self.date_to.year
        h.HeaderComment = ""
        h.TaxAccountingBasis = "A"
        return h

    def Company(self):
        p = saft.CompanyStructure()
        return self.Partner(p, self.company.partner_id)

    def MasterFiles(self):
        mf = saft.MasterFilesType()
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

        mf.GeneralLedgerAccounts = saft.GeneralLedgerAccountsType()
        for account in self.company.env["account.account"].search([]):
            mf.GeneralLedgerAccounts.add_Account(
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

        mf.Customers = saft.CustomersType()

        for customer in self.company.env["res.partner"].browse(
            [d["partner_id"][0] for d in closing_balance_records]
        ):
            mf.Customers.add_Customer(
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

        mf.Suppliers = saft.SuppliersType()

        for supplier in self.company.env["res.partner"].browse(
            [d["partner_id"][0] for d in closing_balance_records]
        ):
            mf.Suppliers.add_Supplier(
                self.Supplier(
                    supplier,
                    opening_balance.get(supplier.id, 0),
                    closing_balance.get(supplier.id, 0),
                )
            )

        # other

        mf.TaxTable = saft.TaxTableType()
        for tax in self.company.env["account.tax"].search(
            [("type_tax_use", "in", ["sale", "purchase"])]
        ):
            mf.TaxTable.add_TaxTableEntry(self.TaxTableEntry(tax))

        mf.AnalysisTypeTable = saft.AnalysisTypeTableType()
        for analytic in self.company.env["account.analytic.account"].search([]):
            mf.AnalysisTypeTable.add_AnalysisTypeTableEntry(
                self.AnalysisTypeTableEntry(analytic)
            )

        # mf.Owners = saft.OwnersType()
        # for owner in self.company.env[''].browse():
        #     mf.Owners.append(self.Owner(owner))

        return mf

    def Account(self, account, opening_balance, closing_balance):
        a = saft.AccountType()
        a.AccountID = account.code
        a.AccountDescription = account.name
        a.AccountType = "GL"
        a.AccountCreationDate = account.create_date
        set_balance(a, opening_balance, closing_balance)
        return a

    def Customer(self, partner, opening_balance, closing_balance):
        p = saft.CustomerType()
        p.CustomerID = partner.id
        p.AccountID = partner.property_account_receivable_id.code
        set_balance(p, opening_balance, closing_balance)
        return self.Partner(p, partner)

    def Supplier(self, partner, opening_balance, closing_balance):
        p = saft.SupplierType()
        p.SupplierID = partner.id
        p.AccountID = partner.property_account_payable_id.code
        set_balance(p, opening_balance, closing_balance)
        return self.Partner(p, partner)

    def Partner(self, p, partner):
        p.RegistrationNumber = partner.vat and partner.vat[2:] or ""
        p.Name = partner.name  # required
        p.add_Address(self.Address(partner))  # required
        p.add_Contact(self.Contact(partner))
        for child in partner.child_ids:
            if child.type == "contact":
                p.add_Contact(self.Contact(child))
            elif child.zip and child.city:
                p.add_Address(self.Address(child))
        if partner.vat:  # then we assume that the partner is VAT registered
            p.add_TaxRegistration(self.TaxRegistration(partner))
        # p.add_BankAccount(self.BankAccount(partner))
        # p.PartyInfo
        return p

    def Address(self, partner):
        a = saft.AddressStructure()
        if partner.street:
            a.StreetName = partner.street
        if partner.street2:
            a.AdditionalAddressDetail = partner.street2
        a.City = partner.city or "unknown"  # required
        a.PostalCode = partner.zip or "unknown"  # required
        if partner.state_id.name:
            a.Region = partner.state_id.name
        if partner.country_id.code:
            a.Country = partner.country_id.code
        a.AddressType = "PostalAddress"
        return a

    def Contact(self, partner):
        c = saft.ContactInformationStructure()
        c.ContactPerson = saft.PersonNameStructure()
        c.ContactPerson.FirstName = partner.name.split(" ")[0]
        c.ContactPerson.LastName = partner.name.split(" ")[0]
        if len(partner.name.split(" ")) >= 2:
            c.ContactPerson.LastName = partner.name.split(" ")[-1]
        c.Telephone = partner.phone
        c.Email = partner.email
        c.Website = partner.website
        c.MobilePhone = partner.mobile
        return c

    def TaxRegistration(self, partner):
        t = saft.TaxIDStructure()
        t.TaxRegistrationNumber = partner.vat[2:] + "MVA"
        t.TaxAuthority = "Skatteetaten"
        # t.TaxVerificationDate
        # # The date that the tax registration details referred to above were last
        #  checked or when the tax registration was completed in the
        #  VAT register (Merverdiavgiftsregisteret).
        return t

    def BankAccount(self, partner):
        b = saft.BankAccountStructure()
        if partner.bank_ids:
            bank_account = partner.bank_ids[0]
            b.BankAccountNumber = bank_account.acc_number
            b.BIC = bank_account.bank_bic
            b.CurrencyCode = bank_account.currency_id.name
            # b.GeneralLedgerAccountID
        return b

    def PartyInfo(self, partner, partner_type):
        p = saft.PartyInfoStructure()
        p.PaymentTerms = saft.PaymentTermsType()
        # if partner_type == 'customer':
        #     p.PaymentTerms.Days = partner.property_payment_term_id...
        # elif partner_type == 'supplier':
        #     p.PaymentTerms.Days = partner.property_supplier_payment_term_id...
        # p.PaymentTerms.CashDiscountDays = partner.
        # p.PaymentTerms.CashDiscountRate = partner.
        # p.PaymentTerms.FreeBillingMonth = partner.
        # p.NaceCode = '63.110'
        p.CurrencyCode = partner.currency_id.name
        p.Type = "Company" if partner.is_company else "Private"
        p.Status = "Active" if partner.active else "Archived"
        return p

    def TaxTableEntry(self, tax):
        t = saft.TaxTableEntryType()
        t.TaxType = "MVA"
        t.Description = "Merverdiavgift"
        tax_details = tax.children_tax_ids or [tax]
        for tax_detail in tax_details:
            t.add_TaxCodeDetails(
                saft.TaxCodeDetailsType(
                    TaxCode=tax_detail.id,
                    Description=tax_detail.name,
                    TaxPercentage=tax_detail.amount,
                    Country="NO",
                    StandardTaxCode=tax_detail.l10n_no_standard_tax_code,
                    BaseRate=[100],  # TODO
                )
            )
        return t

    def AnalysisTypeTableEntry(self, analytic):
        a = saft.AnalysisTypeTableEntryType()
        a.AnalysisType = str(analytic.plan_id.id)
        a.AnalysisTypeDescription = analytic.plan_id.display_name
        a.AnalysisID = analytic.id
        a.AnalysisIDDescription = analytic.name
        return a

    def Owner(self):
        o = saft.OwnerType()
        return o

    def GeneralLedgerEntries(self):
        e = saft.GeneralLedgerEntriesType()
        e.NumberOfEntries = self.company.env["account.move"].search_count(
            [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        )
        lines = self.company.env["account.move.line"].search(
            [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        )
        e.TotalDebit = decimal_string(sum(line.debit for line in lines))
        e.TotalCredit = decimal_string(sum(line.credit for line in lines))
        for journal in self.company.env["account.journal"].search([]):
            e.add_Journal(self.Journal(journal))
        return e

    def Journal(self, journal):
        j = saft.JournalType()
        j.JournalID = journal.code
        j.Description = journal.name
        j.Type = journal.code  # ?
        for move in self.company.env["account.move"].search(
            [
                ("journal_id", "=", journal.id),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
            ]
        ):
            j.add_Transaction(self.Transaction(move))
        return j

    def Transaction(self, move):
        t = saft.TransactionType()
        t.TransactionID = move.name
        t.Period = int(move.date.strftime("%m"))
        t.PeriodYear = int(move.date.strftime("%Y"))
        t.TransactionDate = move.date
        # t.SourceID = move.
        # t.TransactionType = move.
        t.Description = move.ref
        # t.BatchID = move.
        t.SystemEntryDate = move.create_date
        t.GLPostingDate = move.write_date
        # t.SystemID = move.
        for idx, line in enumerate(move.line_ids):
            t.add_Line(self.Line(idx, line))
        return t

    def Line(self, idx, line):
        l = saft.LineType()
        l.RecordID = idx + 1
        l.AccountID = line.account_id.code
        if line.analytic_distribution:
            for analytic_id, percent in line.analytic_distribution.items():
                analytic = line.env["account.analytic.account"].browse(int(analytic_id))
                l.add_Analysis(
                    saft.AnalysisStructure(
                        AnalysisType=str(analytic.plan_id.id),
                        AnalysisID=str(analytic.id),
                        AnalysisAmount=line.balance * percent / 100.0,
                    )
                )
        l.ValueDate = line.move_id.date
        # l.SourceDocumentID
        l.Description = line.name or ""
        if line.partner_id:
            l.Description = "{} (partner: {})".format(
                l.Description, line.partner_id.name
            ).strip()
        if line.debit:
            l.DebitAmount = saft.AmountStructure(Amount=line.debit)
        else:  # required with debit or credit
            l.CreditAmount = saft.AmountStructure(Amount=line.credit)
        for tax in line.tax_ids:
            l.add_TaxInformation(self.TaxInformation(line, tax))
        # l.ReferenceNumber
        # l.CID
        l.SystemEntryTime = datetime.now()
        # l.ownerID
        return l

    def TaxInformation(self, line, tax):
        t = saft.TaxInformationStructure()
        t.TaxType = "MVA"
        # t.TaxCode
        t.TaxPercentage = int(tax.amount)
        t.TaxBase = line.debit + line.credit
        t.TaxAmount = saft.AmountStructure(
            Amount=decimal_string(t.TaxBase * tax.amount / 100)
        )
        return t
