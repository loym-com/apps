from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMParam(models.Model):
    _name = "teamm.param"
    _description = "teamm.param"

    teamm_id = fields.Many2one("teamm", required=True)
    type = fields.Selection([("api", "API"), ("code", "Code")], required=True)
    key = fields.Char()
    value = fields.Char()
