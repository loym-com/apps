from odoo import _, api, fields, models


class ResourceBookingCombination(models.Model):
    _inherit = "resource.booking.combination"

    @api.model
    def _teamm2odoo(self):
        records = self

        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            # A record for each bed
            for i in range(int(beds)):
                self_shared_room = self.with_context(
                    teamm_bed_counter=i+1,
                    teamm_room_sharing="Share room",
                )
                records |= self_shared_room._teamm2odoo_set_record()
            # A record for all beds
            self_private_room = self.with_context(
                teamm_room_sharing="Private",
            )
            records |= self_private_room._teamm2odoo_set_record()
        else:
            # A record for the room
            records |= self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        room = self.env["resource.group"]._teamm2odoo_search()
        room_size = len(room.resource_ids)
        room_sharing = self.env.context.get("teamm_room_sharing")
        if room_size > 1:
            if room_sharing == "Share room":
                resources = self.env["resource.resource"]._teamm2odoo_search()
            else:
                resources = self.env["resource.group"]._teamm2odoo_search().resource_ids
        else:
            resources = self.env["resource.resource"]._teamm2odoo_search()
        kwargs["resource_ids"] = resources.ids
        return super()._teamm2odoo_search_kwargs(kwargs)
