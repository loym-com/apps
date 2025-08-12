from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    stage_ids = fields.Many2many(
        "project.task.type",
        "project_task_type_rel",
        "project_id",
        "type_id",
        string="Stages",
    )
