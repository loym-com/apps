from odoo import _, api, fields, models


class ResourceBookingTypeCombinationRel(models.Model):
    _inherit = "resource.booking.type.combination.rel"

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
        kwargs |= {
            "type_id": self.env["resource.booking.type"]._teamm2odoo_search().id,
            "combination_id": self.env["resource.booking.combination"]._teamm2odoo_search().id,
        }
        return super()._teamm2odoo_search_kwargs(kwargs)
