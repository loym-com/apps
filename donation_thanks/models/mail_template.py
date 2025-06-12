from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    # Based on https://github.com/OCA/server-tools/blob/11.0/mail_template_attachment_i18n/models/mail_template.py
    # That module has mail.template one2many ir.attachment.language
    # This module has donation.thanks.template one2many ir.attachment (with lang field).
    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        email = super().generate_email(res_ids, fields)

        if self.model in ("donation.thanks", "donation.tax.receipt"):

            # assert len(res_ids) == 1, \
            #     "This method should only be called with a single res_id"

            # assert res_ids = email['res_id'], \
            #     "The res_id in the email should match the res_ids provided"

            # email["attachments"] = email.get("attachments", [])

            model_record = self.env[self.model].browse(res_ids)
            thanks_template = model_record.thanks_template_id
            lang = model_record.partner_id.lang

            # Add thanks_template attachments based on the language of the partner
            for attachment in thanks_template.attachment_ids.filtered(
                lambda a: a.lang == lang
            ):
                email["attachments"].append((attachment.name, attachment.datas))

        return email
