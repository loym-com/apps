from odoo import api, fields

from odoo.addons.spec_driven_model.models import spec_models


class Employee(spec_models.SpecModel):
    _name = "hr.employee"
    _inherit = [
        "hr.employee",
        "amelding.22.inntektsmottaker",
    ]

    amelding22_norskIdentifikator = fields.Char(related="identification_id")

    amelding22_inntektsmottaker_Virksomhet_id = fields.Char(
        related="company_id.login"
    )

    # amelding22_internasjonalIdentifikator
    # amelding22_identifiserendeInformasjon
    # amelding22_arbeidsforhold
    # amelding22_fradrag
    # amelding22_forskuddstrekk
    # amelding22_inntekt
    # amelding22_sjoefolksrelatertInformasjon
    # amelding22_oppholdPaaSvalbardJanMayenOgBilandene
    # amelding22_utleggstrekk
