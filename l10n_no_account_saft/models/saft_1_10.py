from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any, List, Optional

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime

__NAMESPACE__ = "urn:StandardAuditFile-Taxation-Financial:NO"




class AccountAccountType(Enum):
    GL = "GL"


class AddressStructureAddressType(Enum):
    STREET_ADDRESS = "StreetAddress"
    POSTAL_ADDRESS = "PostalAddress"
    BILLING_ADDRESS = "BillingAddress"
    SHIP_TO_ADDRESS = "ShipToAddress"
    SHIP_FROM_ADDRESS = "ShipFromAddress"


@dataclass
class AmountStructure:
    """A common structure used wherever an amount is required.

    Monetary amount with optional foreign currency exchange rate
    information.

    :ivar amount: Amount in the header’s default currency.
    :ivar currency_code: Three-letter currency code according to ISO
        4217 standard. Required if CurrencyAmount is used.
    :ivar currency_amount: Amount in foreign currency. Required if
        CurrencyCode is used.
    :ivar exchange_rate: The exchange rate used. CurrencyAmount x
        ExchangeRate = Amount
    """

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 2,
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "length": 3,
        },
    )
    currency_amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CurrencyAmount",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "total_digits": 18,
            "fraction_digits": 2,
        },
    )
    exchange_rate: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "ExchangeRate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "total_digits": 18,
            "fraction_digits": 8,
        },
    )


class AnalysisTypeTableEntryStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    OBSERVATION = "Observation"
    PASSIVE = "Passive"


@dataclass
class BankAccountStructure:
    """Bank account number information.

    IBAN number, or account number with optional information.

    :ivar ibannumber: International Bank Account Number, ISO 13616
    :ivar bank_account_number: The number allocated to the account by
        the individual’s or company’s own bank.
    :ivar bank_account_name: The name of the individual or company
        holding the bank account.
    :ivar sort_code: Identifier for the bank branch at which the account
        is held. May be needed to uniquely identify the account. Also
        known as ABA Number or National Bank Code
    :ivar bic: Bank Identifier Code.
    :ivar currency_code: Currency Code for the Bank Account from ISO
        4217.
    :ivar general_ledger_account_id: Link to a General Ledger account.
    """

    ibannumber: Optional[str] = field(
        default=None,
        metadata={
            "name": "IBANNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    bank_account_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "BankAccountNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    bank_account_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "BankAccountName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    sort_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "SortCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    bic: Optional[str] = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "length": 3,
        },
    )
    general_ledger_account_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "GeneralLedgerAccountID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )


class HeaderTaxAccountingBasis(Enum):
    A = "A"


class LineDebitCreditIndicator(Enum):
    D = "D"
    C = "C"


class PartyInfoStructureStatus(Enum):
    ACTIVE = "Active"
    OBSERVATION = "Observation"
    PASSIVE = "Passive"


class PartyInfoStructureType(Enum):
    PRIVATE = "Private"
    COMPANY = "Company"
    GOVERNMENT = "Government"


@dataclass
class PersonNameStructure:
    """
    All information about the name of a natural person.

    :ivar title: Not in use.
    :ivar first_name: First name of the person. If the name of the
        person is in an unstructured form, insert “NotUsed” in this
        element and enter the full unstructured name in the LastName
        element.
    :ivar initials: Initials.
    :ivar last_name_prefix: A textual expression of a prefix that
        precedes this person's family name such as Van, Von.
    :ivar last_name: Last name of the person. If the FirstName element
        has the text “NotUsed” then this element should contain the full
        unstructured name of the person.
    :ivar birth_name: Birth name of the person.
    :ivar salutation: A formal sign or expression of greeting, expressed
        as text, that is appropriate for this person such as Right
        Honourable, Monsignor or Madam.
    :ivar other_titles: Used for roles in the company, such as Daglig
        leder, Styreleder, Regnskapsfører, etc.
    """

    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 9,
        },
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 35,
        },
    )
    initials: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initials",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    last_name_prefix: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastNamePrefix",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 70,
        },
    )
    birth_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "BirthName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    salutation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salutation",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    other_titles: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OtherTitles",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )


@dataclass
class SelectionCriteriaStructure:
    """
    The selection criteria used to generate this Standard Auditfile.

    :ivar tax_reporting_jurisdiction: Identifies the tax jurisdiction
        for whose purpose the SAF has been created. Principally for use
        where a single Revenue body covers more than one territory.
    :ivar company_entity: For use where data has been extracted from the
        full data set by reference to a specific corporate entity.
    :ivar selection_start_date: The start date for the reporting period
        covered by the SAF.
    :ivar selection_end_date: The end date for the reporting period
        covered by the SAF.
    :ivar period_start: The first Accounting Period covered by the SAF.
    :ivar period_start_year: The Accounting Year in which the
        PeriodStart falls.
    :ivar period_end: The last Accounting Period covered by the SAF.
    :ivar period_end_year: The Accounting Year in which the PeriodEnd
        falls.
    :ivar document_type: Type of documents selected. For use where the
        data has been restricted by reference to particular transaction
        types.
    :ivar other_criteria: Any other criteria used in selecting data.
        Individual Revenue Bodies may wish to draw up a list of other
        acceptable selection criteria for use within their jurisdiction.
    """

    tax_reporting_jurisdiction: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxReportingJurisdiction",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    company_entity: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyEntity",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    selection_start_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "SelectionStartDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    selection_end_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "SelectionEndDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    period_start: Optional[int] = field(
        default=None,
        metadata={
            "name": "PeriodStart",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    period_start_year: Optional[int] = field(
        default=None,
        metadata={
            "name": "PeriodStartYear",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_inclusive": 1970,
            "max_inclusive": 2100,
        },
    )
    period_end: Optional[int] = field(
        default=None,
        metadata={
            "name": "PeriodEnd",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    period_end_year: Optional[int] = field(
        default=None,
        metadata={
            "name": "PeriodEndYear",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_inclusive": 1970,
            "max_inclusive": 2100,
        },
    )
    document_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocumentType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 256,
        },
    )
    other_criteria: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OtherCriteria",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 256,
        },
    )


class TaxIdstructureTaxAuthority(Enum):
    SKATTEETATEN = "Skatteetaten"


class TaxInformationStructureTaxType(Enum):
    MVA = "MVA"


class TaxTableEntryDescription(Enum):
    MERVERDIAVGIFT = "Merverdiavgift"


class TaxTableEntryTaxType(Enum):
    MVA = "MVA"


@dataclass
class AddressStructure:
    """
    A common structure used wherever an address is required.

    :ivar street_name: Address line 1. Normally street name or post box.
        Can also include house number.
    :ivar number: Address line 1. House number if available.
    :ivar additional_address_detail: Address line 2.
    :ivar building: Not in use
    :ivar city: Name of the city/post district.
    :ivar postal_code: Postal code for the relevant city/post district.
    :ivar region: Country specific code to indicate regions / provinces
        within the tax authority.
    :ivar country: Two-letter country code according to ISO 3166-1 alpha
        2 standard.
    :ivar address_type: Field to differentiate between multiple
        addresses and to indicate the type of address. Choose from the
        predefined enumerations: StreetAddress, PostalAddress,
        BillingAddress, ShipToAddress, ShipFromAddress.
    """

    street_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "StreetName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    additional_address_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "AdditionalAddressDetail",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    building: Optional[str] = field(
        default=None,
        metadata={
            "name": "Building",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    postal_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    region: Optional[str] = field(
        default=None,
        metadata={
            "name": "Region",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "length": 2,
        },
    )
    address_type: Optional[AddressStructureAddressType] = field(
        default=None,
        metadata={
            "name": "AddressType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )


@dataclass
class AnalysisStructure:
    """
    General Ledger analysis codes.

    :ivar analysis_type: Analysis type identifier/code for the dimension
        type (e.g. departments, projects, journal types, cost centers,
        etc.)
    :ivar analysis_id: Analysis ID of the specific dimension.
    :ivar analysis_amount: Amount applying to the Analysis: f.i. the
        amount applying for this dimension.
    """

    analysis_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnalysisType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 9,
        },
    )
    analysis_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnalysisID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 256,
        },
    )
    analysis_amount: Optional[AmountStructure] = field(
        default=None,
        metadata={
            "name": "AnalysisAmount",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )


@dataclass
class ContactInformationStructure:
    """
    Contact information of a company.

    :ivar contact_person: The name of the contact person.
    :ivar telephone: Telephone number.
    :ivar fax: Fax number.
    :ivar email: E-mail address.
    :ivar website: Website address.
    :ivar mobile_phone: The mobile phone number (for SMS messages).
    """

    contact_person: Optional[PersonNameStructure] = field(
        default=None,
        metadata={
            "name": "ContactPerson",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
        },
    )
    telephone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Telephone",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    fax: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fax",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    website: Optional[str] = field(
        default=None,
        metadata={
            "name": "Website",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    mobile_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "MobilePhone",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )


@dataclass
class TaxIdstructure:
    """
    Tax information of a company.

    :ivar tax_registration_number: The company’s VAT (MVA) number. This
        is the unique number/organization number from The Brønnøysund
        Register Centre (Brønnøysundregistrene). This element is
        mandatory if the company is subject to VAT (MVA).
    :ivar tax_type: Not in use.
    :ivar tax_number: Not in use.
    :ivar tax_authority: Identification of the Revenue Body to which
        this TaxType refers. The only valid value is “Skatteetaten ”.
    :ivar tax_verification_date: The date that the tax registration
        details referred to above were last checked or when the tax
        registration was completed in the VAT register
        (Merverdiavgiftsregisteret).
    """

    class Meta:
        name = "TaxIDStructure"

    tax_registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRegistrationNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 35,
        },
    )
    tax_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 9,
        },
    )
    tax_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    tax_authority: Optional[TaxIdstructureTaxAuthority] = field(
        default=None,
        metadata={
            "name": "TaxAuthority",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    tax_verification_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "TaxVerificationDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )


@dataclass
class TaxInformationStructure:
    """
    Tax Amount information structure.

    :ivar tax_type: Tax type for look-up in tables. If used, then the
        only valid value is "MVA".
    :ivar tax_code: Tax Code for lookup in tables.
    :ivar tax_percentage: Tax percentage.
    :ivar country: Two-letter country code according to ISO 3166-1 alpha
        2 standard.
    :ivar tax_base: The base on which the tax is calculated. This can be
        an amount, or a quantity, eg. Litres.
    :ivar tax_base_description: Description of the value in the TaxBase.
        Eg. Litres for excises on alcoholic bevarages.
    :ivar tax_amount: Tax amount information
    :ivar tax_exemption_reason: Tax exemption or reduction reason or
        rationale
    :ivar tax_declaration_period: The identification of the
        declaration/return in which the taxamount is reported to the
        Revenue body.
    """

    tax_type: Optional[TaxInformationStructureTaxType] = field(
        default=None,
        metadata={
            "name": "TaxType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    tax_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    tax_percentage: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxPercentage",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "length": 2,
        },
    )
    tax_base: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TaxBase",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    tax_base_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxBaseDescription",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    tax_amount: Optional[AmountStructure] = field(
        default=None,
        metadata={
            "name": "TaxAmount",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
        },
    )
    tax_exemption_reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxExemptionReason",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    tax_declaration_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxDeclarationPeriod",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )


@dataclass
class AnalysisPartyInfoStructure(AnalysisStructure):
    """
    Analysis structure (restricted) for use in PartyInfoStructure.

    :ivar analysis_amount: Amount applying to the Analysis: f.i. the
        amount applying for this dimension.
    """

    analysis_amount: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class CompanyStructure:
    """
    Name, address, contact and identification information of a company.

    :ivar registration_number: Organization number from The Brønnøysund
        Register Centre (Brønnøysundregistrene) or other relevant
        government authority. In case of private persons, the social
        security number can be used.
    :ivar name: The name of the company.
    :ivar address: Addresses of the company.
    :ivar contact: Contacts of the company.
    :ivar tax_registration: Tax registration of the company.
    :ivar bank_account: Bank accounts of the company.
    """

    registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RegistrationNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 70,
        },
    )
    address: List[AddressStructure] = field(
        default_factory=list,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_occurs": 1,
        },
    )
    contact: List[ContactInformationStructure] = field(
        default_factory=list,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    tax_registration: List[TaxIdstructure] = field(
        default_factory=list,
        metadata={
            "name": "TaxRegistration",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    bank_account: List[BankAccountStructure] = field(
        default_factory=list,
        metadata={
            "name": "BankAccount",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )


@dataclass
class ContactHeaderStructure(ContactInformationStructure):
    """
    ContactInformationStructure with madatory TelephoneNumber.

    :ivar telephone: Telephone number.
    """

    telephone: Optional[str] = field(
        default=None,
        metadata={
            "name": "Telephone",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 18,
        },
    )


@dataclass
class ShippingPointStructure:
    """
    A structure that holds all shipping point information.

    :ivar delivery_id: Identification of the delivery
    :ivar delivery_date: Date goods are delivered
    :ivar warehouse_id: Warehouse where goods held - also to identify
        work-in-progress, or stock-in-transit
    :ivar location_id: Location of goods in warehouse
    :ivar ucr: Unique consignment reference number
    :ivar address:
    """

    delivery_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeliveryID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    delivery_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DeliveryDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    warehouse_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "WarehouseID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    location_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocationID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    ucr: Optional[str] = field(
        default=None,
        metadata={
            "name": "UCR",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    address: Optional[AddressStructure] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )


@dataclass
class CompanyHeaderStructure(CompanyStructure):
    """
    CompanyStructure with mandatory RegistrationNumber and Telephone (Contact).

    :ivar registration_number: Organization number from The Brønnøysund
        Register Centre (Brønnøysundregistrene) or other relevant
        government authority. In case of private persons, the social
        security number can be used.
    :ivar contact: Contacts of the company.
    """

    registration_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RegistrationNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 35,
        },
    )
    contact: List[ContactInformationStructure] = field(
        default_factory=list,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_occurs": 1,
        },
    )


@dataclass
class InvoiceStructure:
    """
    Containing all information about sales invoices and suppliers invoices.

    :ivar invoice_no:
    :ivar customer_info:
    :ivar supplier_info:
    :ivar account_id: General Ledger Account code of the customer /
        supplier. Can be including sub-account id. It can contain many
        different levels to identify the Account. It could include cost
        centres such as company, division, region, group and
        branch/department.
    :ivar branch_store_number: Branch or Storenumber, additional
        segregation of customer/supplier, used if not included as part
        of the customer/supplier id.
    :ivar period: Accounting Period
    :ivar period_year: The year of the Accounting Period.
    :ivar invoice_date:
    :ivar invoice_type: Type of invoice: Debit invoice, Credit invoice,
        Cash, Ticket, etc.
    :ivar ship_to: Ship To details
    :ivar ship_from: Ship from Details
    :ivar payment_terms: Payments terms for this invoice
    :ivar self_billing_indicator: Indicator showing if self-billing  is
        used for this invoice.
    :ivar source_id: Details of person or application that entered the
        transaction
    :ivar glposting_date: Date posting to GL
    :ivar batch_id: Systems generated ID for batch
    :ivar system_id: Unique number created by the system for the
        document
    :ivar transaction_id: Cross-reference to GL posting. It can contain
        many different levels to identify the transaction. It could
        include cost centres such as company, division, region, group
        and branch/department.
    :ivar receipt_numbers: The number(s) of the receipt(s) on this
        "consolidated invoicerecord". Can be a single number, a range or
        a list.
    :ivar line:
    :ivar settlement:
    :ivar document_totals:
    """

    invoice_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "InvoiceNo",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 70,
        },
    )
    customer_info: Optional["InvoiceStructure.CustomerInfo"] = field(
        default=None,
        metadata={
            "name": "CustomerInfo",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    supplier_info: Optional["InvoiceStructure.SupplierInfo"] = field(
        default=None,
        metadata={
            "name": "SupplierInfo",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    account_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    branch_store_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "BranchStoreNumber",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    period: Optional[int] = field(
        default=None,
        metadata={
            "name": "Period",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    period_year: Optional[int] = field(
        default=None,
        metadata={
            "name": "PeriodYear",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_inclusive": 1970,
            "max_inclusive": 2100,
        },
    )
    invoice_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "InvoiceDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
        },
    )
    invoice_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "InvoiceType",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 9,
        },
    )
    ship_to: Optional[ShippingPointStructure] = field(
        default=None,
        metadata={
            "name": "ShipTo",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    ship_from: Optional[ShippingPointStructure] = field(
        default=None,
        metadata={
            "name": "ShipFrom",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    payment_terms: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentTerms",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    self_billing_indicator: Optional[str] = field(
        default=None,
        metadata={
            "name": "SelfBillingIndicator",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 9,
        },
    )
    source_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SourceID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    glposting_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "GLPostingDate",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    batch_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "BatchID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    system_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SystemID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 35,
        },
    )
    transaction_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransactionID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 70,
        },
    )
    receipt_numbers: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReceiptNumbers",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 256,
        },
    )
    line: List["InvoiceStructure.Line"] = field(
        default_factory=list,
        metadata={
            "name": "Line",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "min_occurs": 1,
        },
    )
    settlement: Optional["InvoiceStructure.Settlement"] = field(
        default=None,
        metadata={
            "name": "Settlement",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    document_totals: Optional["InvoiceStructure.DocumentTotals"] = field(
        default=None,
        metadata={
            "name": "DocumentTotals",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )

    @dataclass
    class Line:
        """
        :ivar line_number: Number of the invoiceline
        :ivar account_id: General Ledger Account code of the GL-revenue-
            account. Can be including sub-account id. It can contain
            many different levels to identify the Account. It could
            include cost centres such as company, division, region,
            group and branch/department.
        :ivar analysis: General Ledger analysis codes
        :ivar order_references: Relevant order references
        :ivar ship_to: Ship To details
        :ivar ship_from: Ship from Details
        :ivar goods_services_id: Indicator showing if goods or service
        :ivar product_code: Product code
        :ivar product_description: Description of goods or services.
        :ivar delivery: Information about the date or timeframe of the
            delivery of the goods or services.
        :ivar quantity: Quantity of goods and services supplied.
        :ivar invoice_uom: Quantity unit of measure e.g. pack of 12
        :ivar uomto_uombase_conversion_factor: Conversion factor of the
            InvoiceUOM to UOM Base. Only needed when InvoiceUOM is
            reported and is different from the UOM Base.
        :ivar unit_price: Unit price for the unit/group of units per UOM
            in the header's default currency.
        :ivar tax_point_date: Tax Point date where recorded or if not
            recorded then the Invoice date
        :ivar references: Credit Note references
        :ivar description: Description of Invoice Line.
        :ivar invoice_line_amount: Amount for transaction excluding
            taxes and freightcharges.
        :ivar debit_credit_indicator: Indicates whether the amounts on
            line-level are debit or credit amounts. Entry must
            correspond to entry reflected in General Ledger Entry.
            Signing of lineamounts is relative to this indicator. E.g. a
            return can lead to a negative amount.
        :ivar shipping_costs_amount: Amount for shipping/freight
            charges.
        :ivar tax_information:
        """

        line_number: Optional[str] = field(
            default=None,
            metadata={
                "name": "LineNumber",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 18,
            },
        )
        account_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "AccountID",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 70,
            },
        )
        analysis: List[AnalysisStructure] = field(
            default_factory=list,
            metadata={
                "name": "Analysis",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        order_references: List["InvoiceStructure.Line.OrderReferences"] = (
            field(
                default_factory=list,
                metadata={
                    "name": "OrderReferences",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                },
            )
        )
        ship_to: Optional[ShippingPointStructure] = field(
            default=None,
            metadata={
                "name": "ShipTo",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        ship_from: Optional[ShippingPointStructure] = field(
            default=None,
            metadata={
                "name": "ShipFrom",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        goods_services_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "GoodsServicesID",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 9,
            },
        )
        product_code: Optional[str] = field(
            default=None,
            metadata={
                "name": "ProductCode",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 70,
            },
        )
        product_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "ProductDescription",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 256,
            },
        )
        delivery: Optional["InvoiceStructure.Line.Delivery"] = field(
            default=None,
            metadata={
                "name": "Delivery",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        quantity: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "Quantity",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "total_digits": 22,
                "fraction_digits": 6,
            },
        )
        invoice_uom: Optional[str] = field(
            default=None,
            metadata={
                "name": "InvoiceUOM",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 9,
            },
        )
        uomto_uombase_conversion_factor: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "UOMToUOMBaseConversionFactor",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        unit_price: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "UnitPrice",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )
        tax_point_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "TaxPointDate",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )
        references: Optional["InvoiceStructure.Line.References"] = field(
            default=None,
            metadata={
                "name": "References",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        description: Optional[str] = field(
            default=None,
            metadata={
                "name": "Description",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
                "max_length": 256,
            },
        )
        invoice_line_amount: Optional[AmountStructure] = field(
            default=None,
            metadata={
                "name": "InvoiceLineAmount",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )
        debit_credit_indicator: Optional[LineDebitCreditIndicator] = field(
            default=None,
            metadata={
                "name": "DebitCreditIndicator",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )
        shipping_costs_amount: Optional[AmountStructure] = field(
            default=None,
            metadata={
                "name": "ShippingCostsAmount",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        tax_information: List[TaxInformationStructure] = field(
            default_factory=list,
            metadata={
                "name": "TaxInformation",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )

        @dataclass
        class OrderReferences:
            """
            :ivar originating_on: Origination Order Number
            :ivar order_date: Date of order
            """

            originating_on: Optional[str] = field(
                default=None,
                metadata={
                    "name": "OriginatingON",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                    "max_length": 70,
                },
            )
            order_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "OrderDate",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                },
            )

        @dataclass
        class Delivery:
            """
            :ivar movement_reference: Unique reference to the movement.
            :ivar delivery_date: The date of the delivery
            :ivar delivery_period: Timeframe of the deliveries
            """

            movement_reference: List[str] = field(
                default_factory=list,
                metadata={
                    "name": "MovementReference",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                    "max_length": 35,
                },
            )
            delivery_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "DeliveryDate",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                },
            )
            delivery_period: Optional[
                "InvoiceStructure.Line.Delivery.DeliveryPeriod"
            ] = field(
                default=None,
                metadata={
                    "name": "DeliveryPeriod",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                },
            )

            @dataclass
            class DeliveryPeriod:
                """
                :ivar from_date: Startdate of the deliveries
                :ivar to_date: Enddate of the deliveries
                """

                from_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "FromDate",
                        "type": "Element",
                        "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                        "required": True,
                    },
                )
                to_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "ToDate",
                        "type": "Element",
                        "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                        "required": True,
                    },
                )

        @dataclass
        class References:
            credit_note: Optional[
                "InvoiceStructure.Line.References.CreditNote"
            ] = field(
                default=None,
                metadata={
                    "name": "CreditNote",
                    "type": "Element",
                    "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                },
            )

            @dataclass
            class CreditNote:
                """
                :ivar reference: Credit note reference (where
                    applicable) to original invoice
                :ivar reason: Credit note reason or rationale
                """

                reference: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Reference",
                        "type": "Element",
                        "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                        "max_length": 35,
                    },
                )
                reason: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Reason",
                        "type": "Element",
                        "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                        "max_length": 256,
                    },
                )

    @dataclass
    class Settlement:
        """
        :ivar settlement_discount: Description Settlement / Other
            Discount
        :ivar settlement_amount: Settlement amount
        :ivar settlement_date: Date settled
        :ivar payment_mechanism: Payment mechanism
        """

        settlement_discount: Optional[str] = field(
            default=None,
            metadata={
                "name": "SettlementDiscount",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 35,
            },
        )
        settlement_amount: Optional[AmountStructure] = field(
            default=None,
            metadata={
                "name": "SettlementAmount",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )
        settlement_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "SettlementDate",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        payment_mechanism: Optional[str] = field(
            default=None,
            metadata={
                "name": "PaymentMechanism",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 9,
            },
        )

    @dataclass
    class DocumentTotals:
        """
        :ivar tax_information_totals: Control totals tax payable
            information. Per TaxType/TaxCode the TaxBase and TaxAmount
            are summarised.
        :ivar shipping_costs_amount_total: Control total amount freight
            charges
        :ivar net_total: Control total sales value excluding tax and
            shippingcosts.
        :ivar gross_total: Control total amount including tax and
            shippingcosts.
        """

        tax_information_totals: List[TaxInformationStructure] = field(
            default_factory=list,
            metadata={
                "name": "TaxInformationTotals",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        shipping_costs_amount_total: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "ShippingCostsAmountTotal",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )
        net_total: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "NetTotal",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )
        gross_total: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "GrossTotal",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )

    @dataclass
    class CustomerInfo:
        """
        :ivar customer_id: Unique code for the customer
        :ivar name: Name of the customer
        :ivar billing_address:
        """

        customer_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "CustomerID",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 35,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 70,
            },
        )
        billing_address: Optional[AddressStructure] = field(
            default=None,
            metadata={
                "name": "BillingAddress",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )

    @dataclass
    class SupplierInfo:
        """
        :ivar supplier_id: Unique code for the supplier
        :ivar name: Name of the supplier
        :ivar billing_address:
        """

        supplier_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "SupplierID",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 35,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "max_length": 70,
            },
        )
        billing_address: Optional[AddressStructure] = field(
            default=None,
            metadata={
                "name": "BillingAddress",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "required": True,
            },
        )


@dataclass
class PartyInfoStructure:
    """
    Additional party information.

    :ivar payment_terms: Payment terms of the party.
    :ivar nace_code: NACE (Nomenclature of Economic Activities) is the
        European statistical classification of economic activities.
    :ivar currency_code: Three-letter currency code according to ISO
        4217 standard.
    :ivar type_value: Type of party. Enumerated: Private, Company,
        Government
    :ivar status: Type of account. Enumerated: Active, Observation,
        Passive.
    :ivar analysis: Standard analysis codes for the party, such as
        project, department, cost center, groups, etc.
    :ivar notes: Notes.
    """

    payment_terms: Optional["PartyInfoStructure.PaymentTerms"] = field(
        default=None,
        metadata={
            "name": "PaymentTerms",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    nace_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "NaceCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 18,
        },
    )
    currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "length": 3,
        },
    )
    type_value: Optional[PartyInfoStructureType] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    status: Optional[PartyInfoStructureStatus] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    analysis: List[AnalysisPartyInfoStructure] = field(
        default_factory=list,
        metadata={
            "name": "Analysis",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )

    @dataclass
    class PaymentTerms:
        """
        :ivar days: Days of respite before due date from invoice date.
        :ivar months: Months of respite before due date from invoice
            date.
        :ivar cash_discount_days: Number of days from the invoice date
            the cash discount can be deducted.
        :ivar cash_discount_rate: Rate for calculating cash discount.
        :ivar free_billing_month: Indicator that states whether free
            billing month is used or not. Free billing month sets the
            deadline to the last date of the invoice month.
        """

        days: Optional[int] = field(
            default=None,
            metadata={
                "name": "Days",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        months: Optional[int] = field(
            default=None,
            metadata={
                "name": "Months",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        cash_discount_days: Optional[int] = field(
            default=None,
            metadata={
                "name": "CashDiscountDays",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )
        cash_discount_rate: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "CashDiscountRate",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
                "min_inclusive": Decimal("0.00"),
                "max_inclusive": Decimal("100.00"),
            },
        )
        free_billing_month: Optional[bool] = field(
            default=None,
            metadata={
                "name": "FreeBillingMonth",
                "type": "Element",
                "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            },
        )


@dataclass
class HeaderStructure:
    """
    Overall information about this Standard Auditfile.

    :ivar audit_file_version: Version of standard audit file being used.
        The version number to be used is displayed in an XML annotation
        in top of the XSD schema file.
    :ivar audit_file_country: Two-letter country code according to ISO
        3166-1 alpha 2 standard.
    :ivar audit_file_region: Not in use.
    :ivar audit_file_date_created: Date of production of the audit file.
    :ivar software_company_name: Name of the software company whose
        product created the audit file.
    :ivar software_id: Name of the software that generated the audit
        file.
    :ivar software_version: Version of the software that generated the
        audit file.
    :ivar company: Company's name and address details.
    :ivar default_currency_code: Three letter Currency Code  (ISO 4217)
        of local currency which is the default for the audit file.
    :ivar selection_criteria: Criteria set by the user to populate the
        audit files
    :ivar header_comment: Space for any further generic comments on the
        audit file.
    """

    audit_file_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuditFileVersion",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 9,
        },
    )
    audit_file_country: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuditFileCountry",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "length": 2,
        },
    )
    audit_file_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuditFileRegion",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 9,
        },
    )
    audit_file_date_created: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "AuditFileDateCreated",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
        },
    )
    software_company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SoftwareCompanyName",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 70,
        },
    )
    software_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SoftwareID",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 256,
        },
    )
    software_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "SoftwareVersion",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "max_length": 18,
        },
    )
    company: Optional[CompanyHeaderStructure] = field(
        default=None,
        metadata={
            "name": "Company",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
        },
    )
    default_currency_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefaultCurrencyCode",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "required": True,
            "length": 3,
        },
    )
    selection_criteria: Optional[SelectionCriteriaStructure] = field(
        default=None,
        metadata={
            "name": "SelectionCriteria",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
        },
    )
    header_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "HeaderComment",
            "type": "Element",
            "namespace": "urn:StandardAuditFile-Taxation-Financial:NO",
            "max_length": 256,
        },
    )


@dataclass
class AuditFile:
    """
    Root element of the Norwegian SAF-T file.

    :ivar header: Overall information about this Standard Audit file.
    :ivar master_files: Holds standing data about general ledger
        account, suppliers, customers, products, etc.. An extension
        point is provided to allow Revenue Bodies to specify additional
        elements or structures such as tax rate tables.
    :ivar general_ledger_entries: Accounting transactions.
    :ivar source_documents: Not in use.
    """

    class Meta:
        namespace = "urn:StandardAuditFile-Taxation-Financial:NO"

    header: Optional["AuditFile.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "required": True,
        },
    )
    master_files: Optional["AuditFile.MasterFiles"] = field(
        default=None,
        metadata={
            "name": "MasterFiles",
            "type": "Element",
        },
    )
    general_ledger_entries: Optional["AuditFile.GeneralLedgerEntries"] = field(
        default=None,
        metadata={
            "name": "GeneralLedgerEntries",
            "type": "Element",
        },
    )
    source_documents: Optional["AuditFile.SourceDocuments"] = field(
        default=None,
        metadata={
            "name": "SourceDocuments",
            "type": "Element",
        },
    )

    @dataclass
    class Header(HeaderStructure):
        """
        :ivar tax_accounting_basis: Type of data in the audit file. The
            only valid value is “A” (Accounting).
        :ivar tax_entity: Company / Division / Branch reference
        :ivar user_id: ID of the user that generated the audit file.
        :ivar audit_file_sender: Information about the sender of the
            audit file if the sender is not the company that owns the
            data. This can be an accounting office, a parent company,
            etc.
        """

        tax_accounting_basis: Optional[HeaderTaxAccountingBasis] = field(
            default=None,
            metadata={
                "name": "TaxAccountingBasis",
                "type": "Element",
                "required": True,
            },
        )
        tax_entity: Optional[str] = field(
            default=None,
            metadata={
                "name": "TaxEntity",
                "type": "Element",
                "max_length": 70,
            },
        )
        user_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "UserID",
                "type": "Element",
                "max_length": 35,
            },
        )
        audit_file_sender: Optional[CompanyStructure] = field(
            default=None,
            metadata={
                "name": "AuditFileSender",
                "type": "Element",
            },
        )

    @dataclass
    class MasterFiles:
        """
        :ivar general_ledger_accounts: The general ledger accounts of a
            company.
        :ivar taxonomies: Not in use.
        :ivar customers: The customers of a company.
        :ivar suppliers: The suppliers of a company.
        :ivar tax_table: The tax tables of a company.
        :ivar uomtable: Not in use.
        :ivar analysis_type_table: Table with the analysis code
            identifiers. Used for further specification of transaction
            data. Example: cost unit, cost center, project, department,
            provider, journal type, employees, etc. Journal type
            (bilagsart) should always be used on all transactions.
        :ivar movement_type_table: Not in use.
        :ivar products: Not in use.
        :ivar physical_stock: Not in use.
        :ivar owners: The owners of a company.
        :ivar assets: Not in use.
        """

        general_ledger_accounts: Optional[
            "AuditFile.MasterFiles.GeneralLedgerAccounts"
        ] = field(
            default=None,
            metadata={
                "name": "GeneralLedgerAccounts",
                "type": "Element",
            },
        )
        taxonomies: Optional["AuditFile.MasterFiles.Taxonomies"] = field(
            default=None,
            metadata={
                "name": "Taxonomies",
                "type": "Element",
            },
        )
        customers: Optional["AuditFile.MasterFiles.Customers"] = field(
            default=None,
            metadata={
                "name": "Customers",
                "type": "Element",
            },
        )
        suppliers: Optional["AuditFile.MasterFiles.Suppliers"] = field(
            default=None,
            metadata={
                "name": "Suppliers",
                "type": "Element",
            },
        )
        tax_table: Optional["AuditFile.MasterFiles.TaxTable"] = field(
            default=None,
            metadata={
                "name": "TaxTable",
                "type": "Element",
            },
        )
        uomtable: Optional["AuditFile.MasterFiles.Uomtable"] = field(
            default=None,
            metadata={
                "name": "UOMTable",
                "type": "Element",
            },
        )
        analysis_type_table: Optional[
            "AuditFile.MasterFiles.AnalysisTypeTable"
        ] = field(
            default=None,
            metadata={
                "name": "AnalysisTypeTable",
                "type": "Element",
            },
        )
        movement_type_table: Optional[
            "AuditFile.MasterFiles.MovementTypeTable"
        ] = field(
            default=None,
            metadata={
                "name": "MovementTypeTable",
                "type": "Element",
            },
        )
        products: Optional["AuditFile.MasterFiles.Products"] = field(
            default=None,
            metadata={
                "name": "Products",
                "type": "Element",
            },
        )
        physical_stock: Optional["AuditFile.MasterFiles.PhysicalStock"] = (
            field(
                default=None,
                metadata={
                    "name": "PhysicalStock",
                    "type": "Element",
                },
            )
        )
        owners: Optional["AuditFile.MasterFiles.Owners"] = field(
            default=None,
            metadata={
                "name": "Owners",
                "type": "Element",
            },
        )
        assets: Optional["AuditFile.MasterFiles.Assets"] = field(
            default=None,
            metadata={
                "name": "Assets",
                "type": "Element",
            },
        )

        @dataclass
        class GeneralLedgerAccounts:
            """
            :ivar account: General ledger account information.
            """

            account: List[
                "AuditFile.MasterFiles.GeneralLedgerAccounts.Account"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "Account",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Account:
                """
                :ivar account_id: General ledger account code/number.
                :ivar account_description: Name of individual general
                    ledger account.
                :ivar standard_account_id: Standard general ledger
                    account code/number from codelists for mapping.
                    Alternatively the elements GroupingCategory and
                    GroupingCode can be used for mapping.
                :ivar grouping_category: Use in conjunction with
                    GroupingCode. Use category from codelists.
                :ivar grouping_code: Use in conjunction with
                    GroupingCategory. Use code from codelists.
                :ivar account_type: Type of account. Set standard
                    account in the StandardAccountID element. The only
                    valid value is “GL” (General Ledger).
                :ivar account_creation_date: Date of when the general
                    ledger account was created.
                :ivar opening_debit_balance: Debit balance at the start
                    date of the selection period in the header's default
                    currency.
                :ivar opening_credit_balance: Credit balance at the
                    start date of the selection period in the header's
                    default currency.
                :ivar closing_debit_balance: Debit balance at the end
                    date of the selection period in the header's default
                    currency.
                :ivar closing_credit_balance: Credit balance at the end
                    date of the selection period in the header's default
                    currency.
                """

                account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountID",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                account_description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountDescription",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                standard_account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "StandardAccountID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                grouping_category: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "GroupingCategory",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                grouping_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "GroupingCode",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                account_type: Optional[AccountAccountType] = field(
                    default=None,
                    metadata={
                        "name": "AccountType",
                        "type": "Element",
                        "required": True,
                    },
                )
                account_creation_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "AccountCreationDate",
                        "type": "Element",
                    },
                )
                opening_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                opening_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )

        @dataclass
        class Taxonomies:
            taxonomy: List["AuditFile.MasterFiles.Taxonomies.Taxonomy"] = (
                field(
                    default_factory=list,
                    metadata={
                        "name": "Taxonomy",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )
            )

            @dataclass
            class Taxonomy:
                """
                :ivar taxonomy_reference: Reference to the taxonomy that
                    applies to the GL Account.
                :ivar taxonomy_element:
                """

                taxonomy_reference: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "TaxonomyReference",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                taxonomy_element: List[
                    "AuditFile.MasterFiles.Taxonomies.Taxonomy.TaxonomyElement"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "TaxonomyElement",
                        "type": "Element",
                    },
                )

                @dataclass
                class TaxonomyElement:
                    """
                    :ivar taxonomy_code: Reference to specific taxonomy
                        element
                    :ivar taxonomy_cluster_id: Additional reference to
                        specific taxonomy element
                    :ivar taxonomy_cluster_context_id:
                    :ivar account_id: General Ledger Account code for
                        this TaxanomyReference/TaxonomyCode. Can be
                        including sub-account id. It can contain many
                        different levels to identify the Account. It
                        could include cost centres such as company,
                        division, region, group and branch/department.
                    """

                    taxonomy_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxonomyCode",
                            "type": "Element",
                            "required": True,
                            "max_length": 256,
                        },
                    )
                    taxonomy_cluster_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxonomyClusterID",
                            "type": "Element",
                            "max_length": 256,
                        },
                    )
                    taxonomy_cluster_context_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxonomyClusterContextID",
                            "type": "Element",
                            "max_length": 256,
                        },
                    )
                    account_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AccountID",
                            "type": "Element",
                            "required": True,
                            "max_length": 70,
                        },
                    )

        @dataclass
        class Customers:
            """
            :ivar customer: Customer information.
            """

            customer: List["AuditFile.MasterFiles.Customers.Customer"] = field(
                default_factory=list,
                metadata={
                    "name": "Customer",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Customer(CompanyStructure):
                """
                :ivar customer_id: Unique account code/number for the
                    customer.
                :ivar self_billing_indicator: Indicator showing if a
                    self-billing agreement exists between the customer
                    and the supplier.
                :ivar account_id: General ledger account code/number for
                    this customer. This is the account code/number into
                    where this sub account/accounts receivable is
                    consolidated in the balance sheet.
                :ivar opening_debit_balance: Debit balance at the start
                    date of the selection period in the header's default
                    currency.
                :ivar opening_credit_balance: Credit balance at the
                    start date of the selection period in the header's
                    default currency.
                :ivar closing_debit_balance: Debit balance at the end
                    date of the selection period in the header's default
                    currency.
                :ivar closing_credit_balance: Credit balance at the end
                    date of the selection period in the header's default
                    currency.
                :ivar party_info: Additional party information.
                """

                customer_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "CustomerID",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                self_billing_indicator: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SelfBillingIndicator",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountID",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                opening_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                opening_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                party_info: Optional[PartyInfoStructure] = field(
                    default=None,
                    metadata={
                        "name": "PartyInfo",
                        "type": "Element",
                    },
                )

        @dataclass
        class Suppliers:
            """
            :ivar supplier: Supplier information.
            """

            supplier: List["AuditFile.MasterFiles.Suppliers.Supplier"] = field(
                default_factory=list,
                metadata={
                    "name": "Supplier",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Supplier(CompanyStructure):
                """
                :ivar supplier_id: Unique account code/number for the
                    supplier.
                :ivar self_billing_indicator: Indicator showing if a
                    self-billing agreement exists between the customer
                    and the supplier.
                :ivar account_id: General ledger account code/number for
                    this supplier. This is the account code/number into
                    where this sub account/accounts payable is
                    consolidated in the balance sheet.
                :ivar opening_debit_balance: Debit balance at the start
                    date of the selection period in the header's default
                    currency.
                :ivar opening_credit_balance: Credit balance at the
                    start date of the selection period in the header's
                    default currency.
                :ivar closing_debit_balance: Debit balance at the end
                    date of the selection period in the header's default
                    currency.
                :ivar closing_credit_balance: Credit balance at the end
                    date of the selection period in the header's default
                    currency.
                :ivar party_info: Additional party information.
                """

                supplier_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SupplierID",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                self_billing_indicator: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SelfBillingIndicator",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountID",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                opening_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                opening_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_debit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingDebitBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_credit_balance: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingCreditBalance",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                party_info: Optional[PartyInfoStructure] = field(
                    default=None,
                    metadata={
                        "name": "PartyInfo",
                        "type": "Element",
                    },
                )

        @dataclass
        class TaxTable:
            """
            :ivar tax_table_entry: Tax entry information.
            """

            tax_table_entry: List[
                "AuditFile.MasterFiles.TaxTable.TaxTableEntry"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "TaxTableEntry",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class TaxTableEntry:
                """
                :ivar tax_type: Tax type for look-up in tables. “MVA” is
                    the only valid value.
                :ivar description: Description of the Tax Type.
                    “Merverdiavgift” is the only valid value.
                :ivar tax_code_details: Tax code details of the tax
                    table entry.
                """

                tax_type: Optional[TaxTableEntryTaxType] = field(
                    default=None,
                    metadata={
                        "name": "TaxType",
                        "type": "Element",
                        "required": True,
                    },
                )
                description: Optional[TaxTableEntryDescription] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                    },
                )
                tax_code_details: List[
                    "AuditFile.MasterFiles.TaxTable.TaxTableEntry.TaxCodeDetails"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "TaxCodeDetails",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class TaxCodeDetails:
                    """
                    :ivar tax_code: Tax Code for lookup in tables.
                    :ivar effective_date: Representing the starting date
                        for this entry.
                    :ivar expiration_date: Representing the ending date
                        for this entry.
                    :ivar description: Description of the Tax Code.
                    :ivar tax_percentage: Tax percentage.
                    :ivar flat_tax_rate: Not in use.
                    :ivar country: Two-letter country code according to
                        ISO 3166-1 alpha 2 standard.
                    :ivar region: Not in use.
                    :ivar standard_tax_code: Standard Tax Code.
                    :ivar compensation: Indicates if the Tax Code is
                        used for compensation.
                    :ivar base_rate: Base rates used for the tax code.
                        Standard is 100 (the whole amount is tax
                        deductible). Example: 60 if only 60% of the
                        total amount is tax deductible. Enter all
                        standard base rates used for the tax code.
                    """

                    tax_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxCode",
                            "type": "Element",
                            "required": True,
                            "max_length": 35,
                        },
                    )
                    effective_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "EffectiveDate",
                            "type": "Element",
                        },
                    )
                    expiration_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "ExpirationDate",
                            "type": "Element",
                        },
                    )
                    description: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Description",
                            "type": "Element",
                            "max_length": 256,
                        },
                    )
                    tax_percentage: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "TaxPercentage",
                            "type": "Element",
                        },
                    )
                    flat_tax_rate: Optional[AmountStructure] = field(
                        default=None,
                        metadata={
                            "name": "FlatTaxRate",
                            "type": "Element",
                        },
                    )
                    country: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Country",
                            "type": "Element",
                            "required": True,
                            "length": 2,
                        },
                    )
                    region: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Region",
                            "type": "Element",
                            "max_length": 9,
                        },
                    )
                    standard_tax_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "StandardTaxCode",
                            "type": "Element",
                            "required": True,
                            "max_length": 35,
                        },
                    )
                    compensation: Optional[bool] = field(
                        default=None,
                        metadata={
                            "name": "Compensation",
                            "type": "Element",
                        },
                    )
                    base_rate: List[Decimal] = field(
                        default_factory=list,
                        metadata={
                            "name": "BaseRate",
                            "type": "Element",
                            "min_occurs": 1,
                            "min_inclusive": Decimal("0"),
                            "max_inclusive": Decimal("100"),
                        },
                    )

        @dataclass
        class Uomtable:
            uomtable_entry: List[
                "AuditFile.MasterFiles.Uomtable.UomtableEntry"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "UOMTableEntry",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class UomtableEntry:
                """
                :ivar unit_of_measure: Quantity unit of measure e.g.
                    pack of 12
                :ivar description: Description of the UOM
                """

                unit_of_measure: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UnitOfMeasure",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )

        @dataclass
        class AnalysisTypeTable:
            """
            :ivar analysis_type_table_entry: Analysis entry information.
            """

            analysis_type_table_entry: List[
                "AuditFile.MasterFiles.AnalysisTypeTable.AnalysisTypeTableEntry"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "AnalysisTypeTableEntry",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class AnalysisTypeTableEntry:
                """
                :ivar analysis_type: Analysis type identifier/code for
                    the dimension type (e.g. departments, projects,
                    journal types, cost centers, employees, etc.).
                :ivar analysis_type_description: Description of the
                    dimension type.
                :ivar analysis_id: Analysis ID of the specific dimension
                    entity.
                :ivar analysis_iddescription: Description of the
                    specific dimension entity.
                :ivar start_date: Start date.
                :ivar end_date: End date.
                :ivar status: Status of the analysis entry. Choose from
                    the predefined enumerations: Active, Closed,
                    Observation, Passive.
                :ivar analysis: Standard linked analysis codes for the
                    analysis entry, such as project, department, cost
                    center, groups, etc.
                """

                analysis_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AnalysisType",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                analysis_type_description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AnalysisTypeDescription",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                analysis_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AnalysisID",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                analysis_iddescription: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AnalysisIDDescription",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                start_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "StartDate",
                        "type": "Element",
                    },
                )
                end_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "EndDate",
                        "type": "Element",
                    },
                )
                status: Optional[AnalysisTypeTableEntryStatus] = field(
                    default=None,
                    metadata={
                        "name": "Status",
                        "type": "Element",
                    },
                )
                analysis: List[AnalysisPartyInfoStructure] = field(
                    default_factory=list,
                    metadata={
                        "name": "Analysis",
                        "type": "Element",
                    },
                )

        @dataclass
        class MovementTypeTable:
            movement_type_table_entry: List[
                "AuditFile.MasterFiles.MovementTypeTable.MovementTypeTableEntry"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "MovementTypeTableEntry",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class MovementTypeTableEntry:
                """
                :ivar movement_type: Identify kind of movement or
                    movement line. E.g. sale, purchase, adjustment, etc.
                    Or  efficiencyloss, use of components in production,
                    etc. Predescribed TABLE is possible.
                :ivar description: Description of the movement(sub)type
                """

                movement_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MovementType",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )

        @dataclass
        class Products:
            product: List["AuditFile.MasterFiles.Products.Product"] = field(
                default_factory=list,
                metadata={
                    "name": "Product",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Product:
                """
                :ivar product_code: Product code
                :ivar goods_services_id: Indicator showing if goods or
                    services (Predescribed TABLE is possible)
                :ivar product_group: Code identifying aggregated level
                    at which similar products are grouped
                :ivar description: Description of goods or services.
                :ivar product_commodity_code: Classification for import
                    / export
                :ivar product_number_code: EAN or other code
                :ivar valuation_method: FIFO, LIFO, Average cost etc.
                :ivar uombase: Unit of measure for Stock Administration
                    for this product Predescribed TABLE is possible.
                :ivar uomstandard: A Standard Unit of Measure applicable
                    for this product, f.i. Kilo, Metres, Litres
                    (Predescribed TABLE is possible)
                :ivar uomto_uombase_conversion_factor: Conversion factor
                    of the UOM to UOM Base
                :ivar tax:
                """

                product_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductCode",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                goods_services_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "GoodsServicesID",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                product_group: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductGroup",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                product_commodity_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductCommodityCode",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                product_number_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductNumberCode",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                valuation_method: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ValuationMethod",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                uombase: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOMBase",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                uomstandard: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOMStandard",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                uomto_uombase_conversion_factor: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "UOMToUOMBaseConversionFactor",
                        "type": "Element",
                    },
                )
                tax: List["AuditFile.MasterFiles.Products.Product.Tax"] = (
                    field(
                        default_factory=list,
                        metadata={
                            "name": "Tax",
                            "type": "Element",
                        },
                    )
                )

                @dataclass
                class Tax:
                    """
                    :ivar tax_type: Tax Type for lookup in tables
                    :ivar tax_code: Tax Code for lookup in tables
                    """

                    tax_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxType",
                            "type": "Element",
                            "max_length": 9,
                        },
                    )
                    tax_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TaxCode",
                            "type": "Element",
                            "max_length": 9,
                        },
                    )

        @dataclass
        class PhysicalStock:
            physical_stock_entry: List[
                "AuditFile.MasterFiles.PhysicalStock.PhysicalStockEntry"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "PhysicalStockEntry",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class PhysicalStockEntry:
                """
                :ivar warehouse_id: Warehouse where goods held -
                    possoble also to identify work-in-progress, or
                    stock-in-transit
                :ivar location_id: Location of goods in warehouse
                :ivar product_code: Product code
                :ivar stock_account_no: Stock batch, lot, serial
                    identification. Not used when there is exactly 1
                    PhysicalStock entry per ProductCode
                :ivar product_type: To determine whether the
                    product/stockaccount is raw material, work-in-
                    progress, finished good, merchandise for resale,
                    etc.
                :ivar product_status: To determine whether the
                    product/stockaccount is discontinued, damaged,
                    obsolete, active, etc.
                :ivar stock_account_commodity_code: Classification for
                    import / export
                :ivar owner_id: Reference to the owner Master File
                :ivar uomphysical_stock: Unit of Measurement for this
                    Physical Stock position
                :ivar uomto_uombase_conversion_factor: Conversion factor
                    of the UOM to UOM Base
                :ivar unit_price: Base Unit price for this stock account
                    in the header's default currency.
                :ivar opening_stock_quantity: In UOM Physical Stock for
                    selection period
                :ivar opening_stock_value: In  the header's currency
                    code for selection period
                :ivar closing_stock_quantity: In UOM Physical Stock for
                    selection period
                :ivar closing_stock_value: Closing stock value  in the
                    header's default currency for selection period
                :ivar stock_characteristics:
                """

                warehouse_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "WarehouseID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                location_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "LocationID",
                        "type": "Element",
                        "max_length": 18,
                    },
                )
                product_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductCode",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                stock_account_no: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "StockAccountNo",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                product_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductType",
                        "type": "Element",
                        "max_length": 18,
                    },
                )
                product_status: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ProductStatus",
                        "type": "Element",
                        "max_length": 18,
                    },
                )
                stock_account_commodity_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "StockAccountCommodityCode",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                owner_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "OwnerID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                uomphysical_stock: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOMPhysicalStock",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                uomto_uombase_conversion_factor: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "UOMToUOMBaseConversionFactor",
                        "type": "Element",
                    },
                )
                unit_price: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "UnitPrice",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                opening_stock_quantity: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningStockQuantity",
                        "type": "Element",
                        "required": True,
                        "total_digits": 22,
                        "fraction_digits": 6,
                    },
                )
                opening_stock_value: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "OpeningStockValue",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                closing_stock_quantity: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingStockQuantity",
                        "type": "Element",
                        "required": True,
                        "total_digits": 22,
                        "fraction_digits": 6,
                    },
                )
                closing_stock_value: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "ClosingStockValue",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                    },
                )
                stock_characteristics: Optional[
                    "AuditFile.MasterFiles.PhysicalStock.PhysicalStockEntry.StockCharacteristics"
                ] = field(
                    default=None,
                    metadata={
                        "name": "StockCharacteristics",
                        "type": "Element",
                    },
                )

                @dataclass
                class StockCharacteristics:
                    """
                    :ivar stock_characteristic: User definable
                        characteristics of the goods. Predescribed TABLE
                        is possible.
                    :ivar stock_characteristic_value: The weight, pack
                        size, colour etc.
                    """

                    stock_characteristic: List[str] = field(
                        default_factory=list,
                        metadata={
                            "name": "StockCharacteristic",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_length": 18,
                            "sequence": 1,
                        },
                    )
                    stock_characteristic_value: List[str] = field(
                        default_factory=list,
                        metadata={
                            "name": "StockCharacteristicValue",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_length": 35,
                            "sequence": 1,
                        },
                    )

        @dataclass
        class Owners:
            """
            :ivar owner: Owner information.
            """

            owner: List["AuditFile.MasterFiles.Owners.Owner"] = field(
                default_factory=list,
                metadata={
                    "name": "Owner",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Owner(CompanyStructure):
                """
                :ivar owner_id: Unique ID code/number for the owner.
                :ivar account_id: General ledger account code for this
                    owner. Can be including sub-account id. It can
                    contain many different levels to identify the
                    Account.
                """

                owner_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "OwnerID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountID",
                        "type": "Element",
                        "max_length": 70,
                    },
                )

        @dataclass
        class Assets:
            asset: List["AuditFile.MasterFiles.Assets.Asset"] = field(
                default_factory=list,
                metadata={
                    "name": "Asset",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Asset:
                """
                :ivar asset_id: Unique identifier of the asset
                :ivar account_id: General Ledger Account code. Can be
                    including sub-account id. It can contain many
                    different levels to identify the Account. It could
                    include cost centres such as company, division,
                    region, group and branch/department.
                :ivar description: Description of this asset
                :ivar supplier: Contains the information of all
                    suppliers, including the historical suppliers.
                :ivar purchase_order_date: Date of the purchase order of
                    this asset
                :ivar date_of_acquisition: Date of the acquisition of
                    the asset (usually the date of delivery).
                :ivar start_up_date: Commissioning date of the asset.
                :ivar valuations: The data can be reported for different
                    purposes. More than one can be in this SAF.
                """

                asset_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AssetID",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                account_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AccountID",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                supplier: List[
                    "AuditFile.MasterFiles.Assets.Asset.Supplier"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "Supplier",
                        "type": "Element",
                    },
                )
                purchase_order_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "PurchaseOrderDate",
                        "type": "Element",
                    },
                )
                date_of_acquisition: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "DateOfAcquisition",
                        "type": "Element",
                        "required": True,
                    },
                )
                start_up_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "StartUpDate",
                        "type": "Element",
                    },
                )
                valuations: Optional[
                    "AuditFile.MasterFiles.Assets.Asset.Valuations"
                ] = field(
                    default=None,
                    metadata={
                        "name": "Valuations",
                        "type": "Element",
                        "required": True,
                    },
                )

                @dataclass
                class Supplier:
                    """
                    :ivar supplier_name: Name of the supplier of the
                        asset
                    :ivar supplier_id: Unique code for the supplier
                    :ivar postal_address: Address information of the
                        supplier of the asset
                    """

                    supplier_name: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierName",
                            "type": "Element",
                            "required": True,
                            "max_length": 70,
                        },
                    )
                    supplier_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    postal_address: Optional[AddressStructure] = field(
                        default=None,
                        metadata={
                            "name": "PostalAddress",
                            "type": "Element",
                            "required": True,
                        },
                    )

                @dataclass
                class Valuations:
                    valuation: List[
                        "AuditFile.MasterFiles.Assets.Asset.Valuations.Valuation"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "Valuation",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )

                    @dataclass
                    class Valuation:
                        """
                        :ivar asset_valuation_type: Describes the
                            purpose for the reporting: f.i. commercial,
                            tax  in country 1, tax in country 2, etc.
                        :ivar valuation_class: This describes the
                            classification of the asset for (tax)
                            reporting purposes.
                        :ivar acquisition_and_production_costs_begin:
                            Total costs of acquisition and/or production
                            of the asset at SelectionStartDate in the
                            header's default currency.
                        :ivar acquisition_and_production_costs_end:
                            Total costs of acquisition and/or production
                            of the asset at SelectionEndDate in the
                            header's default currency.
                        :ivar investment_support: Total amount of
                            investment support for this asset in the
                            header's default currency.
                        :ivar asset_life_year: Periode of useful life in
                            years
                        :ivar asset_life_month: Period of useful life in
                            months
                        :ivar asset_addition: Bookvalue of the
                            acquisition and/or production of the asset
                            in the  Selectionperiod in the header's
                            default currency.
                        :ivar transfers: Book value of the transfers of
                            the asset during the Selectionperiod in the
                            header's default currency.
                        :ivar asset_disposal: Book value of the
                            disposals of the asset during the
                            Selectionperiod in the header's default
                            currency.
                        :ivar book_value_begin: Bookvalue at the
                            beginning of the Selectionperiod in the
                            header's default currency.
                        :ivar depreciation_method: Method of normal
                            depreciation during the Selectionperiod.
                        :ivar depreciation_percentage: The rate of the
                            normal depreciation per year or month
                            (depends on choice useful life periode)
                        :ivar depreciation_for_period: Total amouunt of
                            normal depreciation during the
                            Selectionperiod in the header's default
                            currency.
                        :ivar appreciation_for_period: Total amouunt of
                            appreciation during the Selectionperiod in
                            the header's default currency.
                        :ivar extraordinary_depreciations_for_period:
                            Extraordinary depreciations for this asset
                            during the Selectionperiod.
                        :ivar accumulated_depreciation: Total amount of
                            depreciation for this asset
                        :ivar book_value_end: Bookvalue at the end of
                            the Selectionperiod in the header's default
                            currency.
                        """

                        asset_valuation_type: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "AssetValuationType",
                                "type": "Element",
                                "max_length": 18,
                            },
                        )
                        valuation_class: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "ValuationClass",
                                "type": "Element",
                                "max_length": 18,
                            },
                        )
                        acquisition_and_production_costs_begin: Optional[
                            Decimal
                        ] = field(
                            default=None,
                            metadata={
                                "name": "AcquisitionAndProductionCostsBegin",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        acquisition_and_production_costs_end: Optional[
                            Decimal
                        ] = field(
                            default=None,
                            metadata={
                                "name": "AcquisitionAndProductionCostsEnd",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        investment_support: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "InvestmentSupport",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        asset_life_year: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetLifeYear",
                                "type": "Element",
                            },
                        )
                        asset_life_month: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetLifeMonth",
                                "type": "Element",
                            },
                        )
                        asset_addition: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetAddition",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        transfers: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "Transfers",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        asset_disposal: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetDisposal",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        book_value_begin: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "BookValueBegin",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        depreciation_method: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "DepreciationMethod",
                                "type": "Element",
                                "max_length": 35,
                            },
                        )
                        depreciation_percentage: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "DepreciationPercentage",
                                "type": "Element",
                            },
                        )
                        depreciation_for_period: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "DepreciationForPeriod",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        appreciation_for_period: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AppreciationForPeriod",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        extraordinary_depreciations_for_period: Optional[
                            "AuditFile.MasterFiles.Assets.Asset.Valuations.Valuation.ExtraordinaryDepreciationsForPeriod"
                        ] = field(
                            default=None,
                            metadata={
                                "name": "ExtraordinaryDepreciationsForPeriod",
                                "type": "Element",
                            },
                        )
                        accumulated_depreciation: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AccumulatedDepreciation",
                                "type": "Element",
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        book_value_end: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "BookValueEnd",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )

                        @dataclass
                        class ExtraordinaryDepreciationsForPeriod:
                            extraordinary_depreciation_for_period: List[
                                "AuditFile.MasterFiles.Assets.Asset.Valuations.Valuation.ExtraordinaryDepreciationsForPeriod.ExtraordinaryDepreciationForPeriod"
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "name": "ExtraordinaryDepreciationForPeriod",
                                    "type": "Element",
                                    "min_occurs": 1,
                                },
                            )

                            @dataclass
                            class ExtraordinaryDepreciationForPeriod:
                                """
                                :ivar extraordinary_depreciation_method:
                                    Method of extraordinary depreciation
                                    during the Selectionperiod.
                                :ivar
                                    extraordinary_depreciation_for_period:
                                    Amouunt of extraordinary
                                    depreciation during the
                                    Selectionperiod in the header's
                                    default currency.
                                """

                                extraordinary_depreciation_method: Optional[
                                    str
                                ] = field(
                                    default=None,
                                    metadata={
                                        "name": "ExtraordinaryDepreciationMethod",
                                        "type": "Element",
                                        "required": True,
                                        "max_length": 35,
                                    },
                                )
                                extraordinary_depreciation_for_period: Optional[
                                    Decimal
                                ] = field(
                                    default=None,
                                    metadata={
                                        "name": "ExtraordinaryDepreciationForPeriod",
                                        "type": "Element",
                                        "required": True,
                                        "total_digits": 18,
                                        "fraction_digits": 2,
                                    },
                                )

    @dataclass
    class GeneralLedgerEntries:
        """
        :ivar number_of_entries: Number of entries. This is the total
            number of Transaction entries (accounting
            documents/vouchers) from all Journals included in the audit
            file.
        :ivar total_debit: The total of all debit amounts in the
            header's default currency.
        :ivar total_credit: The total of all credit amounts in the
            header's default currency.
        :ivar journal: Journal information.
        """

        number_of_entries: Optional[int] = field(
            default=None,
            metadata={
                "name": "NumberOfEntries",
                "type": "Element",
                "required": True,
            },
        )
        total_debit: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "TotalDebit",
                "type": "Element",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )
        total_credit: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "TotalCredit",
                "type": "Element",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            },
        )
        journal: List["AuditFile.GeneralLedgerEntries.Journal"] = field(
            default_factory=list,
            metadata={
                "name": "Journal",
                "type": "Element",
            },
        )

        @dataclass
        class Journal:
            """
            :ivar journal_id: Source GL journal identifier, or invoices
                and payments in single ledger systems.
            :ivar description: Description of the Journal.
            :ivar type_value: Grouping mechanism for journals. Please
                use the examples in the technical description when
                appropriate.
            :ivar transaction: Accounting transactions.
            """

            journal_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "JournalID",
                    "type": "Element",
                    "required": True,
                    "max_length": 18,
                },
            )
            description: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Description",
                    "type": "Element",
                    "required": True,
                    "max_length": 256,
                },
            )
            type_value: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Type",
                    "type": "Element",
                    "required": True,
                    "max_length": 9,
                },
            )
            transaction: List[
                "AuditFile.GeneralLedgerEntries.Journal.Transaction"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "Transaction",
                    "type": "Element",
                },
            )

            @dataclass
            class Transaction:
                """
                :ivar transaction_id: The number/ID of the accounting
                    document/voucher.
                :ivar period: Accounting Period.
                :ivar period_year: The year of the Accounting Period.
                    Restriction: 1970-2100.
                :ivar transaction_date: The date of the accounting
                    document/voucher.
                :ivar source_id: Details of person or application that
                    entered the transaction.
                :ivar transaction_type: Type of journaltransaction:
                    normal, (automated) periodically, etc.
                :ivar description: Description of Journal Transaction.
                :ivar batch_id: Systems generated ID for batch.
                :ivar system_entry_date: Date captured by system. The
                    date when the transaction was entered into the
                    system - manual entry, imported transaction, etc. If
                    this date is not available in your system, use the
                    TransactionDate.
                :ivar glposting_date: Date posting to the general ledger
                    account. The date when the transaction was updated
                    to the database. If this date is not available in
                    your system, use the TransactionDate.
                :ivar customer_id: Not in use.
                :ivar supplier_id: Not in use.
                :ivar system_id: Unique ID/number created by the system
                    for the accounting document/voucher.
                :ivar line: Transaction lines.
                """

                transaction_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "TransactionID",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                period: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "Period",
                        "type": "Element",
                        "required": True,
                    },
                )
                period_year: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "PeriodYear",
                        "type": "Element",
                        "required": True,
                        "min_inclusive": 1970,
                        "max_inclusive": 2100,
                    },
                )
                transaction_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "TransactionDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                source_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SourceID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                transaction_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "TransactionType",
                        "type": "Element",
                        "max_length": 18,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                batch_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "BatchID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                system_entry_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "SystemEntryDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                glposting_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "GLPostingDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                customer_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "CustomerID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                supplier_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SupplierID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                system_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SystemID",
                        "type": "Element",
                        "max_length": 18,
                    },
                )
                line: List[
                    "AuditFile.GeneralLedgerEntries.Journal.Transaction.Line"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "Line",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class Line:
                    """
                    :ivar record_id: Identifier to trace entry to
                        journal line or posting reference.
                    :ivar account_id: General ledger account
                        code/number. If this Line is a ledger/sub
                        account (accounts payable or accounts
                        receivable) entry, then this is the account
                        code/number into where this ledger/sub account
                        is consolidated in the balance sheet.
                    :ivar analysis: General Ledger analysis codes
                    :ivar value_date: Effective date from which interest
                        charged. To be reported when this date or this
                        Line of the accounting document/voucher differs
                        from the TransactionDate.
                    :ivar source_document_id: Source document number to
                        which line relates.
                    :ivar customer_id: Unique account code/number for
                        the customer. Is only used if this Line is a
                        ledger/sub account (accounts payable or accounts
                        receivable) entry. Must not be used in
                        conjunction with SupplierID.
                    :ivar supplier_id: Unique account code/number for
                        the supplier. Is only used if this Line is a
                        ledger/sub account (accounts payable or accounts
                        receivable) entry. Must not be used in
                        conjunction with CustomerID.
                    :ivar description: Description of the Journal Line.
                    :ivar debit_amount: Debit amount information for
                        transaction.
                    :ivar credit_amount: Credit amount information for
                        transaction.
                    :ivar tax_information: Tax information for the
                        accounting line.
                    :ivar reference_number: The reference number, such
                        as invoice or credit note number.
                    :ivar cid: The CID number.
                    :ivar due_date: The due date.
                    :ivar quantity: Quantity.
                    :ivar cross_reference: Cross-reference. Information
                        about matched documents/records.
                    :ivar system_entry_time: Time captured by system.
                        The time when the transaction was entered into
                        the system - manual entry, imported transaction,
                        etc.
                    :ivar owner_id: The unique ID code/number for the
                        owner.
                    """

                    record_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "RecordID",
                            "type": "Element",
                            "required": True,
                            "max_length": 18,
                        },
                    )
                    account_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AccountID",
                            "type": "Element",
                            "required": True,
                            "max_length": 70,
                        },
                    )
                    analysis: List[AnalysisStructure] = field(
                        default_factory=list,
                        metadata={
                            "name": "Analysis",
                            "type": "Element",
                        },
                    )
                    value_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "ValueDate",
                            "type": "Element",
                        },
                    )
                    source_document_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SourceDocumentID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    customer_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CustomerID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    supplier_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    description: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Description",
                            "type": "Element",
                            "required": True,
                            "max_length": 256,
                        },
                    )
                    debit_amount: Optional[AmountStructure] = field(
                        default=None,
                        metadata={
                            "name": "DebitAmount",
                            "type": "Element",
                        },
                    )
                    credit_amount: Optional[AmountStructure] = field(
                        default=None,
                        metadata={
                            "name": "CreditAmount",
                            "type": "Element",
                        },
                    )
                    tax_information: List[TaxInformationStructure] = field(
                        default_factory=list,
                        metadata={
                            "name": "TaxInformation",
                            "type": "Element",
                        },
                    )
                    reference_number: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ReferenceNumber",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    cid: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    due_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "DueDate",
                            "type": "Element",
                        },
                    )
                    quantity: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "Quantity",
                            "type": "Element",
                            "total_digits": 22,
                            "fraction_digits": 6,
                        },
                    )
                    cross_reference: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CrossReference",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    system_entry_time: Optional[XmlDateTime] = field(
                        default=None,
                        metadata={
                            "name": "SystemEntryTime",
                            "type": "Element",
                        },
                    )
                    owner_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "OwnerID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )

    @dataclass
    class SourceDocuments:
        """
        :ivar sales_invoices:
        :ivar purchase_invoices:
        :ivar payments:
        :ivar movement_of_goods:
        :ivar asset_transactions: Details of all transactions related to
            an asset during the Selectionperiod.
        """

        sales_invoices: Optional["AuditFile.SourceDocuments.SalesInvoices"] = (
            field(
                default=None,
                metadata={
                    "name": "SalesInvoices",
                    "type": "Element",
                },
            )
        )
        purchase_invoices: Optional[
            "AuditFile.SourceDocuments.PurchaseInvoices"
        ] = field(
            default=None,
            metadata={
                "name": "PurchaseInvoices",
                "type": "Element",
            },
        )
        payments: Optional["AuditFile.SourceDocuments.Payments"] = field(
            default=None,
            metadata={
                "name": "Payments",
                "type": "Element",
            },
        )
        movement_of_goods: Optional[
            "AuditFile.SourceDocuments.MovementOfGoods"
        ] = field(
            default=None,
            metadata={
                "name": "MovementOfGoods",
                "type": "Element",
            },
        )
        asset_transactions: Optional[
            "AuditFile.SourceDocuments.AssetTransactions"
        ] = field(
            default=None,
            metadata={
                "name": "AssetTransactions",
                "type": "Element",
            },
        )

        @dataclass
        class SalesInvoices:
            """
            :ivar number_of_entries: Number of entries
            :ivar total_debit: The total of all debit amounts in the
                header's default currency
            :ivar total_credit: The total of all credit amounts in the
                header's default currency
            :ivar invoice:
            """

            number_of_entries: Optional[int] = field(
                default=None,
                metadata={
                    "name": "NumberOfEntries",
                    "type": "Element",
                    "required": True,
                },
            )
            total_debit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalDebit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            total_credit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalCredit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            invoice: List[InvoiceStructure] = field(
                default_factory=list,
                metadata={
                    "name": "Invoice",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

        @dataclass
        class PurchaseInvoices:
            """
            :ivar number_of_entries: Number of entries
            :ivar total_debit: The total of all debit amounts in the
                header's default currency
            :ivar total_credit: The total of all credit amounts in the
                header's default currency
            :ivar invoice:
            """

            number_of_entries: Optional[int] = field(
                default=None,
                metadata={
                    "name": "NumberOfEntries",
                    "type": "Element",
                    "required": True,
                },
            )
            total_debit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalDebit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            total_credit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalCredit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            invoice: List[InvoiceStructure] = field(
                default_factory=list,
                metadata={
                    "name": "Invoice",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

        @dataclass
        class Payments:
            """
            :ivar number_of_entries: Number of entries
            :ivar total_debit: The total of all debit amounts in the
                header's default currency
            :ivar total_credit: The total of all credit amounts in the
                header's default currency
            :ivar payment:
            """

            number_of_entries: Optional[int] = field(
                default=None,
                metadata={
                    "name": "NumberOfEntries",
                    "type": "Element",
                    "required": True,
                },
            )
            total_debit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalDebit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            total_credit: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalCredit",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                },
            )
            payment: List["AuditFile.SourceDocuments.Payments.Payment"] = (
                field(
                    default_factory=list,
                    metadata={
                        "name": "Payment",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )
            )

            @dataclass
            class Payment:
                """
                :ivar payment_ref_no: Unique reference number for
                    payment
                :ivar period: Accounting Period
                :ivar period_year: The year of the Accounting Period.
                :ivar transaction_id: Cross-reference to GL posting. It
                    can contain many different levels to identify the
                    transaction. It could include cost centres such as
                    company, division, region, group and
                    branch/department.
                :ivar transaction_date: Document date
                :ivar payment_method: Cheque, Bank, Giro, Cash, etc.
                :ivar description: Description of the payment.
                :ivar batch_id: Systems generated ID for batch
                :ivar system_id: Unique number created by the system for
                    the document
                :ivar source_id: Details of person or application that
                    entered the transaction
                :ivar line:
                :ivar settlement:
                :ivar document_totals:
                """

                payment_ref_no: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "PaymentRefNo",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                period: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "Period",
                        "type": "Element",
                    },
                )
                period_year: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "PeriodYear",
                        "type": "Element",
                        "min_inclusive": 1970,
                        "max_inclusive": 2100,
                    },
                )
                transaction_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "TransactionID",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                transaction_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "TransactionDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                payment_method: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "PaymentMethod",
                        "type": "Element",
                        "max_length": 9,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "required": True,
                        "max_length": 256,
                    },
                )
                batch_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "BatchID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                system_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SystemID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                source_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SourceID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                line: List[
                    "AuditFile.SourceDocuments.Payments.Payment.Line"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "Line",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )
                settlement: Optional[
                    "AuditFile.SourceDocuments.Payments.Payment.Settlement"
                ] = field(
                    default=None,
                    metadata={
                        "name": "Settlement",
                        "type": "Element",
                    },
                )
                document_totals: Optional[
                    "AuditFile.SourceDocuments.Payments.Payment.DocumentTotals"
                ] = field(
                    default=None,
                    metadata={
                        "name": "DocumentTotals",
                        "type": "Element",
                    },
                )

                @dataclass
                class Line:
                    """
                    :ivar line_number: Number of the paymentline
                    :ivar source_document_id: The source document to
                        which the line relates
                    :ivar account_id: General Ledger Account code. Can
                        be including sub-account id. It can contain many
                        different levels to identify the Account. It
                        could include cost centres such as company,
                        division, region, group and branch/department.
                    :ivar analysis: General Ledger analysis codes
                    :ivar customer_id: Unique code for the customer
                    :ivar supplier_id: Unique code for the supplier
                    :ivar tax_point_date: Tax Point date where recorded
                        or if not recorded then the Invoice date
                    :ivar description: Description of the payment line.
                    :ivar debit_credit_indicator: Indicates whether the
                        amounts on line-level are debit or credit
                        amounts. Entry must correspond to entry
                        reflected in General Ledger Entry. Signing of
                        lineamounts is relative to this indicator. E.g.
                        a return can lead to a negative amount.
                    :ivar payment_line_amount: Amount for transaction
                        excluding taxes.
                    :ivar tax_information:
                    """

                    line_number: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LineNumber",
                            "type": "Element",
                            "max_length": 18,
                        },
                    )
                    source_document_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SourceDocumentID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    account_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AccountID",
                            "type": "Element",
                            "max_length": 70,
                        },
                    )
                    analysis: List[AnalysisStructure] = field(
                        default_factory=list,
                        metadata={
                            "name": "Analysis",
                            "type": "Element",
                        },
                    )
                    customer_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CustomerID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    supplier_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    tax_point_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "TaxPointDate",
                            "type": "Element",
                        },
                    )
                    description: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Description",
                            "type": "Element",
                            "max_length": 256,
                        },
                    )
                    debit_credit_indicator: Optional[
                        LineDebitCreditIndicator
                    ] = field(
                        default=None,
                        metadata={
                            "name": "DebitCreditIndicator",
                            "type": "Element",
                            "required": True,
                        },
                    )
                    payment_line_amount: Optional[AmountStructure] = field(
                        default=None,
                        metadata={
                            "name": "PaymentLineAmount",
                            "type": "Element",
                            "required": True,
                        },
                    )
                    tax_information: List[TaxInformationStructure] = field(
                        default_factory=list,
                        metadata={
                            "name": "TaxInformation",
                            "type": "Element",
                        },
                    )

                @dataclass
                class Settlement:
                    """
                    :ivar settlement_discount: Description Settlement /
                        Other Discount
                    :ivar settlement_amount: Settlement amount
                    :ivar settlement_date: Date settled
                    :ivar payment_mechanism: Payment mechanism
                    """

                    settlement_discount: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SettlementDiscount",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    settlement_amount: Optional[AmountStructure] = field(
                        default=None,
                        metadata={
                            "name": "SettlementAmount",
                            "type": "Element",
                        },
                    )
                    settlement_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "SettlementDate",
                            "type": "Element",
                        },
                    )
                    payment_mechanism: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PaymentMechanism",
                            "type": "Element",
                            "max_length": 9,
                        },
                    )

                @dataclass
                class DocumentTotals:
                    """
                    :ivar tax_information_totals: Control totals tax
                        payable information. Per TaxType/TaxCode the
                        TaxBase and TaxAmount are summarised.
                    :ivar net_total: Total amount excluding tax in the
                        header's default currency.
                    :ivar gross_total: Total amount including tax in the
                        header's default currency.
                    """

                    tax_information_totals: List[TaxInformationStructure] = (
                        field(
                            default_factory=list,
                            metadata={
                                "name": "TaxInformationTotals",
                                "type": "Element",
                            },
                        )
                    )
                    net_total: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "NetTotal",
                            "type": "Element",
                            "total_digits": 18,
                            "fraction_digits": 2,
                        },
                    )
                    gross_total: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "GrossTotal",
                            "type": "Element",
                            "required": True,
                            "total_digits": 18,
                            "fraction_digits": 2,
                        },
                    )

        @dataclass
        class MovementOfGoods:
            """
            :ivar number_of_movement_lines: Number of movementlines in
                selected period
            :ivar total_quantity_received: Quantity of goods received
            :ivar total_quantity_issued: Quantity of goods issued in
                selected period
            :ivar stock_movement:
            """

            number_of_movement_lines: Optional[int] = field(
                default=None,
                metadata={
                    "name": "NumberOfMovementLines",
                    "type": "Element",
                    "required": True,
                },
            )
            total_quantity_received: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalQuantityReceived",
                    "type": "Element",
                    "required": True,
                    "total_digits": 22,
                    "fraction_digits": 6,
                },
            )
            total_quantity_issued: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TotalQuantityIssued",
                    "type": "Element",
                    "required": True,
                    "total_digits": 22,
                    "fraction_digits": 6,
                },
            )
            stock_movement: List[
                "AuditFile.SourceDocuments.MovementOfGoods.StockMovement"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "StockMovement",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class StockMovement:
                """
                :ivar movement_reference: Unique reference to the
                    movement.
                :ivar movement_date: Document date
                :ivar movement_posting_date: Date of posting of the
                    movement if different to Movement Date
                :ivar movement_posting_time: Time of posting of the
                    movement
                :ivar tax_point_date: Date of supply of goods
                :ivar movement_type: The movementtype expresses the type
                    of the process for the underlaying lines. E.g.
                    production, sales, purchase. Predescribed TABLE is
                    possible.
                :ivar source_id: Details of person or application that
                    entered the transaction
                :ivar system_id: Unique number created by the system for
                    the document
                :ivar document_reference:
                :ivar line:
                """

                movement_reference: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MovementReference",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                movement_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "MovementDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                movement_posting_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "MovementPostingDate",
                        "type": "Element",
                    },
                )
                movement_posting_time: Optional[XmlTime] = field(
                    default=None,
                    metadata={
                        "name": "MovementPostingTime",
                        "type": "Element",
                    },
                )
                tax_point_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "TaxPointDate",
                        "type": "Element",
                    },
                )
                movement_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MovementType",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                source_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SourceID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                system_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SystemID",
                        "type": "Element",
                        "max_length": 35,
                    },
                )
                document_reference: Optional[
                    "AuditFile.SourceDocuments.MovementOfGoods.StockMovement.DocumentReference"
                ] = field(
                    default=None,
                    metadata={
                        "name": "DocumentReference",
                        "type": "Element",
                    },
                )
                line: List[
                    "AuditFile.SourceDocuments.MovementOfGoods.StockMovement.Line"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "Line",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class DocumentReference:
                    """
                    :ivar document_type: Type of document
                    :ivar document_number: Reference number of the
                        document
                    :ivar document_line: Line number of the document
                    """

                    document_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "DocumentType",
                            "type": "Element",
                            "required": True,
                            "max_length": 18,
                        },
                    )
                    document_number: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "DocumentNumber",
                            "type": "Element",
                            "required": True,
                            "max_length": 35,
                        },
                    )
                    document_line: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "DocumentLine",
                            "type": "Element",
                            "max_length": 18,
                        },
                    )

                @dataclass
                class Line:
                    """
                    :ivar line_number: Number of the movementline
                    :ivar account_id: General Ledger Account code. Can
                        be including sub-account id.
                    :ivar transaction_id: Cross-reference to GL posting.
                        It can contain many different levels to identify
                        the transaction. It could include cost centres
                        such as company, division, region, group and
                        branch/department.
                    :ivar customer_id: Unique code for the customer
                    :ivar supplier_id: Unique code for the supplier
                    :ivar ship_to: Ship To details
                    :ivar ship_from: Ship from Details
                    :ivar product_code: Product code
                    :ivar stock_account_no: Stock batch, lot, serial
                        identification. Not used when there is exactly 1
                        PhysicalStock entry per ProductCode
                    :ivar quantity: Quantity of goods
                    :ivar unit_of_measure: Quantity unit of measure e.g.
                        pack of 12
                    :ivar uomto_uomphysical_stock_conversion_factor:
                        Conversion factor of the UOM to UOM Physical
                        Stock
                    :ivar book_value: Value of the transaction line as
                        registrerd in the general ledger in the header's
                        default currency.
                    :ivar movement_sub_type: Indentify the type of the
                        movement on line / article level. A
                        movement(type) production contains f.i. use of
                        components, getting finished product,
                        efficiencyloss as movementsubtypes. Predescribed
                        TABLE is possible.
                    :ivar movement_comments: A reason for the movement
                    :ivar tax_information:
                    """

                    line_number: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LineNumber",
                            "type": "Element",
                            "required": True,
                            "max_length": 18,
                        },
                    )
                    account_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AccountID",
                            "type": "Element",
                            "max_length": 70,
                        },
                    )
                    transaction_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "TransactionID",
                            "type": "Element",
                            "max_length": 70,
                        },
                    )
                    customer_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CustomerID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    supplier_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    ship_to: Optional[ShippingPointStructure] = field(
                        default=None,
                        metadata={
                            "name": "ShipTo",
                            "type": "Element",
                        },
                    )
                    ship_from: Optional[ShippingPointStructure] = field(
                        default=None,
                        metadata={
                            "name": "ShipFrom",
                            "type": "Element",
                        },
                    )
                    product_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ProductCode",
                            "type": "Element",
                            "required": True,
                            "max_length": 70,
                        },
                    )
                    stock_account_no: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "StockAccountNo",
                            "type": "Element",
                            "max_length": 70,
                        },
                    )
                    quantity: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "Quantity",
                            "type": "Element",
                            "required": True,
                            "total_digits": 22,
                            "fraction_digits": 6,
                        },
                    )
                    unit_of_measure: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "UnitOfMeasure",
                            "type": "Element",
                            "max_length": 9,
                        },
                    )
                    uomto_uomphysical_stock_conversion_factor: Optional[
                        Decimal
                    ] = field(
                        default=None,
                        metadata={
                            "name": "UOMToUOMPhysicalStockConversionFactor",
                            "type": "Element",
                        },
                    )
                    book_value: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "BookValue",
                            "type": "Element",
                            "total_digits": 18,
                            "fraction_digits": 2,
                        },
                    )
                    movement_sub_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MovementSubType",
                            "type": "Element",
                            "required": True,
                            "max_length": 9,
                        },
                    )
                    movement_comments: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MovementComments",
                            "type": "Element",
                            "max_length": 256,
                        },
                    )
                    tax_information: List[TaxInformationStructure] = field(
                        default_factory=list,
                        metadata={
                            "name": "TaxInformation",
                            "type": "Element",
                        },
                    )

        @dataclass
        class AssetTransactions:
            """
            :ivar number_of_asset_transactions: Number of movementlines
                during selected period
            :ivar asset_transaction:
            """

            number_of_asset_transactions: Optional[int] = field(
                default=None,
                metadata={
                    "name": "NumberOfAssetTransactions",
                    "type": "Element",
                    "required": True,
                },
            )
            asset_transaction: List[
                "AuditFile.SourceDocuments.AssetTransactions.AssetTransaction"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "AssetTransaction",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class AssetTransaction:
                """
                :ivar asset_transaction_id: Unique Identification  of
                    the transaction
                :ivar asset_id: Unique identifier of the asset
                :ivar asset_transaction_type: Code for the type of the
                    transaction
                :ivar description: Description of the type of the
                    transaction.
                :ivar asset_transaction_date: Recording date of the
                    transaction type (e. g. assets: date of the addition
                    of the asset)
                :ivar supplier: Information about the supplier of the
                    asset
                :ivar transaction_id: Cross-reference to GL posting in
                    the journal. It can contain many different levels to
                    identify the transaction. It could include cost
                    centres such as company, division, region, group and
                    branch/department.
                :ivar asset_transaction_valuations: These amounts of the
                    transaction can differ per asset valuation type.
                """

                asset_transaction_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AssetTransactionID",
                        "type": "Element",
                        "required": True,
                        "max_length": 70,
                    },
                )
                asset_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AssetID",
                        "type": "Element",
                        "required": True,
                        "max_length": 35,
                    },
                )
                asset_transaction_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "AssetTransactionType",
                        "type": "Element",
                        "required": True,
                        "max_length": 9,
                    },
                )
                description: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "max_length": 256,
                    },
                )
                asset_transaction_date: Optional[XmlDate] = field(
                    default=None,
                    metadata={
                        "name": "AssetTransactionDate",
                        "type": "Element",
                        "required": True,
                    },
                )
                supplier: Optional[
                    "AuditFile.SourceDocuments.AssetTransactions.AssetTransaction.Supplier"
                ] = field(
                    default=None,
                    metadata={
                        "name": "Supplier",
                        "type": "Element",
                    },
                )
                transaction_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "TransactionID",
                        "type": "Element",
                        "max_length": 70,
                    },
                )
                asset_transaction_valuations: Optional[
                    "AuditFile.SourceDocuments.AssetTransactions.AssetTransaction.AssetTransactionValuations"
                ] = field(
                    default=None,
                    metadata={
                        "name": "AssetTransactionValuations",
                        "type": "Element",
                        "required": True,
                    },
                )

                @dataclass
                class Supplier:
                    """
                    :ivar supplier_name: Name of the supplier of the
                        asset
                    :ivar supplier_id: Unique code for the supplier
                    :ivar postal_address: Address information of the
                        supplier of the asset
                    """

                    supplier_name: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierName",
                            "type": "Element",
                            "required": True,
                            "max_length": 70,
                        },
                    )
                    supplier_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SupplierID",
                            "type": "Element",
                            "max_length": 35,
                        },
                    )
                    postal_address: Optional[AddressStructure] = field(
                        default=None,
                        metadata={
                            "name": "PostalAddress",
                            "type": "Element",
                            "required": True,
                        },
                    )

                @dataclass
                class AssetTransactionValuations:
                    asset_transaction_valuation: List[
                        "AuditFile.SourceDocuments.AssetTransactions.AssetTransaction.AssetTransactionValuations.AssetTransactionValuation"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "AssetTransactionValuation",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )

                    @dataclass
                    class AssetTransactionValuation:
                        """
                        :ivar asset_valuation_type: Describes the
                            purpose for the reporting: f.i. commercial,
                            tax  in country 1, tax in country 2, etc.
                        :ivar
                            acquisition_and_production_costs_on_transaction:
                            Costs of acquisition and/or production of
                            related asset transaction in the header's
                            default currency at date of transaction.
                        :ivar book_value_on_transaction: Bookvalue of
                            related asset transaction in the header's
                            default currency at date of transaction.
                        :ivar asset_transaction_amount: Net Amount of
                            related asset transaction in the header's
                            default currency, for instance the net sales
                            revenue.
                        """

                        asset_valuation_type: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "AssetValuationType",
                                "type": "Element",
                                "max_length": 18,
                            },
                        )
                        acquisition_and_production_costs_on_transaction: Optional[
                            Decimal
                        ] = field(
                            default=None,
                            metadata={
                                "name": "AcquisitionAndProductionCostsOnTransaction",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        book_value_on_transaction: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "BookValueOnTransaction",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
                        asset_transaction_amount: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetTransactionAmount",
                                "type": "Element",
                                "required": True,
                                "total_digits": 18,
                                "fraction_digits": 2,
                            },
                        )
