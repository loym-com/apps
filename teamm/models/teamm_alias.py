from odoo import api, fields, models
from odoo.exceptions import UserError


class TeammAlias(models.Model):
    _name = "teamm.alias"
    _description = "teamm.alias"
    _order = "note,name"

    note = fields.Char()
    name = fields.Char()
    aliases = fields.Text(help="comma-separated string")
    teamm_id = fields.Many2one("teamm", ondelete="cascade")
    teamm_sequence = fields.Integer(related="teamm_id.sequence")
