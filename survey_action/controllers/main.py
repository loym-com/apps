import json
import logging

from odoo import SUPERUSER_ID, http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey

_logger = logging.getLogger(__name__)


class Survey2(Survey):

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        if answer_sudo.state == 'done':
            action = survey_sudo.server_action_id
            if action:
                redirect_url = (
                    action.with_context(
                        active_id=answer_sudo.id,
                        active_model="survey.user_input",
                        # website_id=request.website.id, # depends on website module
                    )
                    .run()
                )
                if redirect_url:
                    post["redirect_url"] = redirect_url
        return super()._prepare_question_html(survey_sudo, answer_sudo, **post)

    def _prepare_survey_data(survey_sudo, answer_sudo, **post):
        data = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        data["redirect_url"] = post["redirect_url"]
        return data

    # TODO
    # Override QWeb 'survey.survey_fill_form_done' to include "redirect_url".
    # - survey_templates.xml
    # Use javascript to get the redirect_url and redirect to that url.
    # - How?
