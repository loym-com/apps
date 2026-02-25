Do not use donation.commercial_partner_id, as it is not needed and causes issues with donations to couples.
Instead, use donation.partner_id directly.

A better solution would be change the donation.tax.receipt model to use partner_id instead of commercial_partner_id,
depending on a context variable.
