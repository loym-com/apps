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
                return_action = (
                    action.with_context(
                        active_id=answer_sudo.id,
                        active_model="survey.user_input",
                        # website_id=request.website.id, # depends on website module
                    )
                    .run()
                )
                if return_action:
                    return return_action
                    # Nothing happens with the action
                    # {
                    #     "jsonrpc": "2.0",
                    #     "id": 1,
                    #     "result": {
                    #         "type": "ir.actions.act_url",
                    #         "url": "/event/332/registration_survey_list",
                    #         "target": "self"
                    #     }
                    # }

        return super()._prepare_question_html(survey_sudo, answer_sudo, **post)
