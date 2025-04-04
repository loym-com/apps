NEED

Create two types of receipts:

- Thank-you receipts with selected donations.
- Yearly tax receipts with donations of a date interval.

Send newsletter combined with thank-you receipt or yearly tax receipt, considering:

- Language (Norwegian / English)
- Subscription (Newsletter Envelope / Newsletter Email)
- Contact info (has address / email address)
- Content (Tax/Thanks / Newsletter / Both)

At least 12 filters. Tax/Thanks template is different each time, the rest is the same.
Want to save the fixed part of the filters.

Register when something is sent, to avoid sending twice.

Content

- Newsletter (contact tag)
- Thanks (dontations to thank for)
- Yearly tax receipt (donations of a date interval)

CURRENTLY

- Thank-you receipts are registered as tax receipts.
- Filter and select tax receipts: Print letter, or Email Tax Receipt Thanks DIRECTLY.
- Filter and select contacts: Print envelopes (filtering depends on donation_partner).
- Subscriptions are registered as contact tags.

OTHER SYSTEMS

- Solidus has an advanced filtering UI to filter contacts on many different dimensions.
- Solidus has contact snailmail/email/nothing settings for newsletters and magazines.

SOLUTION

Send thank-you letters and yealy tax receipts separately; it is complex to combine them.

Yearly tax receipt

- Use "donation.tax.receipt" and "donation.thanks.template".

Thanks receipt

- Use "donation.donation" and "donation.thanks.template".

Thanks Letter Templates

- New field: model (donation.donation or donation.tax.receipt)
- > On these models, see only templates for that model

Donor favorite filters

- Configure manually filters for often used combinations. Set action_id of Donors.

Donor search (new fields, new search view connected with donor action)

- Use "donation_partner" to filter on contacts to send or not send tax/thanks receipt.
- New fields for donation_partner: donation/tax.receipt: has_thanks_template

Donor actions

- Print envelope

[Move from donation.tax.receipt to res.partner]

- Print donation receipt
- Print tax receipt
- Send donation receipt DIRECTLY
- Send tax receipt DIRECTLY

TODO

Reports should belong to their data model.

Contacts should have two actions, return a window action with domain, ready to print:

- Donations to print
- Donation tax receipts to print

Improve the reports:

- report_donation_donation.odt
- report_donation_tax_receipt.odt

For now, report_donation_tax_receipt.odt works when there is max 1 receipt per contact.
