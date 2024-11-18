import logging

from odoo import _, http
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slugify

# from odoo.addons.http_routing.models.ir_http import _guess_mimetype
from odoo.addons.survey_action.controllers.main import (  # don't replace fill_survey
    Survey2 as SurveyController,
)
from odoo.addons.website_event_sale.controllers.main import (  # inherits (WebsiteEventController)
    WebsiteEventSaleController,
)

_logger = logging.getLogger(__name__)


# class SurveyController2(SurveyController):
#     @http.route()
#     def survey_start(self, survey_token, **post):
#         # MOVE TO event_register()?
#         survey = request.env["survey.survey"].search([("access_token", "=", survey_token)])
#         if survey.event_id:

#             if post.get("answer_token"):
#                 answer_token = post.pop("answer_token")
#             else:
#                 # Create user_input and goto /survey/fill (state != 'new')
#                 vals = {"survey_id": survey.id, "state": "in_progress"}
#                 if request.website.user_id != request.env.user:
#                     vals["partner_id"] = request.env.user.partner_id.id
#                 answer_token = request.env["survey.user_input"].create(vals).access_token

#         return super().survey_start(survey_token, answer_token, **post)


class EventSurveyController(http.Controller):
    def _get_attendees(self, event, **post):

        Input = request.env["survey.user_input"]
        InputLine = request.env["survey.user_input.line"]
        EventTicket = request.env["event.event.ticket"]

        order = request.website.sale_get_order()
        my_input = Input.sudo().search([("order_id", "=", order.id)])
        attendees = []

        for _count, user_input in enumerate(my_input, start=1):
            name = InputLine.search(
                [
                    ("user_input_id", "=", user_input.id),
                    ("question_id", "=", event.registration_name_question_id.id),
                ]
            ).value_char_box
            email = InputLine.search(
                [
                    ("user_input_id", "=", user_input.id),
                    ("question_id", "=", event.registration_email_question_id.id),
                ]
            ).value_char_box
            phone = InputLine.search(
                [
                    ("user_input_id", "=", user_input.id),
                    ("question_id", "=", event.registration_phone_question_id.id),
                ]
            ).value_char_box

            ticket = {}
            ticket_question = event.registration_ticket_question_id
            if ticket_question:
                ticket_answer = InputLine.search(
                    [
                        ("user_input_id", "=", user_input.id),
                        ("question_id", "=", ticket_question.id),
                    ]
                )
                assert (
                    len(ticket_answer) == 1
                ), "There must be exactly one answer to the question %s" % (
                    ticket_question.question
                )
                ticket_survey_label = ticket_answer.suggested_answer_id
                assert ticket_survey_label.id > 0, (
                    "The question '%s' must be of type 'Multiple choice: only one answer'."
                    % (ticket_question.question)
                )
                ticket = EventTicket.search(
                    [
                        ("event_id", "=", event.id),
                        ("survey_label_id", "=", ticket_survey_label.id),
                    ]
                )
                assert (
                    len(ticket) == 1
                ), "The answer '%s' must be set on exactly one event ticket." % (
                    ticket_survey_label.value
                )
            else:
                ticket = EventTicket.search([("event_id", "=", event.id)])
                assert len(ticket) == 1, (
                    "There must be exactly one event ticket, or a survey question "
                    + "with each answer mapped to an event ticket."
                )

            # Prepare products, order by survey label sequence
            # (order by doesn't make so much sense when multiple questions have products)
            user_input_lines = user_input.user_input_line_ids.filtered(
                lambda x: x.suggested_answer_id.product_id
            )
            product_sequence_price = [
                [
                    l.suggested_answer_id.sudo().product_id,
                    l.suggested_answer_id.sequence,
                    l.suggested_answer_id.sudo().product_id.list_price,
                ]
                for l in user_input_lines
            ]
            product_sequence_price.sort(key=lambda p: p[1])

            total_price = ticket.price + sum([p[2] for p in product_sequence_price])

            attendees.append(
                {
                    "name": name,
                    "email": email,
                    "phone": phone if phone else "",
                    "ticket_id": str(ticket.id),
                    "survey_user_input_id": str(user_input.id),
                    "survey_user_input_print_url": str(user_input.answers_url),
                    "survey_user_input_edit_url": str(user_input.answers_url).replace(
                        "print", "edit"
                    ),
                    "survey_user_input_delete_url": str(user_input.answers_url).replace(
                        "print", "delete"
                    ),
                    "event_registration_product_ids": [
                        p[0].id for p in product_sequence_price
                    ],
                    "event_registration_total_price": total_price,
                }
            )
        return attendees

    @http.route(
        [
            "/event/<model('event.event'):event>/registration_survey_list",
            "/event/<model('event.event'):event>/registration_survey_list/"
            + "<string:error_msg>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def registration_survey_list(self, event, error_msg="", **post):
        attendees = self._get_attendees(event, **post)
        if not attendees:
            return request.redirect("/event/%s/register" % slugify(event))

        total_price = sum([a["event_registration_total_price"] for a in attendees])
        data = {
            "attendees": attendees,
            "total_price": total_price,
            "event": event,
            "error_msg": error_msg,
        }
        return request.render("event_survey.registration_survey_list", data)

    @http.route(
        ["/event/<model('event.event'):event>/registration_survey_list/confirm"],
        type="http",
        auth="public",
        website=True,
    )
    def registration_survey_list_confirm(self, event, **post):

        order = request.website.sale_get_order()
        OrderLine = request.env["sale.order.line"]
        Registration = request.env["event.registration"]

        # validation with server action
        action = event.registration_validation_action_id
        user = event.company_id.user_tech_id
        if action and action.state == "code" and action.website_published:
            error_msg = (
                action.with_context(active_id=order.id, active_model="sale.order")
                .sudo(user)
                .run()
            )
            if error_msg:
                return request.redirect(
                    "/event/%s/registration_survey_list/%s"
                    % (slugify(event), error_msg)
                )

        # delete previously registered attendees on this sales order,
        # and event-related products in the shopping cart
        Registration.sudo().search([("sale_order_id", "=", order.id)]).unlink()
        tickets = event.event_ticket_ids
        labels = (
            request.env["survey.question.answer"]
            .search([])
            .filtered(
                lambda l: l.question_id.page_id.survey_id.event_id == event
                and l.product_id
            )
        )
        product_ids = [t.product_id.id for t in tickets] + [
            l.product_id.id for l in labels
        ]
        OrderLine.sudo().search(
            [("order_id", "=", order.id), ("product_id", "in", product_ids)]
        ).unlink()

        # event partner > public partner (to skip address)
        if order.partner_id == event.registration_partner_id:
            order.partner_id = request.website.user_id.sudo().partner_id.id

        # get attendees
        attendees = self._get_attendees(event, **post)
        for count, attendee in enumerate(attendees, start=1):
            i = str(count) + "-"
            post.update({i + k: v for k, v in attendee.items()})

        # Take the user to the next step (confirmation or payment)
        controller = WebsiteEventSaleController2()
        return controller.registration_confirm(event, **post)

    @http.route(
        ["/survey/edit/<model('survey.survey'):survey>/<string:token>"],
        type="http",
        auth="public",
        website=True,
    )
    def edit(self, survey, token, **post):
        domain = [("access_token", "=", token), ("survey_id", "=", survey.id)]
        user_input = request.env["survey.user_input"].search(domain)
        if user_input:
            user_input.ensure_one()
            if user_input.sudo().order_id.state == "draft":
                user_input.state = "new"
                return request.redirect("/survey/fill/%s/%s" % (survey.id, token))
            else:
                return request.redirect(
                    "/event/%s/registration_survey_list" % slugify(survey.event_id)
                )

    @http.route(
        ["/survey/delete/<model('survey.survey'):survey>/<string:token>"],
        type="http",
        auth="public",
        website=True,
    )
    def delete(self, survey, token, **post):
        domain = [("access_token", "=", token), ("survey_id", "=", survey.id)]
        user_input = request.env["survey.user_input"].search(domain)
        for myinput in user_input:
            if myinput.sudo().order_id.state == "draft":
                myinput.sudo().unlink()

        return request.redirect(
            "/event/%s/registration_survey_list" % slugify(survey.event_id)
        )


class WebsiteEventSaleController2(WebsiteEventSaleController):
    @http.route()
    def event_register(self, event, **post):

        if event.registration_survey_id:

            # Start survey
            controller = SurveyController()
            return controller.survey_start(event.registration_survey_id.access_token, **post)

        return super().event_register(event, **post)

    # from website_event_sale
    @http.route()
    def registration_confirm(self, event, **post):
        order = request.website.sale_get_order(force_create=1)
        attendee_ids = set()

        registrations = self._process_registration_details(post)
        for registration in registrations:
            ticket = (
                request.env["event.event.ticket"]
                .sudo()
                .browse(int(registration["ticket_id"]))
            )
            cart_values = order.with_context(
                event_ticket_id=ticket.id, fixed_price=True
            )._cart_update(
                product_id=ticket.product_id.id,
                add_qty=1,
                registration_data=[registration],
            )
            attendee_ids |= set(cart_values.get("attendee_ids", []))

        # NEW ############################################################

        note = _("Attendees:\n")
        for registration in registrations:

            # Add name to sales order note
            note += "%s (%s)\n" % (registration["name"], registration["email"])

            # Add products to cart in the end
            product_ids = registration.get("event_registration_product_ids")
            if product_ids and any(product_ids):
                for product_id in product_ids:
                    order._cart_update(product_id=product_id, add_qty=1)
        order.note = note

        # END ############################################################

        # free tickets -> order with amount = 0: auto-confirm, no checkout
        if not order.amount_total:
            order.action_confirm()  # tde notsure: email sending ?
            attendees = (
                request.env["event.registration"].browse(list(attendee_ids)).sudo()
            )
            # clean context and session, then redirect to the confirmation page
            request.website.sale_reset()
            return request.render(
                "website_event.registration_complete",
                {
                    "attendees": attendees,
                    "event": event,
                },
            )

        # NEW ############################################################

        if order.partner_id.id == request.website.partner_id.id:
            partner = event.registration_partner_id
            if partner and partner.country_id:

                # set partner, skip address
                order.write(
                    {
                        "partner_id": partner.id,
                        "partner_invoice_id": partner.id,
                        "partner_shipping_id": partner.id,
                    }
                )
                return request.redirect("/shop/checkout?express=1")

        # END ############################################################

        return request.redirect("/shop/checkout")
