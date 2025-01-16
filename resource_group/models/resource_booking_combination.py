from odoo import _, api, fields, models

class ResourceBookingCombination(models.Model):
    _inherit = "resource.booking.combination"

    name = fields.Char(compute="_compute_name", store=True)

    @api.depends("resource_ids.name", "forced_calendar_id.name", "resource_ids.group_id.name")
    def _compute_name(self):
        for one in self:
            if one.resource_ids.group_id.resource_ids == one.resource_ids:
                resources = one.resource_ids.group_id.mapped("name")
            else:
                resources = one.resource_ids.mapped("name")
            data = {
                "resources": " + ".join(sorted(
                    resources
                    # one.resource_ids.mapped("group_id").mapped("name") or one.resource_ids.mapped("name")
                )),
                "calendar": one.forced_calendar_id.name,
            }

            if one.forced_calendar_id:
                one.name = _("%(resources)s (using calendar %(calendar)s)") % data
            else:
                one.name = _("%(resources)s") % data
