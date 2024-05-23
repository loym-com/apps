from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


from . import amelding_v2_2 as a


edag = a.EdagM()

leveranse = edag.leveranse = a.Leveranse(
    leveringstidspunkt="2024-05-16",
    kalendermaaned="2024-05",
    kildesystem="Odoo",
    meldings_id="123",
)
leveranse.opplysningspliktig = a.Opplysningspliktig(
    norsk_identifikator="123456789",
)
leveranse.oppgave = a.JuridiskEntitet()


config = SerializerConfig(pretty_print=True)
serializer = XmlSerializer(config=config)
print(serializer.render(edag))

# l10n_no_payroll\models\amelding>   python -m generated.learn_xsdata
