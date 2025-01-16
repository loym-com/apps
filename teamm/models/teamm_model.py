from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMModel(models.Model):
    _name = "teamm.model"
    _description = "teamm.model"
    _order = "sequence"

    teamm_id = fields.Many2one("teamm", ondelete="cascade")
    sequence = fields.Integer()
    is_active = fields.Boolean()
    name = fields.Char()
    description = fields.Text()
    primary_key = fields.Text()
    values = fields.Text()
