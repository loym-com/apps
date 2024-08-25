from odoo import api, fields, models


class MedicalNote(models.Model):
    _inherit = "medical.note"

    sensitive_note = fields.Text()

    def read(self, fields=None, load='_classic_read'):
        if fields and "sensitive_note" in fields:
            for record in self:
                self.env["medical.note.log"].sudo().create({"medical_note_id": record.id})
        return super().read(fields, load)
