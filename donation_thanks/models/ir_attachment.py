from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _get_lang(self):
        return self.env['res.lang'].get_installed()

    lang = fields.Selection(_get_lang, string='Language')
