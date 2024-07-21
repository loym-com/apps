from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod

__NAMESPACE__ = "urn:ske:fastsetting:innsamling:a-meldingen:v2_2"


@dataclass
class Arbeidsgiveravgiftsgrunnlag:
    beregningskodeForArbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
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
    avgiftsgrunnlagBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class Betalingsinformasjon:
    sumForskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sumArbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sumFinansskattLoenn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sumUtleggstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class BetalingsinformasjonForForenkletOrdning:
    sumForskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sumArbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
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
    antallKilometer: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antallReiser: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    heravAntallKilometerMellomHjemOgArbeid: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    listeprisForBil: Optional[Decimal] = field(
        default=None,
        metadata={
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
    erBilpool: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    erAnnenBil: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    erBilUtenforStandardregelen: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    personklassifiseringAvBilbruker: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class BonusFraForsvaret:
    aaretUtbetalingenGjelderFor: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class DagmammaIEgenBolig:
    antallBarn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    antallMaaneder: Optional[int] = field(
        default=None,
        metadata={
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
class FradragIGrunnlaget:
    beregningskodeForArbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
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
    avgiftsfradragBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class FradragIGrunnlagetForUtenlandsk:
    avgiftsfradragBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
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
    totaltUtbetaltBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class LottOgPartInnenFiske:
    antallDager: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class OppholdPaaSvalbardJanMayenOgBilandene:
    oppholdsId: Optional[str] = field(
        default=None,
        metadata={
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
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
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
    permisjonId: Optional[str] = field(
        default=None,
        metadata={
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
    antallReiser: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class SjoefolksrelatertInformasjon:
    antallDoegnOmbord: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    antallDoegnOmbordUtenDekkedeSmaautgifter: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Spesifikasjon:
    skattemessigBosattILand: Optional[str] = field(
        default=None,
        metadata={
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
    erOpptjentPaaHjelpefartoey: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    erOpptjentPaaKontinentalsokkel: Optional[bool] = field(
        default=None,
        metadata={
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
    trukketArtistskatt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class UtenlandskeMedFastAvgiftsbeloep:
    antallAvgiftsgrunnlagPersoner: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    beloepssatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class UtenlandskeMedSaerskiltProsentsats:
    avgiftsgrunnlagBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
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
    heravEtterlattepensjon: Optional[Decimal] = field(
        default=None,
        metadata={
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
    arbeidsforholdId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    typeArbeidsforhold: Optional[str] = field(
        default=None,
        metadata={
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
    antallTimerPerUkeSomEnFullStillingTilsvarer: Optional[Decimal] = field(
        default=None,
        metadata={
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
    sisteLoennsendringsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
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
    sisteDatoForStillingsprosentendring: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    aarsakTilSluttdato: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    formForAnsettelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Arbeidsgiveravgift:
    loennOgGodtgjoerelse: List[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    tilskuddOgPremieTilPensjon: List[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandskeMedSaerskiltProsentsats: Optional[UtenlandskeMedSaerskiltProsentsats] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandskeMedFastAvgiftsbeloep: Optional[UtenlandskeMedFastAvgiftsbeloep] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fradragIGrunnlagetForSone: List[FradragIGrunnlaget] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    fradragIGrunnlagetForUtenlandsk: Optional[FradragIGrunnlagetForUtenlandsk] = field(
        default=None,
        metadata={
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
    betaltSkattebeloepIUtlandet: Optional[Decimal] = field(
        default=None,
        metadata={
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
    gjelderLoennFoerste60Dager: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class Tilleggsinformasjon:
    bilOgBaat: Optional[BilOgBaat] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    dagmammaIEgenBolig: Optional[DagmammaIEgenBolig] = field(
        default=None,
        metadata={
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
    inntektPaaNorskKontinentalsokkel: Optional[NorskKontinentalsokkel] = field(
        default=None,
        metadata={
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
    lottOgPart: Optional[LottOgPartInnenFiske] = field(
        default=None,
        metadata={
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
    reiseKostOgLosji: Optional[ReiseKostOgLosji] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    utenlandskArtist: Optional[UtenlandskArtist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    bonusFraForsvaret: Optional[BonusFraForsvaret] = field(
        default=None,
        metadata={
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
    skatteOgAvgiftsregel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    startdatoOpptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    sluttdatoOpptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
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
    utloeserArbeidsgiveravgift: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )
    inngaarIGrunnlagForTrekk: Optional[bool] = field(
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
    arbeidsforholdId: Optional[str] = field(
        default=None,
        metadata={
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
    ytelseFraOffentlige: Optional[YtelseFraOffentlige] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    pensjonEllerTrygd: Optional[PensjonEllerTrygd] = field(
        default=None,
        metadata={
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
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    internasjonalIdentifikator: List[InternasjonalIdentifikator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    identifiserendeInformasjon: Optional[IdentifiserendeInformasjon] = field(
        default=None,
        metadata={
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
    sjoefolksrelatertInformasjon: Optional[SjoefolksrelatertInformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    oppholdPaaSvalbardJanMayenOgBilandene: List[OppholdPaaSvalbardJanMayenOgBilandene] = field(
        default_factory=list,
        metadata={
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
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
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
    betalingsinformasjonForForenkletOrdning: List[BetalingsinformasjonForForenkletOrdning] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )
    annenBagatellmessigStoette: Optional[Decimal] = field(
        default=None,
        metadata={
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
# Leveranse -> leveranse
class leveranse:
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
    erstatterMeldingsId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        }
    )
    meldingsId: Optional[str] = field(
        default=None,
        metadata={
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
    spraakForTilbakemelding: Optional[Spraak] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
        }
    )


@dataclass
class EDAG_M:
    # Optional[Leveranse] -> Optional[leveranse]
    Leveranse: Optional[leveranse] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_2",
            "required": True,
        }
    )


@dataclass
class melding(EDAG_M):
    class Meta:
        namespace = "urn:ske:fastsetting:innsamling:a-meldingen:v2_2"
