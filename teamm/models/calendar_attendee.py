from odoo import models, fields, api

""" DO NOT SEND MEETING INVITATIONS TO GUESTS WHEN THEY BOOK A STAY. """


class CalendarAttendee(models.Model):
    _inherit = "calendar.attendee"

    def _send_mail_to_attendees(self, mail_template, force_send=False):
        return
