from datetime import datetime

from odoo.tests.common import TransactionCase


class TestNoPayrollBase(TransactionCase):
    def setUp(self):
        super(TestNoPayrollBase, self).setUp()

        self.company = self.env.ref("base.main_company")
        self.company.write(
            {
                "l10n_no_Grunnlagsprosent": "14.1",
                "vat": "NO913860128",
                "l10n_no_virksomhet": "913864042",
                "l10n_no_Spraak": "bokmaal",
                "l10n_no_BeregningskodeForArbeidsgiveravgift": "generelleNaeringer",
                "l10n_no_Arbeidsgiveravgiftsone": "1",
                "l10n_no_fp_prosent": 10.2,
                "l10n_no_fp_prosent_senior": 12.5,
                "l10n_no_pensjonsinnretning": "958995369",
                "l10n_no_aga_konto": self.env.ref("l10n_no.1_chart5400").id,
                "l10n_no_aga_motkonto": self.env.ref("l10n_no.1_chart2770").id,
                "l10n_no_fp_konto": self.env.ref("l10n_no.1_chart5092").id,
                "l10n_no_fp_motkonto": self.env.ref("l10n_no.1_chart2940").id,
                "l10n_no_aga_fp_konto": self.env.ref("l10n_no.1_chart5405").id,
                "l10n_no_aga_fp_motkonto": self.env.ref("l10n_no.1_chart2785").id,
                "l10n_no_loennsart_fp_i_aar": self.env.ref(
                    "l10n_no_payroll.rule_fp_i_aar"
                ).id,
                "l10n_no_loennsart_fp_i_fjor": self.env.ref(
                    "l10n_no_payroll.rule_fp_i_fjor"
                ).id,
            }
        )

        self.job = self.env["hr.job"].create(
            [
                {
                    "name": "ALTMULIGMANN (PRIVATHJEM)",
                    "l10n_no_job_code": self.env["l10n.no.job.code"].search(
                        [("code", "=", "9120105")]
                    ),
                }
            ],
        )

        self.employee = self.env["hr.employee"].create(
            [
                {
                    "name": "Ola Nordmann",
                    "birthday": datetime(2000, 1, 1).date(),
                    # "l10n_no_trekktabell": "7100",
                    "l10n_no_trekkprosent": 32,
                    # "l10n_no_fribeloep": 55000,
                }
            ],
        )

        self.contract = self.env["hr.contract"].create(
            [
                {
                    "name": "Test contract for {}".format(self.employee.name),
                    "employee_id": self.employee.id,
                    "job_id": self.job.id,
                    "struct_id": self.env.ref("l10n_no_payroll.structure_no").id,
                    "date_start": datetime(2023, 1, 1).date(),
                    "date_end": datetime(2023, 12, 31).date(),
                    "wage": 0,
                    "l10n_no_Arbeidsforholdtype": "ordinaertArbeidsforhold",
                    "l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer": 37.5,
                    "l10n_no_Arbeidstidsordning": "ikkeSkift",
                    "l10n_no_FormForAnsettelse": "fast",
                    "l10n_no_loennsansiennitet": datetime(2023, 1, 1).date(),
                    "l10n_no_loennstrinn": "20",
                    "l10n_no_sisteDatoForStillingsprosentendring": datetime(
                        2023, 1, 1
                    ).date(),
                    "l10n_no_sisteLoennsendringsdato": datetime(2023, 1, 1).date(),
                    "l10n_no_stillingsprosent": 100,
                    "l10n_no_AarsakTilSluttdato": "kontraktEngasjementEllerVikariatErUtloept",
                },
            ]
        )
