from odoo import fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    leave_ids = fields.One2many("hr.leave", "contract_id", string="Leaves")

    def l10n_no_action_new_leave(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.leave",
            "views": [[False, "form"]],
            "context": "{'default_employee_id': %d,'default_contract_id': %d}"
            % (self.employee_id.id, self.id),
        }

    json = fields.Serialized()
    l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer = fields.Float(
        "Antall timer per uke som en full stilling tilsvarer", sparse="json"
    )
    l10n_no_Arbeidsforholdtype = fields.Selection(
        string="Type arbeidsforhold",
        sparse="json",
        selection=[
            ("frilanserOppdragstakerHonorarPersonerMm", "frilanserOppdragstakerHonorarPersonerMm"),
            ("maritimtArbeidsforhold", "maritimtArbeidsforhold"),
            ("ordinaertArbeidsforhold", "ordinaertArbeidsforhold"),
            ("pensjonOgAndreTyperYtelserUtenAnsettelsesforhold", "pensjonOgAndreTyperYtelserUtenAnsettelsesforhold"),
        ],
    )
    l10n_no_Arbeidstidsordning = fields.Selection(
        string="Arbeidstidsordning",
        sparse="json",
        selection=[
            ("offshore336", "offshore336"),
            ("doegnkontinuerligSkiftOgTurnus355", "doegnkontinuerligSkiftOgTurnus355"),
            ("helkontinuerligSkiftOgAndreOrdninger336", "helkontinuerligSkiftOgAndreOrdninger336"),
            ("ikkeSkift", "ikkeSkift"),
            ("skift365", "skift365"),
        ],
    )
    l10n_no_FormForAnsettelse = fields.Selection(
        string="Form for ansettelse",
        sparse="json",
        selection=[
            ("fast", "Fast ansettelse"),
            ("midlertidig", "Midlertidig ansettelse"),
            ("fastAnsattUtleid", "Fast ansatt utleid"),
            ("midlertidigAnsattUtleid", "Midlertidig ansatt utleid"),
            ("midlertidigAnsattSomTilkallingsvikar", "Midlertidig ansatt som tilkallingsvikar"),
        ],
    )
    l10n_no_loennsansiennitet = fields.Date("Dato for lønnsansiennitet", sparse="json")
    l10n_no_loennstrinn = fields.Char("Loennstrinn", sparse="json")
    l10n_no_sisteDatoForStillingsprosentendring = fields.Date(
        "Dato for siste stillingsprosentendring", sparse="json"
    )
    l10n_no_sisteLoennsendringsdato = fields.Date(
        "Dato for siste lønnsendring", sparse="json"
    )
    l10n_no_stillingsprosent = fields.Float("Stillingsprosent", sparse="json")
    l10n_no_AarsakTilSluttdato = fields.Selection(
        string="Årsak til sluttdato",
        sparse="json",
        selection=[
            ("arbeidsforholdetSkulleAldriVaertRapportert", "Arbeidsforholdet skulle aldri vært rapportert"),
            ("arbeidsgiverHarSagtOppArbeidstaker", "Arbeidsgiver har sagt opp arbeidstaker"),
            ("arbeidstakerHarSagtOppSelv", "Arbeidstaker har sagt opp selv"),
            ("byttetLoenssystemEllerRegnskapsfoerer", "Byttet lønnssystem eller regnskapsfører"),
            ("endringIOrganisasjonsstrukturEllerByttetJobbInternt", "Endring i organisasjonsstruktur eller byttet jobb internt"),
            ("kontraktEngasjementEllerVikariatErUtloept", "Kontrakt, engasjement eller vikariat er utløpt"),
        ],
    )
