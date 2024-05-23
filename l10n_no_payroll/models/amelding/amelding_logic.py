import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo.exceptions import UserError

from . import amelding_v2_2 as a

_logger = logging.getLogger(__name__)


"""
a = amelding_v2_2
af = Arbeidsforhold
aga = Arbeidsgiveravgift
agag = Arbeidsgiveravgiftsgrunnlag
bi = Betalingsinformasjon
bif = BetalingsinformasjonForForenkletOrdning
fraig = FradragIGrunnlagetForSone
fra = Fradrag
ft = Forskuddstrekk
inn = Inntekt
ii = InternasjonalIdentifikator
im = Inntektsmottaker
je = JuridiskEntitet
lev = Leveranse
m = Melding
opphold = OppholdPaaSvalbardJanMayenOgBilandene
p = Permisjon
v = Virksomhet

parent = object
for element in sequence:
    child, info = f(element)
    parent.total = not_None(parent.total) + info['total']
"""


def _debug(my_input):
    # _logger.debug(str(my_input))
    # print(str(my_input))
    pass


def not_None(variable):
    if variable is None:
        return 0
    else:
        return variable


class AmeldingLogikk:
    def __init__(self, amelding_record):
        self.amelding_record = amelding_record

        period = self._get(self.amelding_record, "kalendermaaned")
        date_from = datetime.strptime(period + "-01", "%Y-%m-%d")
        self.date_from = date_from.date()
        date_to = date_from + relativedelta(day=31)
        self.date_to = date_to.date()
        self.company = self._get(self.amelding_record, "company_id")
        company_id = self._get(self.company, "id")
        self.employees = self._get_records(
            "hr.employee",
            [("company_id", "=", company_id), ("active", "=", True)],
            self.company,
        )
        self.contracts = self._get_records(
            "hr.contract", [("company_id", "=", company_id)], self.company
        )
        self.payslips = self._get_records(
            "hr.payslip",
            [
                ("company_id", "=", company_id),
                ("date_to", ">=", date_from),
                ("date_to", "<=", date_to),
            ],
            self.company,
        )
        self.payslip_lines = self._get_records(
            "hr.payslip.line",
            [("slip_id", "in", self._mapped(self.payslips, "id"))],
            self.company,
        )
        self.payslip_runs = self.payslips.mapped("payslip_run_id")
        # self.salary_rules = self._get_records('hr.salary.rule', [], self.company) # hr.payslip.line.salary_rule_id
        self.countries = self._get_records("res.country", [], self.company)
        self.jobs = self._get_records(
            "hr.job", [("company_id", "=", company_id)], self.company
        )

        models = [
            "hr.contract",
            "hr.employee",
            "hr.job",
            "hr.leave.type",
            "hr.payslip",
            "hr.payslip.line",
            "hr.payslip.run",
            "hr.salary.rule",
            "res.company",
        ]
        # self.field_values = self._get_records(
        #     "res.field.value",
        #     [("company_id", "=", company_id), ("model", "in", models)],
        #     self.company,
        # )
        # self.field_selection_values = self._get_records(
        #     "res.field.selection_value", [], self.company
        # )  # security rule: 1_or_company_id

        self.je = {
            "annenBagatellmessigStoette": 0,
            "sumForskuddstrekk": 0,
            "sumArbeidsgiveravgift": 0,
            "sumFinansskattLoenn": 0,
            "sumUtleggstrekk": 0,
            "sumForskuddstrekkForenklet": 0,
            "sumArbeidsgiveravgiftForenklet": 0,
        }
        self.aga = {
            "avgiftsgrunnlagBeloep": 0,
            "avgiftsgrunnlagBeloepPensjon": 0,
            "avgiftsgrunnlagBeloepSaerskiltProsentsats": 0,
            "antallAvgiftsgrunnlagPersonerFastBeloep": 0,
            "avgiftsfradragBeloep": 0,
            "avgiftsfradragBeloepSaerskiltProsentsats": 0,
        }

    def melding_xml(self):
        m = self.melding2()
        # raise UserError(m)
        # Melding(leveranse=None)

        myxml = m.toxml("utf-8")
        myetree = etree.fromstring(myxml)

        no_of_times = 5  # Do a few times to remove nested empty nodes
        for i in range(0, no_of_times):
            for element in myetree.xpath("//*[not(node())]"):
                element.getparent().remove(element)

        mypretty = etree.tostring(myetree, pretty_print=True)
        return mypretty

    def melding2(self):
        m = a.Melding()
        m.Leveranse = a.Leveranse()
        return m

    def melding(self):
        m = a.melding()
        m.Leveranse = self.Leveranse()
        return m

    def Leveranse(self):
        lev = a.Leveranse()
        lev.leveringstidspunkt = self.amelding_record.leveringstidspunkt
        lev.kalendermaaned = self._get(
            self.amelding_record, "kalendermaaned"
        )  #'2018-01' #required
        lev.kildesystem = "Odoo"  # string #required
        # self._set(lev, 'erstatterMeldingsId', str(self._get(self.amelding_record, 'erstatterMeldingsId'))) #optional
        erstatterMeldingsId = self._get(self.amelding_record, "erstatterMeldingsId")
        if erstatterMeldingsId:
            lev.erstatterMeldingsId = str(erstatterMeldingsId)
        lev.meldingsId = str(
            self._get(self.amelding_record, "meldingsId")
        )  # string #required
        company = self._get(self.amelding_record, "company_id")  # required
        lev.opplysningspliktig = a.Opplysningspliktig()  # required
        lev.opplysningspliktig.norskIdentifikator = self._get(company, "vat")[
            2:
        ]  # string #required
        self._set(
            lev, "spraakForTilbakemelding", self._get(company, "l10n_no_Spraak")
        )  # selection #optional
        lev.oppgave = self.JuridiskEntitet()  # required
        return lev

    def JuridiskEntitet(
        self,
    ):
        je = a.JuridiskEntitet()
        # bi = je.betalingsinformasjon = a.Betalingsinformasjon()
        # virksomheter
        for my_id in [1]:  # replace
            v = self.Virksomhet()
            je.virksomhet.append(v)  # optional
            # bi = self.Betalingsinformasjon(bi, **info)
        je.betalingsinformasjon = self.Betalingsinformasjon()  # optional
        # betalingsinformasjonForForenkletOrdning
        # for id in []: #replace
        #    bif = self.BetalingsinformasjonForForenkletOrdning()
        #    je.betalingsinformasjonForForenkletOrdning.append(bif) #optional
        # je.annenBagatellmessigStoette = 1000.5 #replace #optional
        pensjonsinnretning = self._get(self.company, "l10n_no_pensjonsinnretning")
        if pensjonsinnretning:
            je.pensjonsinnretning.append(pensjonsinnretning)
        return je

    # def Betalingsinformasjon(self, bi, sumForskuddstrekk=None, sumArbeidsgiveravgift=None, sumFinansskattLoenn=None, **kwargs):
    #     if sumForskuddstrekk:
    #         bi.sumForskuddstrekk = not_None(bi.sumForskuddstrekk) + int(sumForskuddstrekk) #integer
    #     if sumArbeidsgiveravgift:
    #         bi.sumArbeidsgiveravgift = not_None(bi.sumArbeidsgiveravgift) + int(sumArbeidsgiveravgift) #integer
    #     if sumFinansskattLoenn:
    #         bi.sumFinansskattLoenn = not_None(bi.sumFinansskattLoenn) + int(sumFinansskattLoenn) #integer
    #     return bi
    def Betalingsinformasjon(self):
        bi = a.Betalingsinformasjon()
        if self.je["sumForskuddstrekk"]:
            bi.sumForskuddstrekk = int(
                self.je["sumForskuddstrekk"]
            )  # integer #optional
            self.amelding_record.sumForskuddstrekk = bi.sumForskuddstrekk
        if self.je["sumArbeidsgiveravgift"]:
            bi.sumArbeidsgiveravgift = int(
                self.je["sumArbeidsgiveravgift"]
            )  # integer #optional
            self.amelding_record.sumArbeidsgiveravgift = bi.sumArbeidsgiveravgift
        if self.je["sumFinansskattLoenn"]:
            bi.sumFinansskattLoenn = int(
                self.je["sumFinansskattLoenn"]
            )  # integer #optional
            self.amelding_record.sumFinansskattLoenn = bi.sumFinansskattLoenn
        if self.je["sumUtleggstrekk"]:
            bi.sumUtleggstrekk = int(self.je["sumUtleggstrekk"])  # integer #optional
            self.amelding_record.sumUtleggstrekk = bi.sumUtleggstrekk
        return bi

    # def BetalingsinformasjonForForenkletOrdning(self):
    #     bif = a.BetalingsinformasjonForForenkletOrdning()
    #     bif.sumForskuddstrekk = 1000 #replace #integer #optional
    #     bif.sumArbeidsgiveravgift = 1000 #replace #integer #optional
    #     bif.loennsutbetalingsdato = '2018-01-01' #replace #required
    #     return bif

    def Virksomhet(self):
        v = a.Virksomhet()
        v.norskIdentifikator = self._get(
            self.company, "l10n_no_virksomhet"
        )  # string #required

        for employee in self.employees:
            im = self.Inntektsmottaker(employee)
            if im:
                v.inntektsmottaker.append(im)  # optional

        for payslip_run in self.payslip_runs:
            agaplikt_uten_loennsopplysningsplikt = self._get(
                payslip_run, "l10n_no_AgapliktUtenLoennsopplysningsplikt"
            )
            if agaplikt_uten_loennsopplysningsplikt:
                self.aga["avgiftsgrunnlagBeloep"] += int(
                    agaplikt_uten_loennsopplysningsplikt
                )

        aga = self.Arbeidsgiveravgift()
        if aga:
            v.arbeidsgiveravgift = aga  # optional

        return v

    def Inntektsmottaker(self, employee):
        use = False
        im = a.Inntektsmottaker()
        norskIdentifikator = self._get(employee, "identification_id")  # string
        ii = self.InternasjonalIdentifikator(employee)
        if ii:
            im.internasjonalIdentifikator.append(ii)  # optional
        if norskIdentifikator:
            im.norskIdentifikator = norskIdentifikator  # optional
        im.identifiserendeInformasjon = a.IdentifiserendeInformasjon()  # optional
        im.identifiserendeInformasjon.navn = self._get(
            employee, "name"
        )  # string #required
        im.identifiserendeInformasjon.foedselsdato = self._get(
            employee, "birthday"
        )  # DATE_FORMAT #required
        # im.identifiserendeInformasjon.ansattnummer = '123' #replace #optional
        # arbeidsforhold
        for contract in self._get(employee, "contract_ids").sorted("date_start"):
            newer_period = contract.date_start > self.date_to
            if contract.date_end:
                older_period = contract.date_end < self.date_from
            else:
                older_period = False
            changed = (
                contract.write_date.date() > self.date_from - relativedelta(months=1)
                and
                not contract.write_uid.has_group('base.group_system')
            )
            if newer_period or (older_period and not changed):
                continue
            af = self.Arbeidsforhold(contract)
            im.arbeidsforhold.append(af)  # optional
            use = True

        for payslip in [
            p
            for p in self.payslips
            if self._get(self._get(p, "employee_id"), "id") == self._get(employee, "id")
        ]:
            use = True
            for line in [
                l
                for l in self.payslip_lines
                if self._get(self._get(l, "slip_id"), "id") == self._get(payslip, "id")
            ]:
                rule = self._get(line, "salary_rule_id")
                rule_type = self._get(rule, "l10n_no_RegelType")
                if rule_type in (
                    "loennsinntekt",
                    "ytelseFraOffentlige",
                    "pensjonEllerTrygd",
                    "naeringsinntekt",
                ):
                    inn = self.Inntekt(employee, payslip, line, rule, rule_type)
                    im.inntekt.append(inn)
                elif rule_type == "fradrag":
                    _debug("ERROR: fradrag")
                elif rule_type == "forskuddstrekk":
                    ft = self.Forskuddstrekk(line, rule)
                    im.forskuddstrekk.append(ft)
                else:
                    # aga av pensjon og refusjon sykepenger er ikke tilknyttet noen regeltype. All aga av inntekt er av typen "inntekt og godtgjoerelser".
                    navn = {
                        "loennOgGodtgjoerelse": "avgiftsgrunnlagBeloep",
                        "tilskuddOgPremieTilPensjon": "avgiftsgrunnlagBeloepPensjon",
                        "fradragIGrunnlagetForSone": "avgiftsfradragBeloep",
                    }
                    beregnAga = self._get(rule, "l10n_no_BeregnAga")
                    if beregnAga:
                        self.aga[navn[beregnAga]] += self._get(line, "total")
                    else:
                        _debug("ERROR: payslip line rule_type = " + str(rule_type))

        # im.sjoefolksrelatertInformasjon = self.SjoefolksrelatertInformasjon()
        # # oppholdPaaSvalbardJanMayenOgBilandene
        # for id in []: #replace
        #     opphold = self.OppholdPaaSvalbardJanMayenOgBilandene()
        #     im.oppholdPaaSvalbardJanMayenOgBilandene.append(opphold) #optional
        # # utleggstrekk
        # for id in []: #replace
        #     trekk = self.Utleggstrekk()
        #     im.utleggstrekk.append(trekk) #optional

        if not use:
            return False
        return im

    def InternasjonalIdentifikator(self, employee):
        passIdentifikator = self._get(employee, "passport_id")  # string
        land = self._get(employee, "country_id")  # record
        landkode = self._get(land, "code")  # string
        if passIdentifikator and landkode:
            ii = a.InternasjonalIdentifikator()
            ii.identifikatortype = "passnummer"
            ii.identifikator = passIdentifikator
            ii.land = landkode
            return ii

        # identifikator = self._get(employee, 'Internasjonalidentifikator')
        # identifikatortype = self._get(employee, 'Internasjonalidentifikatortype')  #string
        # land = self._get(employee, 'countryCode') # string
        # if identifikator and identifikatortype and land:
        #    ii = a.InternasjonalIdentifikator()
        #    ii.identifikator = identifikator  # string #required
        #    ii.identifikatortype = identifikatortype  # string #required
        #    ii.land = landkode # string #required
        #    return ii

        # result = []
        # if not countryCode:
        #     return None
        # for field in ['international_passportNo', 'international_socialSecurityNumber', 'international_taxIdentificationNumber', 'international_valueAddedTaxNumber']:
        #     value = self._get(employee, field)
        #     if value:
        #         ii = a.InternasjonalIdentifikator()
        #         ii.identifikator = value #string
        #         ii.identifikatortype = field #string
        #         ii.land = countryCode #string
        #         result.append()
        # return result

    def Arbeidsforhold(self, contract):
        af = a.Arbeidsforhold()
        af.arbeidsforholdId = str(contract.id)  # string #optional
        af.typeArbeidsforhold = self._get(
            contract, "l10n_no_Arbeidsforholdtype"
        )  # string #required
        if af.typeArbeidsforhold != "pensjonOgAndreTyperYtelserUtenAnsettelsesforhold":
            self._set(
                af, "startdato", self._get(contract, "date_start")
            )  # date #optional
            self._set(
                af, "sluttdato", self._get(contract, "date_end")
            )  # date #optional
            self._set(
                af,
                "antallTimerPerUkeSomEnFullStillingTilsvarer",
                self._get(
                    contract, "l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer"
                ),
            )  # float #optional
            # af.avloenningstype = self._get(contract, 'avloenningstype') #replace #string #optional #utgaar
            job = self._get(contract, "job_id")
            test_record = self._get(job, "l10n_no_job_code")
            test_code = test_record.code
            self._set(
                # af, "yrke", self._get(job, "l10n_no_job_code").code
                af,
                "yrke",
                test_code,
            )  # string #optional
            self._set(
                af,
                "arbeidstidsordning",
                self._get(contract, "l10n_no_Arbeidstidsordning"),
            )  # selection #optional
            self._set(
                af, "stillingsprosent", self._get(contract, "l10n_no_stillingsprosent")
            )  # float #optional
            self._set(
                af,
                "sisteLoennsendringsdato",
                self._get(contract, "l10n_no_sisteLoennsendringsdato"),
            )  # replace #datestring #optional
            self._set(
                af,
                "loennsansiennitet",
                self._get(contract, "l10n_no_loennsansiennitet"),
            )  # datestring #optional
            self._set(
                af, "loennstrinn", self._get(contract, "l10n_no_loennstrinn")
            )  # string #optional
            # af.fartoey = self.Fartoey() #optional
            # permisjon
            for leave in self._get(contract, "leave_ids").sorted("date_from"):
                newer_period = leave.date_from.date() > self.date_to
                older_period = leave.date_to.date() < self.date_from - relativedelta(
                    months=1
                )
                changed = (
                    leave.write_date.date() > self.date_from - relativedelta(months=1)
                    and
                    not leave.write_uid.has_group('base.group_system')
                )
                if newer_period or (older_period and not changed):
                    continue
                p = self.Permisjon(leave)
                af.permisjon.append(p)
            self._set(
                af,
                "sisteDatoForStillingsprosentendring",
                self._get(contract, "l10n_no_sisteDatoForStillingsprosentendring"),
            )  # date #optional
            self._set(
                af,
                "aarsakTilSluttdato",
                self._get(contract, "l10n_no_AarsakTilSluttdato"),
            )  # string #optional
            self._set(
                af,
                "formForAnsettelse",
                self._get(contract, "l10n_no_FormForAnsettelse"),
            )  # string #optional
        return af

    # def Fartoey(self):
    #     fartoey = a.Fartoey()
    #     fartoey.skipsregister = 'string' #replace
    #     fartoey.skipstype = 'string' #replace
    #     fartoey.fartsomraade = 'string' #replace
    #     return fartoey
    #
    def Permisjon(self, leave):
        p = a.Permisjon()
        p.startdato = leave.date_from.strftime("%Y-%m-%d")
        p.sluttdato = leave.date_to.strftime("%Y-%m-%d")
        p.permisjonsprosent = leave.percent
        p.permisjonId = str(leave.id)
        p.beskrivelse = self._get(
            leave.holiday_status_id, "l10n_no_PermisjonsOgPermitteringsBeskrivelse"
        )
        return p

    # def Fradrag(self):
    #     fra = a.Fradrag()
    #     fra.beskrivelse = 'string' #replace
    #     fra.beloep = 1000.5 #replace
    #     return fra

    def Forskuddstrekk(self, line, rule):
        ft = a.Forskuddstrekk()
        self._set(
            ft, "beskrivelse", self._get(rule, "l10n_no_Forskuddstrekkbeskrivelse")
        )  # selection #string #optional
        factor = -1 if line.slip_id.credit_note else 1
        ft.beloep = factor * self._get(line, "total")  # integer #required
        self.je["sumForskuddstrekk"] += -ft.beloep
        return ft

    def Inntekt(self, employee, payslip, line, rule, my_type):
        inn = a.Inntekt()
        self._set(
            inn, "skatteOgAvgiftsregel", self._get(rule, "l10n_no_SkatteOgAvgiftsregel")
        )  # selection #string #optional
        # inn.startdatoOpptjeningsperiode = '2018-01-01' #replace #date #optional
        # inn.sluttdatoOpptjeningsperiode = '2018-01-01' #replace #date #optional
        inn.fordel = self._get(rule, "l10n_no_Fordel")  # selection #string #required
        factor = -1 if line.slip_id.credit_note else 1
        inn.beloep = factor * self._get(line, "total")  # float #required

        beregnAga = self._get(rule, "l10n_no_BeregnAga")
        if beregnAga:
            navn = {
                "loennOgGodtgjoerelse": "avgiftsgrunnlagBeloep",
                "tilskuddOgPremieTilPensjon": "avgiftsgrunnlagBeloepPensjon",
                "fradragIGrunnlagetForSone": "avgiftsfradragBeloep",
            }
            self.aga[navn[beregnAga]] += inn.beloep
            inn.utloeserArbeidsgiveravgift = True  # boolean #required
        else:
            inn.utloeserArbeidsgiveravgift = False  # boolean #required

        inn.inngaarIGrunnlagForTrekk = bool(
            self._get(rule, "l10n_no_BeregnTrekk")
        )  # boolean #required
        # beregnTrekk = self._get(rule, 'l10n_no_BeregnTrekk')
        # if beregnTrekk:
        #    inn.inngaarIGrunnlagForTrekk = True #boolean #required
        # else:
        #    inn.inngaarIGrunnlagForTrekk = False #boolean #required

        # inn.arbeidsforholdId = '1' #replace #optional

        # choice
        inn.loennsinntekt = self.Loennsinntekt(line, rule)
        # inn.ytelseFraOffentlige = self.YtelseFraOffentlige()
        # inn.pensjonEllerTrygd = self.PensjonEllerTrygd()
        # inn.naeringsinntekt = self.Naeringsinntekt()
        return inn

    def Loennsinntekt(self, line, rule):
        loenn = a.Loennsinntekt()
        loenn.beskrivelse = self._get(
            rule, "l10n_no_Loennsbeskrivelse"
        )  # replace #string #required
        # loenn.tilleggsinformasjon = self.Tilleggsinformasjon() #optional
        # loenn.spesifikasjon = self.Spesifikasjon() #optional
        if loenn.beskrivelse in [
            "friTransport",
            "kilometergodtgjoerelseAndreFremkomstmidler",
            "kilometergodtgjoerelseBil",
            "kilometergodtgjoerelseElBil",
            "kilometergodtgjoerelsePassasjertillegg",
            "kostbesparelseIHjemmet",
            "kostDager",
            "kostDoegn",
            "losji",
            "losjiEgenBrakkeCampingvogn",
            "overtidsgodtgjoerelse",
            "overtidsmat",
            "reiseKostMedOvernatting",
            "reiseKostMedOvernattingPaaHotell",
            "reiseKostMedOvernattingPaaHotellBeordringUtover28Doegn",
            "reiseKostMedOvernattingPaaHybelBrakkePrivat",
            "reiseKostMedOvernattingPaaPensjonat",
            "reiseKostMedOvernattingTilLangtransportsjaafoerForKjoeringIUtlandet",
            "reiseKostUtenOvernatting",
            "reiseNattillegg",
            "timeloenn",
            "yrkebilTjenestligbehovKilometer",
        ]:
            self._set(loenn, "antall", self._get(line, "quantity"))  # optional
        return loenn

    # def Tilleggsinformasjon(self):
    #     ti = a.Tilleggsinformasjon()
    #     # choice
    #     ti.bilOgBaat = self.BilOgBaat()
    #     ti.dagmammaIEgenBolig = self.DagmammaIEgenBolig()
    #     ti.etterbetalingsperiode = self.Periode()
    #     ti.inntektPaaNorskKontinentalsokkel = self.NorskKontinentalsokkel()
    #     ti.inntjeningsforhold = 'string' #replace
    #     ti.livrente = self.Livrente()
    #     ti.lottOgPart = self.LottOgPartInnenFiske()
    #     ti.nettoloenn = self.Nettoloennsordning()
    #     ti.pensjon = self.AldersUfoereEtterlatteAvtalefestetOgKrigspensjon()
    #     ti.reiseKostOgLosji = self.ReiseKostOgLosji()
    #     ti.utenlandskArtist = self.UtenlandskArtist()
    #     ti.bonusFraForsvaret = self.BonusFraForsvaret()
    #     return ti
    #
    # def Periode(self):
    #     periode = a.Periode()
    #     periode.startdato = '2018-01-01'
    #     periode.sluttdato = '2018-01-01'
    #     return periode
    #
    # def BilOgBaat(self):
    #     bil = a.BilOgBaat()
    #     bil.antallKilometer = 1000.5 #replace
    #     bil.antallReiser = 1000 #replace #integer
    #     bil.heravAntallKilometerMellomHjemOgArbeid = 1000.5 #replace
    #     bil.listeprisForBil = 1000.5 #replace
    #     bil.bilregistreringsnummer = 'AB12345' #replace
    #     bil.erBilpool = True #replace
    #     bil.erAnnenBil = True #replace
    #     bil.erBilUtenforStandardregelen = True #replace
    #     bil.personklassifiseringAvBilbruker = 'string' #replace
    #     return bil
    #
    # def DagmammaIEgenBolig(self):
    #     dag = a.DagmammaIEgenBolig()
    #     dag.antallBarn = 1 #replace #integer
    #     dag.antallMaaneder = 1 #replace #integer
    #     return dag
    #
    # def NorskKontinentalsokkel(self):
    #     nks = a.NorskKontinentalsokkel()
    #     nks.tidsrom = self.Periode()
    #     nks.gjelderLoennFoerste60Dager = True #replace
    #     return nks
    #
    # def Livrente(self):
    #     livrente = a.Livrente()
    #     livrente.totaltUtbetaltBeloep = 1000.5 #replace
    #     return livrente
    #
    # def LottOgPartInnenFiske(self):
    #     lott = a.LottOgPartInnenFiske()
    #     lott.antallDager = 1 #replace #integer
    #     return lott
    #
    # def Nettoloennsordning(self):
    #     netto = a.Nettoloennsordning()
    #     netto.oppgrossingstabellnummer = 1000 #replace #integer
    #     netto.bilinformasjon = self.BilOgBaat()
    #     netto.betaltSkattebeloepIUtlandet = 1000.5 #replace
    #     return netto
    #
    # def AldersUfoereEtterlatteAvtalefestetOgKrigspensjon(self):
    #     pensjon = a.AldersUfoereEtterlatteAvtalefestetOgKrigspensjon()
    #     pensjon.grunnpensjonsbeloep = 1000.5 #replace
    #     pensjon.tilleggspensjonsbeloep = 1000.5 #replace
    #     pensjon.ufoeregrad = 50 #replace #integer
    #     pensjon.pensjonsgrad = 50 #replace #integer
    #     pensjon.heravEtterlattepensjon = 1000.5 #replace
    #     pensjon.tidsrom = self.Periode()
    #     return pensjon
    #
    # def ReiseKostOgLosji(self):
    #     reise = a.ReiseKostOgLosji()
    #     reise.persontype = 'string' #replace
    #     reise.antallReiser = 1 #replace #integer
    #     return reise
    #
    # def UtenlandskArtist(self):
    #     artist = a.UtenlandskArtist()
    #     artist.inntektsaar = '2018' #replace
    #     artist.oppgrossingsgrunnlag = 1000.5 #replace
    #     artist.trukketArtistskatt = 1000 #replace #integer
    #
    # def BonusFraForsvaret(self):
    #     bonus = a.BonusFraForsvaret()
    #     bonus.aaretUtbetalingenGjelderFor = '2018' #replace
    #     return bonus
    #
    # def Spesifikasjon(self):
    #     spes = a.Spesifikasjon()
    #     spes.skattemessigBosattILand = 'NO' #replace
    #     spes.opptjeningsland = 'NO' #replace
    #     spes.erOpptjentPaaHjelpefartoey = True #replace
    #     spes.erOpptjentPaaKontinentalsokkel = True #replace
    #     return spes
    #
    # def YtelseFraOffentlige(self):
    #     ytelse = a.YtelseFraOffentlige()
    #     ytelse.beskrivelse = 'string' #replace
    #     ytelse.tilleggsinformasjon = self.Tilleggsinformasjon()
    #     return ytelse
    #
    # def PensjonEllerTrygd(self):
    #     pt = a.PensjonEllerTrygd()
    #     pt.beskrivelse = 'string' #replace
    #     pt.tilleggsinformasjon = self.Tilleggsinformasjon()
    #     return pt
    #
    # def Naeringsinntekt(self):
    #     naering = a.Naeringsinntekt()
    #     naering.beskrivelse = 'string' #replace
    #     naering.tilleggsinformasjon = self.Tilleggsinformasjon()
    #     return naering
    #
    # def SjoefolksrelatertInformasjon(self):
    #     sjoe = a.SjoefolksrelatertInformasjon()
    #     sjoe.antallDoegnOmbord = 1 #replace #integer
    #     sjoe.antallDoegnOmbordUtenDekkedeSmaautgifter = 1 #replace #integer
    #     return sjoe
    #
    # def OppholdPaaSvalbardJanMayenOgBilandene(self):
    #     opphold = a.OppholdPaaSvalbardJanMayenOgBilandene()
    #     opphold.oppholdsId = 'string' #replace
    #     opphold.startdato = '2018-01-01' #replace
    #     opphold.sluttdato = '2018-01-01' #replace
    #     opphold.beskrivelse = 'string' #replace
    #     return opphold
    #
    # def Utleggstrekk(self):
    #     trekk = a.Utleggstrekk()
    #     trekk.beskrivelse = 'string' #replace
    #     trekk.beloep = 'integer' #replace
    #     return trekk

    def Arbeidsgiveravgift(self):
        aga = a.Arbeidsgiveravgift()
        # sumArbeidsgiveravgift = 0
        # loennOgGodtgjoerelse
        for my_id in [1]:  # replace
            # agag_loenn, arbeidsgiveravgift = self.Arbeidsgiveravgiftsgrunnlag(loennOgGodtgjoerelse)
            agag_loenn = self.Arbeidsgiveravgiftsgrunnlag(
                self.aga["avgiftsgrunnlagBeloep"]
            )
            aga.loennOgGodtgjoerelse.append(agag_loenn)
            # sumArbeidsgiveravgift += arbeidsgiveravgift
        # tilskuddOgPremieTilPensjon
        for my_id in [1]:  # replace
            agag_tilskudd = self.Arbeidsgiveravgiftsgrunnlag(
                self.aga["avgiftsgrunnlagBeloepPensjon"]
            )
            aga.tilskuddOgPremieTilPensjon.append(agag_tilskudd)
        # aga.utenlandskeMedSaerskiltProsentsats = self.UtenlandskeMedSaerskiltProsentsats()
        # aga.utenlandskeMedFastAvgiftsbeloep = self.UtenlandskeMedFastAvgiftsbeloep()
        # fradragIGrunnlagetForSone
        for my_id in [1]:  # replace
            fraig = self.FradragIGrunnlaget(self.aga["avgiftsfradragBeloep"])
            aga.fradragIGrunnlagetForSone.append(fraig)
        # aga.fradragIGrunnlagetForUtenlandsk = self.FradragIGrunnlagetForUtenlandsk()
        return aga

    def Arbeidsgiveravgiftsgrunnlag(self, beloep):
        agag = a.Arbeidsgiveravgiftsgrunnlag()
        agag.beregningskodeForArbeidsgiveravgift = self._get(
            self.company, "l10n_no_BeregningskodeForArbeidsgiveravgift"
        )
        agag.sone = self._get(self.company, "l10n_no_Arbeidsgiveravgiftsone")
        agag.avgiftsgrunnlagBeloep = beloep  # float
        agag.prosentsatsForAvgiftsberegning = self._get(
            self.company, "l10n_no_Grunnlagsprosent"
        )  # float
        self.je["sumArbeidsgiveravgift"] += (
            agag.avgiftsgrunnlagBeloep * agag.prosentsatsForAvgiftsberegning / 100
        )
        return agag

    # def UtenlandskeMedSaerskiltProsentsats(self):
    #     prosent = a.UtenlandskeMedSaerskiltProsentsats()
    #     prosent.avgiftsgrunnlagBeloep = 1000.5 #replace
    #     prosent.prosentsatsForAvgiftsberegning = 0.1 #replace
    #     return prosent
    #
    # def UtenlandskeMedFastAvgiftsbeloep(self):
    #     fast = a.UtenlandskeMedFastAvgiftsbeloep()
    #     fast.antallAvgiftsgrunnlagPersoner = 1 #replace #integer
    #     fast.beloepssatsForAvgiftsberegning = 1000.5 #replace
    #     return fast

    def FradragIGrunnlaget(self, beloep):
        fraig = a.FradragIGrunnlaget()
        fraig.beregningskodeForArbeidsgiveravgift = self._get(
            self.company, "l10n_no_BeregningskodeForArbeidsgiveravgift"
        )
        fraig.sone = self._get(self.company, "l10n_no_Arbeidsgiveravgiftsone")
        fraig.avgiftsfradragBeloep = beloep  # float
        fraig.prosentsatsForAvgiftsberegning = self._get(
            self.company, "l10n_no_Grunnlagsprosent"
        )  # float
        self.je["sumArbeidsgiveravgift"] += (
            fraig.avgiftsfradragBeloep * fraig.prosentsatsForAvgiftsberegning / 100
        )
        return fraig

    # def FradragIGrunnlagetForUtenlandsk(self):
    #     fraigu = a.FradragIGrunnlagetForUtenlandsk()
    #     fraigu.avgiftsfradragBeloep = 1000.5 #replace
    #     fraigu.prosentsatsForAvgiftsberegning = 0.1 #replace
    #     return fraigu

    # RECORDS

    def _get_records(self, model, domain, record):
        _debug("%s %s %s" % (str(model), str(domain), str(record)))
        records = record.env[model].with_context(active_test=False).search(domain)
        return records

    # def _filtered(self, records, field, list):  # HOW TO USER LAMBDA WITH VARIABLES? getattr(record, field) == variable ?
    #    if type(record) not in (dict, tuple):
    #        return records.filtered(lambda record: getattr(record, field) in list)
    #    else:
    #        pass

    # Get a list of record ids (if field is 'id')
    # Only used for Odoo search domain
    def _mapped(self, records, field):
        try:
            return records.mapped(field)
        except:
            pass
            # if len(records) > 0:
            #    #return (records[0][0], range(0, len(records)))
            #    return (records[0][0], [r[field] for r in records])

    # FIELDS

    def _set(self, obj, name, value):
        if value:
            setattr(obj, name, value)

    def _get(self, record, field):
        if record is None:
            return
        else:
            return getattr(record, field)
