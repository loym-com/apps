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
        string="Resource ID",
    )
    code_list_id = fields.Many2one(
        comodel_name="code.list",
    )
    code_list_item_id = fields.Many2one(
        comodel_name="code.list.item",
    )
    note = fields.Text()
    resource_id = fields.Reference(
        selection=[('res.partner', 'Contacts')],
        string="Resource",
        compute="_compute_resource_id",
        inverse="_inverse_resource_id",
        store=True,
    )

    @api.depends("model", "res_id")
    def _compute_resource_id(self):
        for record in self:
            if record.model and record.res_id:
                record.resource_id = f"{record.model},{record.res_id}"
            else:
                record.resource_id = False

    def _inverse_resource_id(self):
        for record in self:
            if record.resource_id:
                record.model = record.resource_id._name
                record.res_id = record.resource_id.id
            else:
                record.model = False
                record.res_id = False
