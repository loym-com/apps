from odoo import api, fields, models

class MedicalNoteLog(models.Model):
    _name = "medical.note.log"
    _description = "medical.note.log"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    medical_note_id = fields.Many2one(
        comodel_name="medical.note",
    )
    create_date = fields.Datetime(
    )
    create_uid = fields.Many2one(
        comodel_name="res.users",
    )
