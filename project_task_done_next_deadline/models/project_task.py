import datetime

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_done = fields.Date(
        string="Done",
    )
    frequency = fields.Selection(
        selection=[
            ('day', 'Daily'),
            ('week', 'Weekly'),
            ('month', 'Monthly'),
            ('year', 'Yearly'),
        ],
        string="Frequency",
    )

    def action_project_task_done_next_deadline(self):

        # Function to get next deadline
        def _get_next_deadline(deadline, frequency):
            if not deadline:
                deadline = datetime.date.today()

            if deadline > datetime.date.today():
                return deadline

            if frequency == 'day':
                return deadline + datetime.timedelta(days=1)
            elif frequency == 'week':
                return deadline + datetime.timedelta(weeks=1)
            elif frequency == 'month':
                # Add one month, handling year rollover
                year = deadline.year + (deadline.month // 12)
                month = deadline.month % 12 + 1
                day = min(deadline.day, 28)
                return datetime.date(year, month, day)
            elif frequency == 'year':
                # Handle February 29th on non-leap years
                return deadline.replace(day=min(deadline.day, 28), year=deadline.year + 1)
            else:
                return False

        # Main
        self.ensure_one()
        self.write({'date_done': datetime.date.today()})
        deadline = _get_next_deadline(self.date_deadline, self.frequency)
        if deadline:
            self.write({'date_deadline': deadline})
