IMPLEMENTATION:
ir.sequence with code = l10n.no.amelding

Generate the csv files from l10n_no_payroll.xlsm


Hints how to develop the amelding:

OCA Days 2021 https://www.youtube.com/watch?v=6gFOe7Wh8uA

python3.10 -m pip install xsdata[cli]==23.8
The version should be from the same time when https://github.com/akretion/xsdata-odoo was last updated.

linux:
XSDATA_SCHEMA="amelding" XSDATA_VERSION="22" xsdata amelding_v2_2.xsd --output=odoo
windows:
cmd /c "set XSDATA_SCHEMA=amelding& set XSDATA_VERSION=22& xsdata amelding_v2_2.xsd --output=odoo"
