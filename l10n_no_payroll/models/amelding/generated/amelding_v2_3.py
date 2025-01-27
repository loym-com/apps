from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod

__NAMESPACE__ = "urn:ske:fastsetting:innsamling:a-meldingen:v2_3"


@dataclass
class Arbeidsgiveravgiftsgrunnlag:
    beregningskodeForArbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    avgiftsgrunnlagBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class BeloepPerLoennsutbetalingsdato:
    loennsutbetalingsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    beloep: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class BetalingsinformasjonForForenkletOrdning:
    sumForskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sumArbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    loennsutbetalingsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class BilOgBaat:
    antallKilometer: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    antallReiser: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    heravAntallKilometerMellomHjemOgArbeid: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    listeprisForBil: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    bilregistreringsnummer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 255,
        },
    )
    erBilpool: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    erAnnenBil: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    erBilUtenforStandardregelen: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    personklassifiseringAvBilbruker: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class BonusFraForsvaret:
    aaretUtbetalingenGjelderFor: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class DagmammaIEgenBolig:
    antallBarn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    antallMaaneder: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Fartoey:
    skipsregister: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    skipstype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    fartsomraade: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Forskuddstrekk:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    beloep: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Fradrag:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class FradragIGrunnlaget:
    beregningskodeForArbeidsgiveravgift: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    avgiftsfradragBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class FradragIGrunnlagetForUtenlandsk:
    avgiftsfradragBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class IdentifiserendeInformasjon:
    navn: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 255,
        },
    )
    foedselsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    ansattnummer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 255,
        },
    )


@dataclass
class InternasjonalIdentifikator:
    identifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 255,
        },
    )
    identifikatortype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    land: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Livrente:
    totaltUtbetaltBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class LottOgPartInnenFiske:
    antallDager: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class OppholdPaaSvalbardJanMayenOgBilandene:
    oppholdsId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Opplysningspliktig:
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Pensjonsinnretning:
    identifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 255,
        },
    )


@dataclass
class Periode:
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Permisjon:
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    permisjonsprosent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    permisjonId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    loennet: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Permittering:
    permitteringId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    varslingsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    startdatoPermittering: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    sluttdatoPermittering: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sluttdatoLoennsplikt: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    permitteringsprosent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    permitteringsaarsak: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class ReiseKostOgLosji:
    persontype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    antallReiser: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class SjoefolksrelatertInformasjon:
    antallDoegnOmbord: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    antallDoegnOmbordUtenDekkedeSmaautgifter: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Spesifikasjon:
    skattemessigBosattILand: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    opptjeningsland: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    erOpptjentPaaHjelpefartoey: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    erOpptjentPaaKontinentalsokkel: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
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
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    oppgrossingsgrunnlag: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    trukketArtistskatt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class UtenlandskeMedFastAvgiftsbeloep:
    antallAvgiftsgrunnlagPersoner: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    beloepssatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class UtenlandskeMedSaerskiltProsentsats:
    avgiftsgrunnlagBeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    prosentsatsForAvgiftsberegning: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class Utleggstrekk:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    beloep: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    datoForUtleggstrekk: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class YrkePerMoenstring:
    yrkeskodePerMoenstring: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    antallTimerPerYrkeskodePerMoenstring: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class AldersUfoereEtterlatteAvtalefestetOgKrigspensjon:
    grunnpensjonsbeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    tilleggspensjonsbeloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    ufoeregrad: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    pensjonsgrad: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    heravEtterlattepensjon: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    tidsrom: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Arbeidsgiveravgift:
    loennOgGodtgjoerelse: list[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    tilskuddOgPremieTilPensjon: list[Arbeidsgiveravgiftsgrunnlag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    utenlandskeMedSaerskiltProsentsats: Optional[
        UtenlandskeMedSaerskiltProsentsats
    ] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    utenlandskeMedFastAvgiftsbeloep: Optional[
        UtenlandskeMedFastAvgiftsbeloep
    ] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    fradragIGrunnlagetForSone: list[FradragIGrunnlaget] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    fradragIGrunnlagetForUtenlandsk: Optional[
        FradragIGrunnlagetForUtenlandsk
    ] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    samletGrunnlagUnderOpplysningsplikt: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Betalingsinformasjon:
    sumForskuddstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sumArbeidsgiveravgift: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sumFinansskattLoenn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sumUtleggstrekk: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sumForskuddstrekkPerLoennsutbetalingsdato: list[
        BeloepPerLoennsutbetalingsdato
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class MoenstringPaaFartoey:
    moenstringsperiodeId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    fartoeyId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    paamoenstringsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    avmoenstringsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    yrkePerMoenstring: list[YrkePerMoenstring] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Nettoloennsordning:
    oppgrossingstabellnummer: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    bilinformasjon: Optional[BilOgBaat] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    betaltSkattebeloepIUtlandet: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class NorskKontinentalsokkel:
    tidsrom: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    gjelderLoennFoerste60Dager: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Arbeidsforhold:
    arbeidsforholdId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    typeArbeidsforhold: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    startdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sluttdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    antallTimerPerUkeSomEnFullStillingTilsvarer: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    avloenningstype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    yrke: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    arbeidstidsordning: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    stillingsprosent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sisteLoennsendringsdato: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    loennsansiennitet: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    loennstrinn: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 255,
        },
    )
    fartoey: Optional[Fartoey] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    permisjon: list[Permisjon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sisteDatoForStillingsprosentendring: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    aarsakTilSluttdato: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    formForAnsettelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    permittering: list[Permittering] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    moenstringPaaFartoey: list[MoenstringPaaFartoey] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Tilleggsinformasjon:
    bilOgBaat: Optional[BilOgBaat] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    dagmammaIEgenBolig: Optional[DagmammaIEgenBolig] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    etterbetalingsperiode: Optional[Periode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    inntektPaaNorskKontinentalsokkel: Optional[NorskKontinentalsokkel] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    inntjeningsforhold: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    livrente: Optional[Livrente] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    lottOgPart: Optional[LottOgPartInnenFiske] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    nettoloenn: Optional[Nettoloennsordning] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    pensjon: Optional[AldersUfoereEtterlatteAvtalefestetOgKrigspensjon] = (
        field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            },
        )
    )
    reiseKostOgLosji: Optional[ReiseKostOgLosji] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    utenlandskArtist: Optional[UtenlandskArtist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    bonusFraForsvaret: Optional[BonusFraForsvaret] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Loennsinntekt:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    spesifikasjon: Optional[Spesifikasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    antall: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Naeringsinntekt:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class PensjonEllerTrygd:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class YtelseFraOffentlige:
    beskrivelse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    tilleggsinformasjon: Optional[Tilleggsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Inntekt:
    skatteOgAvgiftsregel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    startdatoOpptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sluttdatoOpptjeningsperiode: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    fordel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    utloeserArbeidsgiveravgift: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    inngaarIGrunnlagForTrekk: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    beloep: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    arbeidsforholdId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    loennsinntekt: Optional[Loennsinntekt] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    ytelseFraOffentlige: Optional[YtelseFraOffentlige] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    pensjonEllerTrygd: Optional[PensjonEllerTrygd] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    naeringsinntekt: Optional[Naeringsinntekt] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Inntektsmottaker:
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    internasjonalIdentifikator: list[InternasjonalIdentifikator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    identifiserendeInformasjon: Optional[IdentifiserendeInformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    arbeidsforhold: list[Arbeidsforhold] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    fradrag: list[Fradrag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    forskuddstrekk: list[Forskuddstrekk] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    inntekt: list[Inntekt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    sjoefolksrelatertInformasjon: Optional[SjoefolksrelatertInformasjon] = (
        field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            },
        )
    )
    oppholdPaaSvalbardJanMayenOgBilandene: list[
        OppholdPaaSvalbardJanMayenOgBilandene
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    utleggstrekk: list[Utleggstrekk] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class Virksomhet:
    norskIdentifikator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    inntektsmottaker: list[Inntektsmottaker] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    arbeidsgiveravgift: Optional[Arbeidsgiveravgift] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class JuridiskEntitet:
    betalingsinformasjon: Optional[Betalingsinformasjon] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    betalingsinformasjonForForenkletOrdning: list[
        BetalingsinformasjonForForenkletOrdning
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    annenBagatellmessigStoette: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    virksomhet: list[Virksomhet] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )
    pensjonsinnretning: list[Pensjonsinnretning] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class leveranse:
    leveringstidspunkt: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    kalendermaaned: Optional[XmlPeriod] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "min_inclusive": XmlPeriod("2014-01"),
            "max_inclusive": XmlPeriod("2099-12"),
        },
    )
    kildesystem: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 255,
        },
    )
    erstatterMeldingsId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    meldingsId: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
            "max_length": 150,
            "pattern": r"([0-9a-zA-Z_.-])*",
        },
    )
    opplysningspliktig: Optional[Opplysningspliktig] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    oppgave: Optional[JuridiskEntitet] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )
    spraakForTilbakemelding: Optional[Spraak] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
        },
    )


@dataclass
class EDAG_M:
    Leveranse: Optional[leveranse] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ske:fastsetting:innsamling:a-meldingen:v2_3",
            "required": True,
        },
    )


@dataclass
class melding(EDAG_M):
    class Meta:
        namespace = "urn:ske:fastsetting:innsamling:a-meldingen:v2_3"
