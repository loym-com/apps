from odoo import models, fields, api

""" DO NOT SEND MEETING INVITATIONS TO GUESTS WHEN THEY BOOK A STAY. """


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    @api.model_create_multi
    def create(self, vals_list):
        return super().with_context(skip_attendee_notification=True).create(vals_list)

    def write(self, vals):
        return super().with_context(skip_attendee_notification=True).create(vals)
