from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    # Based on https://github.com/OCA/server-tools/blob/11.0/mail_template_attachment_i18n/models/mail_template.py
    # That module has mail.template one2many ir.attachment.language
    # This module has donation.thanks.template one2many ir.attachment (with lang field).
    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        multi = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi = False
        res = super().generate_email(
            res_ids, fields
        )

        if not self.model == "donation.tax.receipt":
            return res

        attached = []
        for res_id in res.keys():
            mail = res[res_id]
            partner_ids = 'partner_ids' in mail and \
                          mail['partner_ids'] or False
            if not partner_ids:
                continue

            thanks_template = self.env["donation.tax.receipt"].browse(res_id).thanks_template_id

            for partner in self.env['res.partner'].browse(partner_ids):
                for attachment in thanks_template.attachment_ids.filtered(
                    lambda a: a.lang == partner.lang
                ):
                    if attachment.id in attached:
                        continue
                    if not res[res_id].get('attachments'):
                        res[res_id]['attachments'] = []
                    res[res_id]['attachments'].append((
                        attachment.name,
                        attachment.datas))
                    attached.append(attachment.id)
        return multi and res or res[res_ids[0]]
