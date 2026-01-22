from odoo import api, fields, models

class CodeListUsage(models.Model):
    _name = "code.list.usage"
    _description = "code.list.usage"
    _sql_constraints = [
        # Consider code_list_uniq (only one usage of a code list per resource)
        (
            "code_list_item_uniq",
            "unique(model, res_id, code_list_item_id)",
            "The code list item can be linked only once to the same resource!",
        ),
    ]

    model = fields.Char()
    res_id = fields.Many2oneReference(
        model_field="model",
        string="Resource",
    )
    code_list_id = fields.Many2one(
        comodel_name="code.list",
    )
    code_list_item_id = fields.Many2one(
        comodel_name="code.list.item",
    )
