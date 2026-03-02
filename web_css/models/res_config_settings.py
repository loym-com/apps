import base64

from odoo import api, fields, models

VARIABLES = {
    "FIELD": "scss_variables",
    "BUNDLE": "web._assets_primary_variables",
    "TARGET": "web_css/static/src/scss/variables.scss",
    "SCSS": """
/*
Example:
$o-brand-odoo: #714B67;
$o-brand-primary: #017e84;
$o-border-radius: .5rem;
$o-view-background-color: pink;
$o-webclient-background-color: purple;
*/
"""
}
BACKEND = {
    "FIELD": "scss_backend",
    "BUNDLE": "web.assets_backend",
    "TARGET": "web_css/static/src/scss/backend.scss",
    "SCSS": """
/*
Example:
div.o_kanban_renderer {
    background-color: white;
}
*/
"""
}

def PATH(ITEM):
    return f"/_custom/{ITEM['BUNDLE']}/{ITEM['TARGET']}"


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    scss_variables = fields.Char(
        string="CSS Variables",
        config_parameter="web_css.scss_variables",
        help="Add your custom SCSS here. It will be included in the backend assets.",
        default=VARIABLES["SCSS"],
    )
    scss_backend = fields.Char(
        string="Backend CSS",
        config_parameter="web_css.scss_backend",
        help="Add your custom CSS here. It will be included in the backend assets.",
        default=BACKEND["SCSS"],
    )

    def set_values(self):
        res = super().set_values()

        for ITEM in [VARIABLES, BACKEND]:
            asset = self.env["ir.asset"].search([("path", "=", PATH(ITEM))])
            attachment = self.env["ir.attachment"].search([("url", "=", PATH(ITEM))])
            if asset or attachment:
                asset.ensure_one()
                attachment.ensure_one()

                current = (getattr(self, ITEM["FIELD"]) or "").strip()
                existing = base64.b64decode(attachment.datas).decode("utf-8").strip()
                if current == existing:
                    continue

                datas = base64.b64encode(current.encode("utf-8"))
                attachment.write({"datas": datas})
                self.env.registry._clear_cache()
            else:
                attachment_values = {
                    "name": PATH(ITEM),
                    "type": "binary",
                    "mimetype": "text/scss",
                    "datas": datas,
                    "url": PATH(ITEM),
                }
                asset_values = {
                    "name": PATH(ITEM),
                    "directive": "replace",
                    "bundle": ITEM["BUNDLE"],
                    "target": ITEM["TARGET"],
                    "path": PATH(ITEM),
                    
                }
                self.env["ir.attachment"].create(attachment_values)
                self.env["ir.asset"].create(asset_values)

        return res

    def reset_scss(self):
        self.env["ir.asset"].search([("path", "=", PATH(VARIABLES))]).unlink()
        self.env["ir.attachment"].search([("url", "=", PATH(VARIABLES))]).unlink()
        self.env["ir.asset"].search([("path", "=", PATH(BACKEND))]).unlink()
        self.env["ir.attachment"].search([("url", "=", PATH(BACKEND))]).unlink()
