import logging
from datetime import datetime

from odoo import _, fields, models
from odoo.exceptions import UserError

from .amelding import amelding_logic

#   File "C:\o150\.venv\Lib\site-packages\pyxb\binding\content.py", line 807, in <module>
#     class _PluralBinding (collections.MutableSequence):
# AttributeError: module 'collections' has no attribute 'MutableSequence'
# Should be "collections.abc.MutableSequence"

_logger = logging.getLogger(__name__)


class AmeldingWizard(models.TransientModel):
    _name = "l10n.no.amelding.wizard"
    _description = "Lag A-melding"

    kalendermaaned = fields.Char()

    def lag_amelding(self):
        # Verify period
        try:
            datetime.strptime(self.kalendermaaned + "-01", "%Y-%m-%d")
        except:
            raise UserError(_("The period should have this format: yyyy-mm"))

        # Look for existing amelding record
        company_id = self.env.company.id
        record = self.env["l10n.no.amelding"].search(
            [
                ("kalendermaaned", "=", self.kalendermaaned),
                ("company_id", "=", company_id),
            ],
            order="id desc",
            limit=1,
        )
        if record and record.state == "new":
            record.leveringstidspunkt = datetime.now()
        else:
            # Create amelding record
            d = {}
            if record:
                d["erstatterMeldingsId"] = record.meldingsId
            d["kalendermaaned"] = self.kalendermaaned
            d["leveringstidspunkt"] = datetime.now()

            record = self.env["l10n.no.amelding"].create(d)

        logic = amelding_logic.AmeldingLogikk(record)
        record.amelding = logic.melding_xml()
        return {
            "type": "ir.actions.act_window",
            "res_model": "l10n.no.amelding",
            "res_id": record.id,
            "view_mode": "form",
        }
