from odoo import api, fields, models

class MedicalNote(models.Model):
    _name = "medical.note"
    _description = "medical.note"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    contact_id = fields.Many2one(
        comodel_name="res.partner",
    )
    log_ids = fields.One2many(
        comodel_name="medical.note.log",
        inverse_name="medical_note_id",
    )
