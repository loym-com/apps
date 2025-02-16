from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo.exceptions import UserError

from odoo.addons.l10n_no_payroll.models.amelding.generated import amelding_v2_3 as a

_logger = logging.getLogger(__name__)


"""
a = amelding_v2_3
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
"""


def _debug(my_input):
    # _logger.debug(str(my_input))
    # print(str(my_input))
    pass


def _strftime(date_or_time):
    format = "%Y-%m-%d"
    if type(date_or_time) is datetime:
        format = "%Y-%m-%dT%H:%M:%S.%f" # TODO: Where is this needed?
    if date_or_time:
        return date_or_time.strftime(format)
    else:
        return ""

# RECORDS

def _get_records(model, domain, record):
    _debug("%s %s %s" % (str(model), str(domain), str(record)))
    records = record.env[model].with_context(active_test=False).search(domain)
    return records

def _mapped(records, field):
    try:
        return records.mapped(field)
    except:
        pass

# FIELDS

def _set(obj, name, value):
    if value:
        setattr(obj, name, value)

def _get(record, field):
    if record is None:
        return
    else:
        return getattr(record, field)


class AmeldingLogikk:
    def __init__(self, amelding_record):
        self.amelding_record = amelding_record

        period = _get(self.amelding_record, "kalendermaaned")
        date_from = datetime.strptime(period + "-01", "%Y-%m-%d")
        self.date_from = date_from.date()
        date_to = date_from + relativedelta(day=31)
        self.date_to = date_to.date()
        self.company = _get(self.amelding_record, "company_id")
        company_id = _get(self.company, "id")
        self.employees = _get_records(
            "hr.employee",
            [("company_id", "=", company_id), ("active", "=", True)],
            self.company,
        )
        self.contracts = _get_records(
            "hr.contract", [("company_id", "=", company_id)], self.company
        )
        self.payslips = _get_records(
            "hr.payslip",
            [
                ("company_id", "=", company_id),
                ("date_to", ">=", date_from),
                ("date_to", "<=", date_to),
            ],
            self.company,
        )
        self.payslip_lines = _get_records(
            "hr.payslip.line",
            [("slip_id", "in", _mapped(self.payslips, "id"))],
            self.company,
        )
        self.payslip_runs = self.payslips.mapped("payslip_run_id")
        self.countries = _get_records("res.country", [], self.company)
        self.jobs = _get_records(
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
        m = self.melding()
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        return serializer.render(m)

    def melding(self):
        m = a.melding()
        # Altinn requires that m.Leveranse has uppercase L.
        # Therefore, a.leveranse() practically needs lowercase l.
        m.Leveranse = self.leveranse()
        return m

    def leveranse(self):
        lev = a.leveranse()
        lev.leveringstidspunkt = self.amelding_record.leveringstidspunkt.strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        lev.kalendermaaned = _get(
            self.amelding_record, "kalendermaaned"
        )
        lev.kildesystem = "Odoo"
        erstatterMeldingsId = _get(self.amelding_record, "erstatterMeldingsId")
        if erstatterMeldingsId:
            lev.erstatterMeldingsId = str(erstatterMeldingsId)
        lev.meldingsId = str(_get(self.amelding_record, "meldingsId"))
        company = _get(self.amelding_record, "company_id")
        lev.opplysningspliktig = a.Opplysningspliktig()
        lev.opplysningspliktig.norskIdentifikator = _get(company, "vat")[2:]
        _set(
            lev, "spraakForTilbakemelding", _get(company, "l10n_no_Spraak")
        )
        lev.oppgave = self.JuridiskEntitet()
        return lev

    def JuridiskEntitet(self):
        je = a.JuridiskEntitet()
        # Not implemented: A legal entity may have multiple companies ("virksomheter").
        v = self.Virksomhet()
        je.virksomhet.append(v)
        je.betalingsinformasjon = self.Betalingsinformasjon()  # optional
        # betalingsinformasjonForForenkletOrdning
        # for id in []: #replace
        #    bif = self.BetalingsinformasjonForForenkletOrdning()
        #    je.betalingsinformasjonForForenkletOrdning.append(bif) #optional
        # je.annenBagatellmessigStoette = 1000.5 #replace #optional

        pensjonsinnretning = _get(self.company, "l10n_no_pensjonsinnretning")
        if pensjonsinnretning:
            pi = a.Pensjonsinnretning()
            pi.identifikator = pensjonsinnretning
            je.pensjonsinnretning.append(pi)
        return je

    def Betalingsinformasjon(self):
        bi = a.Betalingsinformasjon()
        if self.je["sumForskuddstrekk"]:
            bi.sumForskuddstrekk = int(
                self.je["sumForskuddstrekk"]
            )
            self.amelding_record.sumForskuddstrekk = bi.sumForskuddstrekk
        if self.je["sumArbeidsgiveravgift"]:
            bi.sumArbeidsgiveravgift = int(
                self.je["sumArbeidsgiveravgift"]
            )
            self.amelding_record.sumArbeidsgiveravgift = bi.sumArbeidsgiveravgift
        if self.je["sumFinansskattLoenn"]:
            bi.sumFinansskattLoenn = int(
                self.je["sumFinansskattLoenn"]
            )
            self.amelding_record.sumFinansskattLoenn = bi.sumFinansskattLoenn
        if self.je["sumUtleggstrekk"]:
            bi.sumUtleggstrekk = int(self.je["sumUtleggstrekk"])
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
        v.norskIdentifikator = _get(self.company, "l10n_no_virksomhet")

        for employee in self.employees:
            im = self.Inntektsmottaker(employee)
            if im:
                v.inntektsmottaker.append(im)  # optional

        for payslip_run in self.payslip_runs:
            agaplikt_uten_loennsopplysningsplikt = _get(
                payslip_run, "l10n_no_AgapliktUtenLoennsopplysningsplikt"
            )
            if agaplikt_uten_loennsopplysningsplikt:
                self.aga["avgiftsgrunnlagBeloep"] += int(
                    agaplikt_uten_loennsopplysningsplikt
                )

        aga = self.Arbeidsgiveravgift()
        if aga:
            v.arbeidsgiveravgift = aga

        return v

    def Inntektsmottaker(self, employee):
        use = False
        im = a.Inntektsmottaker()
        norskIdentifikator = _get(employee, "identification_id")
        ii = self.InternasjonalIdentifikator(employee)
        if ii:
            im.internasjonalIdentifikator.append(ii)
        if norskIdentifikator:
            im.norskIdentifikator = norskIdentifikator
        im.identifiserendeInformasjon = a.IdentifiserendeInformasjon()
        im.identifiserendeInformasjon.navn = _get(
            employee, "name"
        )
        im.identifiserendeInformasjon.foedselsdato = _get(
            employee, "birthday"
        ).strftime("%Y-%m-%d")
        # im.identifiserendeInformasjon.ansattnummer = '123' #replace #optional

        for contract in _get(employee, "contract_ids").sorted("date_start"):
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
            im.arbeidsforhold.append(af)
            use = True

        for payslip in [
            p
            for p in self.payslips
            if _get(_get(p, "employee_id"), "id") == _get(employee, "id")
        ]:
            use = True
            for line in [
                l
                for l in self.payslip_lines
                if _get(_get(l, "slip_id"), "id") == _get(payslip, "id")
            ]:
                rule = _get(line, "salary_rule_id")
                rule_type = _get(rule, "l10n_no_RegelType")
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
                    navn = {
                        "loennOgGodtgjoerelse": "avgiftsgrunnlagBeloep",
                        "tilskuddOgPremieTilPensjon": "avgiftsgrunnlagBeloepPensjon",
                        "fradragIGrunnlagetForSone": "avgiftsfradragBeloep",
                    }
                    beregnAga = _get(rule, "l10n_no_BeregnAga")
                    if beregnAga:
                        self.aga[navn[beregnAga]] += _get(line, "total")
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
        passIdentifikator = _get(employee, "passport_id")
        land = _get(employee, "country_id")
        landkode = _get(land, "code")
        if passIdentifikator and landkode:
            ii = a.InternasjonalIdentifikator()
            ii.identifikatortype = "passnummer"
            ii.identifikator = passIdentifikator
            ii.land = landkode
            return ii

        # identifikator = _get(employee, 'Internasjonalidentifikator')
        # identifikatortype = _get(employee, 'Internasjonalidentifikatortype')  #string
        # land = _get(employee, 'countryCode') # string
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
        #     value = _get(employee, field)
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
        af.typeArbeidsforhold = _get(
            contract, "l10n_no_Arbeidsforholdtype"
        )
        if af.typeArbeidsforhold != "pensjonOgAndreTyperYtelserUtenAnsettelsesforhold":
            _set(af, "startdato", _strftime(_get(contract, "date_start")))
            _set(af, "sluttdato", _strftime(_get(contract, "date_end")))
            _set(
                af,
                "antallTimerPerUkeSomEnFullStillingTilsvarer",
                _get(
                    contract, "l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer"
                ),
            )
            job = _get(contract, "job_id")
            _set(af, "yrke", _get(job, "l10n_no_job_code").code)
            # test_record = _get(job, "l10n_no_job_code")
            # test_code = test_record.code
            # _set(af, "yrke", test_code)
            _set(
                af,
                "arbeidstidsordning",
                _get(contract, "l10n_no_Arbeidstidsordning"),
            )
            _set(
                af, "stillingsprosent", _get(contract, "l10n_no_stillingsprosent")
            )
            _set(
                af,
                "sisteLoennsendringsdato",
                _strftime(_get(contract, "l10n_no_sisteLoennsendringsdato")),
            )
            _set(
                af,
                "loennsansiennitet",
                _strftime(_get(contract, "l10n_no_loennsansiennitet")),
            )
            _set(
                af, "loennstrinn", _get(contract, "l10n_no_loennstrinn")
            )
            # af.fartoey = self.Fartoey() #optional

            for leave in _get(contract, "leave_ids").sorted("date_from"):
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
            _set(
                af,
                "sisteDatoForStillingsprosentendring",
                _strftime(
                    _get(contract, "l10n_no_sisteDatoForStillingsprosentendring")
                ),
            )
            _set(
                af,
                "aarsakTilSluttdato",
                _get(contract, "l10n_no_AarsakTilSluttdato"),
            )
            _set(
                af,
                "formForAnsettelse",
                _get(contract, "l10n_no_FormForAnsettelse"),
            )
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
        p.beskrivelse = _get(
            leave.holiday_status_id, "l10n_no_PermisjonsOgPermitteringsBeskrivelse"
        )
        p.loennet = _get(leave.holiday_status_id, "l10n_no_PermisjonLoennetUloennet")
        return p

    def Permittering(self, leave):
        p = a.Permittering()
        p.permitteringId = str(leave.id)
        p.varslingsdato = leave.l10n_no_date_warning.strftime("%Y-%m-%d")
        p.startdatoPermittering = leave.date_from.strftime("%Y-%m-%d")
        p.sluttdatoPermittering = leave.date_to.strftime("%Y-%m-%d")
        p.sluttdatoLoennsplikt = leave.l10n_no_date_end_salary.strftime("%Y-%m-%d")
        p.permitteringsprosent = leave.percent
        p.permitteringsaarsak = _get(
            leave.holiday_status_id, "l10n_no_PermitteringsBeskrivelse"
        )
        return p

    # def Fradrag(self):
    #     fra = a.Fradrag()
    #     fra.beskrivelse = 'string' #replace
    #     fra.beloep = 1000.5 #replace
    #     return fra

    def Forskuddstrekk(self, line, rule):
        ft = a.Forskuddstrekk()
        _set(
            ft, "beskrivelse", _get(rule, "l10n_no_Forskuddstrekkbeskrivelse")
        )
        factor = -1 if line.slip_id.credit_note else 1
        ft.beloep = factor * int(_get(line, "total"))
        self.je["sumForskuddstrekk"] += -ft.beloep
        return ft

    def Inntekt(self, employee, payslip, line, rule, my_type):
        inn = a.Inntekt()
        _set(
            inn, "skatteOgAvgiftsregel", _get(rule, "l10n_no_SkatteOgAvgiftsregel")
        )
        # inn.startdatoOpptjeningsperiode = '2018-01-01' #replace #date #optional
        # inn.sluttdatoOpptjeningsperiode = '2018-01-01' #replace #date #optional
        inn.fordel = _get(rule, "l10n_no_Fordel")  # selection #string #required
        factor = -1 if line.slip_id.credit_note else 1
        inn.beloep = factor * _get(line, "total")

        beregnAga = _get(rule, "l10n_no_BeregnAga")
        if beregnAga:
            navn = {
                "loennOgGodtgjoerelse": "avgiftsgrunnlagBeloep",
                "tilskuddOgPremieTilPensjon": "avgiftsgrunnlagBeloepPensjon",
                "fradragIGrunnlagetForSone": "avgiftsfradragBeloep",
            }
            self.aga[navn[beregnAga]] += inn.beloep
            inn.utloeserArbeidsgiveravgift = True
        else:
            inn.utloeserArbeidsgiveravgift = False

        inn.inngaarIGrunnlagForTrekk = bool(
            _get(rule, "l10n_no_BeregnTrekk")
        )
        # inn.arbeidsforholdId = '1' #replace #optional

        # choice
        inn.loennsinntekt = self.Loennsinntekt(line, rule)
        # inn.ytelseFraOffentlige = self.YtelseFraOffentlige()
        # inn.pensjonEllerTrygd = self.PensjonEllerTrygd()
        # inn.naeringsinntekt = self.Naeringsinntekt()
        return inn

    def Loennsinntekt(self, line, rule):
        loenn = a.Loennsinntekt()
        loenn.beskrivelse = _get(
            rule, "l10n_no_Loennsbeskrivelse"
        )
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
            _set(loenn, "antall", _get(line, "quantity"))
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
        # loennOgGodtgjoerelse
        agag_loenn = self.Arbeidsgiveravgiftsgrunnlag(
            self.aga["avgiftsgrunnlagBeloep"]
        )
        aga.loennOgGodtgjoerelse.append(agag_loenn)
        # tilskuddOgPremieTilPensjon
        agag_tilskudd = self.Arbeidsgiveravgiftsgrunnlag(
            self.aga["avgiftsgrunnlagBeloepPensjon"]
        )
        aga.tilskuddOgPremieTilPensjon.append(agag_tilskudd)
        # aga.utenlandskeMedSaerskiltProsentsats = self.UtenlandskeMedSaerskiltProsentsats()
        # aga.utenlandskeMedFastAvgiftsbeloep = self.UtenlandskeMedFastAvgiftsbeloep()
        # fradragIGrunnlagetForSone
        fraig = self.FradragIGrunnlaget(self.aga["avgiftsfradragBeloep"])
        aga.fradragIGrunnlagetForSone.append(fraig)
        # aga.fradragIGrunnlagetForUtenlandsk = self.FradragIGrunnlagetForUtenlandsk()
        return aga

    def Arbeidsgiveravgiftsgrunnlag(self, beloep):
        agag = a.Arbeidsgiveravgiftsgrunnlag()
        agag.beregningskodeForArbeidsgiveravgift = _get(
            self.company, "l10n_no_BeregningskodeForArbeidsgiveravgift"
        )
        agag.sone = _get(self.company, "l10n_no_Arbeidsgiveravgiftsone")
        agag.avgiftsgrunnlagBeloep = beloep
        agag.prosentsatsForAvgiftsberegning = _get(
            self.company, "l10n_no_Grunnlagsprosent"
        )  # float
        self.je["sumArbeidsgiveravgift"] += (
            agag.avgiftsgrunnlagBeloep
            * float(agag.prosentsatsForAvgiftsberegning) / 100
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
        fraig.beregningskodeForArbeidsgiveravgift = _get(
            self.company, "l10n_no_BeregningskodeForArbeidsgiveravgift"
        )
        fraig.sone = _get(self.company, "l10n_no_Arbeidsgiveravgiftsone")
        fraig.avgiftsfradragBeloep = beloep
        fraig.prosentsatsForAvgiftsberegning = _get(
            self.company, "l10n_no_Grunnlagsprosent"
        )
        self.je["sumArbeidsgiveravgift"] += (
            fraig.avgiftsfradragBeloep
            * float(fraig.prosentsatsForAvgiftsberegning) / 100
        )
        return fraig

    # def FradragIGrunnlagetForUtenlandsk(self):
    #     fraigu = a.FradragIGrunnlagetForUtenlandsk()
    #     fraigu.avgiftsfradragBeloep = 1000.5 #replace
    #     fraigu.prosentsatsForAvgiftsberegning = 0.1 #replace
    #     return fraigu
