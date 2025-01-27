IMPLEMENTATION

ir.sequence with code = l10n.no.amelding

## How to update yearly taxes

https://www.skatteetaten.no/satser/trekktabeller-i-tekstformat/

Download zip, copy list to tabelltrekk2025.py

Update l10n_no_tabelltrekk.py

```
from .tabelltrekk2025 import tabelltrekk as tabelltrekk20xx

YEAR = 2025
```

## How to update to a new version of amelding

OCA Days 2021 https://www.youtube.com/watch?v=6gFOe7Wh8uA

```bash
python3.10 -m pip install xsdata[cli]
python3.10 -m pip install xsdata-pydantic[cli]

cd models/amelding
xsdata generate amelding_v2_3.xsd
```

Replace **Leveranse** with **leveranse** in amelding_v2_3.py in two places.

```
@dataclass
class leveranse:

@dataclass
class EDAG_M:
    Leveranse: Optional[leveranse] = field(
```

Generate csv files from l10n_no_payroll.xlsm


## Technical notes

xsdata:      xsd thisWay changes by default to this_way (snake_case)
xsdata-odoo: xsd thisWay ------------> amelding_thisWay
So I would like xsdata to output                thisWay (camelCase)
This is configured in .xsdata.xml


Not relevant because we are not using xsdata-odoo:
The version should be from the same time when https://github.com/akretion/xsdata-odoo was last updated.

linux:
XSDATA_SCHEMA="amelding" XSDATA_VERSION="22" xsdata amelding_v2_2.xsd --output=odoo
windows:
cmd /c "set XSDATA_SCHEMA=amelding& set XSDATA_VERSION=22& xsdata amelding_v2_2.xsd --output=odoo"
