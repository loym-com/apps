from odoo import models, fields, api

""" DO NOT SEND MEETING INVITATIONS TO GUESTS WHEN THEY BOOK A STAY. """


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    @api.model_create_multi
    def create(self, vals_list):
        self = self.with_context(skip_attendee_notification=True)
        return super().create(vals_list)

    def write(self, vals):
        self = self.with_context(skip_attendee_notification=True)
        return super().write(vals)
