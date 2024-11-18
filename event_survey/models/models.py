import logging

from odoo import fields, models

from odoo.addons.http_routing.models.ir_http import slugify

# from odoo.addons.http_routing.models.ir_http import _guess_mimetype


_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _inherit = "event.event"

    registration_survey = fields.Boolean("Registration Survey")
    registration_survey_id = fields.Many2one("survey.survey", "Survey")
    registration_partner_id = fields.Many2one(
        "res.partner",
        "Customer",
        help="Public users (no login) will skip address to simplify the payment. "
            "This partner will be used for the sales order.",
    )
    registration_name_question_id = fields.Many2one(
        "survey.question",
        "Question: Name",
        help="Single line text box. Mandatory answer.",
    )
    registration_email_question_id = fields.Many2one(
        "survey.question",
        "Question: Email",
        help="Single line text box. Mandatory answer. Input must be an email.",
    )
    registration_phone_question_id = fields.Many2one(
        "survey.question", "Question: Phone", help="Single line text box."
    )
    registration_ticket_question_id = fields.Many2one(
        "survey.question",
        "Question: Ticket",
        help="Multiple choice: only one answer. Mandatory answer. "
            "BUG: Creating new ticket will set this field blank.",
    )
    registration_products_question_id = fields.Many2one(
        "survey.question",
        "Question: Products",
        help="Multiple choice: multiple answers allowed.",
    )
    registration_products_suggested_answer_ids = fields.One2many(
        "survey.question.answer",
        "question_id",
        "Question: Product Labels",
        related="registration_products_question_id.suggested_answer_ids",
    )
    registration_validation_action_id = fields.Many2one(
        "ir.actions.server", "Validation Action"
    )

    # copied from website_event/models/event.py 12.0
    # is_participating = fields.Boolean("Is Participating", compute="_compute_is_participating")
    # def _compute_is_participating(self):
    #     # we don't allow public user to see participating label
    #     if self.env.user != self.env['website'].get_current_website().user_id:
    #         email = self.env.user.partner_id.email
    #         for event in self:
    #             domain = ['&','&', '|', ('email', '=', email),
    #               ('partner_id', '=', self.env.user.partner_id.id),
    #                       ('event_id', '=', event.id), ('state', '!=', 'cancel')]
    #             event.is_participating = self.env[
    #               'event.registration'
    #             ].sudo().search_count(domain)

    _sql_constraints = [
        (
            "registration_survey_uniq",
            "unique (registration_survey_id)",
            "Each registration survey must be unique.",
        ),
    ]


class EventRegistration(models.Model):
    _inherit = "event.registration"

    survey_user_input_id = fields.Many2one("survey.user_input", string="Survey Answers")
    survey_user_input_print_url = fields.Char(
        string="Survey Answers URL", related="survey_user_input_id.answers_url"
    )

    # Was used when the event registration came BEFORE the survey.
    # @api.model
    # def create(self, vals):
    #    event = self.env['event.event'].browse(vals['event_id'])
    #    if event.registration_survey_id.id:
    #        survey_user_input = self.env['survey.user_input'].create(
    #           {
    #               'survey_id': event.registration_survey_id.id,
    #               'type': 'link'
    #           }
    #        ) # 'link' will avoid auto-vacuum
    #        vals['survey_user_input_id'] = survey_user_input.id
    #    registration = super(EventRegistration, self).create(vals)
    #    return registration


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    survey_question_id = fields.Many2one(
        "survey.question",
        "Survey Ticket Question",
        related="event_id.registration_ticket_question_id",
    )
    survey_label_id = fields.Many2one("survey.question.answer", "Survey Ticket")


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    product_id = fields.Many2one("product.template", "Product")
    product_list_price = fields.Float("List Price", related="product_id.list_price")


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    # fill_url = fields.Char('Public link with token for user input',
    #   compute='_compute_fill_url')
    order_id = fields.Many2one(
        "sale.order", "Sales Order", help="Do multiple surveys before "
    )
    # state = fields.Selection(
    #     selection_add=[("new_event_registration", "New Event Registration")]
    # )

    # Was used when the event registration came BEFORE the survey.
    # @api.one
    # def _compute_fill_url(self):
    #    self.fill_url = "/survey/fill/%s/%s" % (slugify(self.survey_id), self.token)
    #    return self.fill_url

    # slug is not working (v12)
    # used by event.registration survey_user_input_print_url
    # used by controller
    answers_url = fields.Char("Answers URL", compute="_compute_answers_url")

    def _compute_answers_url(self):
        for record in self:
            record.answers_url = "/survey/print/%s/%s" % (
                slugify(self.survey_id),
                self.access_token,
            )


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def _compute_event(self):
        for record in self:
            record.event_id = self.env["event.event"].search(
                [("registration_survey_id", "=", record.id)]
            )

    event_id = fields.Many2one("event.event", "Event", compute="_compute_event")
