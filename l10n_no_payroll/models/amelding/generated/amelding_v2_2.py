from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod

__NAMESPACE__ = "urn:ske:fastsetting:innsamling:a-meldingen:v2_2"


@dataclass
class Arbeidsgiveravgiftsgrunnlag:
    beregningskode_for_arbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
            "name": "beregningskodeForArbeidsgiveravgift",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    sone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    avgiftsgrunnlag_beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "avgiftsgrunnlagBeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsats_for_avgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "prosentsatsForAvgiftsberegning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Betalingsinformasjon:
    sum_forskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumForskuddstrekk",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sum_arbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumArbeidsgiveravgift",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sum_finansskatt_loenn: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumFinansskattLoenn",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sum_utleggstrekk: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumUtleggstrekk",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class BetalingsinformasjonForForenkletOrdning:
    sum_forskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumForskuddstrekk",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sum_arbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
            "name": "sumArbeidsgiveravgift",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    loennsutbetalingsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class BilOgBaat:
    antall_kilometer: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "antallKilometer",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antall_reiser: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallReiser",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    herav_antall_kilometer_mellom_hjem_og_arbeid: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "heravAntallKilometerMellomHjemOgArbeid",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    listepris_for_bil: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "listeprisForBil",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    bilregistreringsnummer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 255,
        }
    )
    er_bilpool: Optional[bool] = field(
        default=None,
        metadata={
            "name": "erBilpool",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    er_annen_bil: Optional[bool] = field(
        default=None,
        metadata={
            "name": "erAnnenBil",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    er_bil_utenfor_standardregelen: Optional[bool] = field(
        default=None,
        metadata={
            "name": "erBilUtenforStandardregelen",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    personklassifisering_av_bilbruker: Optional[str] = field(
        default=None,
        metadata={
            "name": "personklassifiseringAvBilbruker",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class BonusFraForsvaret:
    aaret_utbetalingen_gjelder_for: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "name": "aaretUtbetalingenGjelderFor",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class DagmammaIegenBolig:
    class Meta:
        name = "DagmammaIEgenBolig"

    antall_barn: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallBarn",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    antall_maaneder: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallMaaneder",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Fartoey:
    skipsregister: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    skipstype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    fartsomraade: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Forskuddstrekk:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    beloep: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Fradrag:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class FradragIgrunnlaget:
    class Meta:
        name = "FradragIGrunnlaget"

    beregningskode_for_arbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
            "name": "beregningskodeForArbeidsgiveravgift",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    sone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    avgiftsfradrag_beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "avgiftsfradragBeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsats_for_avgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "prosentsatsForAvgiftsberegning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class FradragIgrunnlagetForUtenlandsk:
    class Meta:
        name = "FradragIGrunnlagetForUtenlandsk"

    avgiftsfradrag_beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "avgiftsfradragBeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsats_for_avgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "prosentsatsForAvgiftsberegning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class IdentifiserendeInformasjon:
    navn: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 255,
        }
    )
    foedselsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    ansattnummer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 255,
        }
    )


@dataclass
class InternasjonalIdentifikator:
    identifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 255,
        }
    )
    identifikatortype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    land: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Livrente:
    totalt_utbetalt_beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "totaltUtbetaltBeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class LottOgPartInnenFiske:
    antall_dager: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallDager",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class OppholdPaaSvalbardJanMayenOgBilandene:
    oppholds_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "oppholdsId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Opplysningspliktig:
    norsk_identifikator: Optional[str] = field(
        default=None,
        metadata={
            "name": "norskIdentifikator",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Pensjonsinnretning:
    identifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 255,
        }
    )


@dataclass
class Periode:
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Permisjon:
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    permisjonsprosent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    permisjon_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "permisjonId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class ReiseKostOgLosji:
    persontype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antall_reiser: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallReiser",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class SjoefolksrelatertInformasjon:
    antall_doegn_ombord: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallDoegnOmbord",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antall_doegn_ombord_uten_dekkede_smaautgifter: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallDoegnOmbordUtenDekkedeSmaautgifter",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Spesifikasjon:
    skattemessig_bosatt_iland: Optional[str] = field(
        default=None,
        metadata={
            "name": "skattemessigBosattILand",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    opptjeningsland: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    er_opptjent_paa_hjelpefartoey: Optional[bool] = field(
        default=None,
        metadata={
            "name": "erOpptjentPaaHjelpefartoey",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    er_opptjent_paa_kontinentalsokkel: Optional[bool] = field(
        default=None,
        metadata={
            "name": "erOpptjentPaaKontinentalsokkel",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


class Spraak(Enum):
    BOKMAAL = "bokmaal"
    NYNORSK = "nynorsk"
    ENGELSK = "engelsk"


@dataclass
class UtenlandskArtist:
    inntektsaar: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    oppgrossingsgrunnlag: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    trukket_artistskatt: Optional[int] = field(
        default=None,
        metadata={
            "name": "trukketArtistskatt",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class UtenlandskeMedFastAvgiftsbeloep:
    antall_avgiftsgrunnlag_personer: Optional[int] = field(
        default=None,
        metadata={
            "name": "antallAvgiftsgrunnlagPersoner",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    beloepssats_for_avgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "beloepssatsForAvgiftsberegning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class UtenlandskeMedSaerskiltProsentsats:
    avgiftsgrunnlag_beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "avgiftsgrunnlagBeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsats_for_avgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "prosentsatsForAvgiftsberegning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Utleggstrekk:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    beloep: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class AldersUfoereEtterlatteAvtalefestetOgKrigspensjon:
    grunnpensjonsbeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    tilleggspensjonsbeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    ufoeregrad: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    pensjonsgrad: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    herav_etterlattepensjon: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "heravEtterlattepensjon",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    tidsrom: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Arbeidsforhold:
    arbeidsforhold_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "arbeidsforholdId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    type_arbeidsforhold: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeArbeidsforhold",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antall_timer_per_uke_som_en_full_stilling_tilsvarer: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "antallTimerPerUkeSomEnFullStillingTilsvarer",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    avloenningstype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    yrke: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    arbeidstidsordning: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    stillingsprosent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    siste_loennsendringsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "sisteLoennsendringsdato",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    loennsansiennitet: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    loennstrinn: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 255,
        }
    )
    fartoey: Optional[Fartoey] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    permisjon: List[Permisjon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    siste_dato_for_stillingsprosentendring: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "sisteDatoForStillingsprosentendring",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    aarsak_til_sluttdato: Optional[str] = field(
        default=None,
        metadata={
            "name": "aarsakTilSluttdato",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    form_for_ansettelse: Optional[str] = field(
        default=None,
        metadata={
            "name": "formForAnsettelse",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Arbeidsgiveravgift:
    loenn_og_godtgjoerelse: List[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "name": "loennOgGodtgjoerelse",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    tilskudd_og_premie_til_pensjon: List[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "name": "tilskuddOgPremieTilPensjon",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandske_med_saerskilt_prosentsats: Optional[UtenlandskeMedSaerskiltProsentsats] = field(
        default=None,
        metadata={
            "name": "utenlandskeMedSaerskiltProsentsats",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandske_med_fast_avgiftsbeloep: Optional[UtenlandskeMedFastAvgiftsbeloep] = field(
        default=None,
        metadata={
            "name": "utenlandskeMedFastAvgiftsbeloep",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fradrag_igrunnlaget_for_sone: List[FradragIgrunnlaget] = field(
        default_factory=list,
        metadata={
            "name": "fradragIGrunnlagetForSone",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fradrag_igrunnlaget_for_utenlandsk: Optional[FradragIgrunnlagetForUtenlandsk] = field(
        default=None,
        metadata={
            "name": "fradragIGrunnlagetForUtenlandsk",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Nettoloennsordning:
    oppgrossingstabellnummer: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    bilinformasjon: Optional[BilOgBaat] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    betalt_skattebeloep_iutlandet: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "betaltSkattebeloepIUtlandet",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class NorskKontinentalsokkel:
    tidsrom: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    gjelder_loenn_foerste60_dager: Optional[bool] = field(
        default=None,
        metadata={
            "name": "gjelderLoennFoerste60Dager",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Tilleggsinformasjon:
    bil_og_baat: Optional[BilOgBaat] = field(
        default=None,
        metadata={
            "name": "bilOgBaat",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    dagmamma_iegen_bolig: Optional[DagmammaIegenBolig] = field(
        default=None,
        metadata={
            "name": "dagmammaIEgenBolig",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    etterbetalingsperiode: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    inntekt_paa_norsk_kontinentalsokkel: Optional[NorskKontinentalsokkel] = field(
        default=None,
        metadata={
            "name": "inntektPaaNorskKontinentalsokkel",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    inntjeningsforhold: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    livrente: Optional[Livrente] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    lott_og_part: Optional[LottOgPartInnenFiske] = field(
        default=None,
        metadata={
            "name": "lottOgPart",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    nettoloenn: Optional[Nettoloennsordning] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    pensjon: Optional[AldersUfoereEtterlatteAvtalefestetOgKrigspensjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    reise_kost_og_losji: Optional[ReiseKostOgLosji] = field(
        default=None,
        metadata={
            "name": "reiseKostOgLosji",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandsk_artist: Optional[UtenlandskArtist] = field(
        default=None,
        metadata={
            "name": "utenlandskArtist",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    bonus_fra_forsvaret: Optional[BonusFraForsvaret] = field(
        default=None,
        metadata={
            "name": "bonusFraForsvaret",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Loennsinntekt:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    spesifikasjon: Optional[Spesifikasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antall: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Naeringsinntekt:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class PensjonEllerTrygd:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class YtelseFraOffentlige:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Inntekt:
    skatte_og_avgiftsregel: Optional[str] = field(
        default=None,
        metadata={
            "name": "skatteOgAvgiftsregel",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    startdato_opptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "startdatoOpptjeningsperiode",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sluttdato_opptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "sluttdatoOpptjeningsperiode",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fordel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    utloeser_arbeidsgiveravgift: Optional[bool] = field(
        default=None,
        metadata={
            "name": "utloeserArbeidsgiveravgift",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    inngaar_igrunnlag_for_trekk: Optional[bool] = field(
        default=None,
        metadata={
            "name": "inngaarIGrunnlagForTrekk",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    arbeidsforhold_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "arbeidsforholdId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    loennsinntekt: Optional[Loennsinntekt] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    ytelse_fra_offentlige: Optional[YtelseFraOffentlige] = field(
        default=None,
        metadata={
            "name": "ytelseFraOffentlige",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    pensjon_eller_trygd: Optional[PensjonEllerTrygd] = field(
        default=None,
        metadata={
            "name": "pensjonEllerTrygd",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    naeringsinntekt: Optional[Naeringsinntekt] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Inntektsmottaker:
    norsk_identifikator: Optional[str] = field(
        default=None,
        metadata={
            "name": "norskIdentifikator",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    internasjonal_identifikator: List[InternasjonalIdentifikator] = field(
        default_factory=list,
        metadata={
            "name": "internasjonalIdentifikator",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    identifiserende_informasjon: Optional[IdentifiserendeInformasjon] = field(
        default=None,
        metadata={
            "name": "identifiserendeInformasjon",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    arbeidsforhold: List[Arbeidsforhold] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fradrag: List[Fradrag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    forskuddstrekk: List[Forskuddstrekk] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    inntekt: List[Inntekt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sjoefolksrelatert_informasjon: Optional[SjoefolksrelatertInformasjon] = field(
        default=None,
        metadata={
            "name": "sjoefolksrelatertInformasjon",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    opphold_paa_svalbard_jan_mayen_og_bilandene: List[OppholdPaaSvalbardJanMayenOgBilandene] = field(
        default_factory=list,
        metadata={
            "name": "oppholdPaaSvalbardJanMayenOgBilandene",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utleggstrekk: List[Utleggstrekk] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Virksomhet:
    norsk_identifikator: Optional[str] = field(
        default=None,
        metadata={
            "name": "norskIdentifikator",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    inntektsmottaker: List[Inntektsmottaker] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    arbeidsgiveravgift: Optional[Arbeidsgiveravgift] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class JuridiskEntitet:
    betalingsinformasjon: Optional[Betalingsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    betalingsinformasjon_for_forenklet_ordning: List[BetalingsinformasjonForForenkletOrdning] = field(
        default_factory=list,
        metadata={
            "name": "betalingsinformasjonForForenkletOrdning",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    annen_bagatellmessig_stoette: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "annenBagatellmessigStoette",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    virksomhet: List[Virksomhet] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    pensjonsinnretning: List[Pensjonsinnretning] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Leveranse:
    leveringstidspunkt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    kalendermaaned: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "min_inclusive": XmlPeriod("2014-01"),
            "max_inclusive": XmlPeriod("2099-12"),
        }
    )
    kildesystem: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 255,
        }
    )
    erstatter_meldings_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "erstatterMeldingsId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    meldings_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "meldingsId",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    opplysningspliktig: Optional[Opplysningspliktig] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    oppgave: Optional[JuridiskEntitet] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    spraak_for_tilbakemelding: Optional[Spraak] = field(
        default=None,
        metadata={
            "name": "spraakForTilbakemelding",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class EdagM:
    class Meta:
        name = "EDAG_M"

    leveranse: Optional[Leveranse] = field(
        default=None,
        metadata={
            "name": "Leveranse",
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Melding(EdagM):
    class Meta:
        name = "melding"
        namespace = "urn:ske:fastsetting:innsamling:a-meldingen:v2_2"
