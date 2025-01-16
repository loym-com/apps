from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo(self):
        records = self._teamm2odoo_set_record()

        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            name = self._teamm2odoo_booking_type_shared()
            self = self.with_context(**{"resource.booking.type": name})
            records |= self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env["teamm"]
        create_event = self.env.context["teamm_params"].get("create_event", "0")
        create_resource = self.env.context["teamm_params"].get("create_resource", "0")
        if int(create_event):
            kwargs["id"] = self.env.ref(
                "event_sale_resource_booking_timeline.resource_booking_type_event"
            ).id
        elif int(create_resource):
            bed_counter = self.env.context.get("teamm_bed_counter", 0)
            room_sharing = self.env.context.get("teamm_room_sharing")
            if bed_counter > 0 and room_sharing == "Share room":
                kwargs["name"] = self._teamm2odoo_booking_type_shared()
        else:
            room = self.env["resource.group"]._teamm2odoo_search()
            type = room.resource_ids.combination_ids.type_rel_ids.type_id
            room_size = len(room.resource_ids)
            if room_size > 1:
                room_sharing = self._teamm2odoo_get_value("room sharing")
                shared_room = self.env.context["teamm_params"]["shared_room"]
                if room_sharing == "Share room":
                    type = type.filtered(lambda t: shared_room in t.name)
                else:
                    type = type.filtered(lambda t: shared_room not in t.name)
                kwargs["id"] = type.id
            else:
                kwargs["id"] = type.id

        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        calendar = self.env.ref("event_sale_resource_booking.resource_calendar")
        kwargs["resource_calendar_id"] = calendar.id
        return super()._teamm2odoo_values(kwargs)

    @api.model
    def _teamm2odoo_booking_type_shared(self):
        shared_room = self.env.context["teamm_params"]["shared_room"]
        name = self._teamm2odoo_name() + " " + shared_room
        return name
