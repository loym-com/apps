import io

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.convert import convert_xml_import

from . import app_templates as t

def iterate_recursively(record):
    """
    Generator som returnerer record og alle descendants
    i rekkefølge basert på _order.
    """
    yield record
    for child in record.child_ids:
        yield from iterate_recursively(child)


class AppMenuitem(models.Model):
    _name = "app.menuitem"
    _description = "app.menuitem"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence"

    name = fields.Char()
    code = fields.Char()
    type = fields.Selection(
        selection=[
            ('parent', 'Submenus'),
            ('model', 'Content'),
            # ('action', 'Action'),
        ],
    )
    parent_id = fields.Many2one(
        comodel_name="app.menuitem",
        domain="[('type', '=', 'parent')]",
    )
    child_ids = fields.One2many(
        comodel_name="app.menuitem",
        inverse_name="parent_id",
    )
    action_id = fields.Reference(
        selection=[('ir.actions.report', 'ir.actions.report'), ('ir.actions.act_window', 'ir.actions.act_window'), ('ir.actions.act_url', 'ir.actions.act_url'), ('ir.actions.server', 'ir.actions.server'), ('ir.actions.client', 'ir.actions.client')],
    )
    ir_model_id = fields.Many2one(
        comodel_name="ir.model",
    )
    field_ids = fields.One2many(
        comodel_name="app.field",
        inverse_name="menuitem_id",
        string="Fields",
    )
    sequence = fields.Integer(default=10)

    def action_open_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'app.menuitem',
            'view_mode': 'form',
            'res_id': self.id,
        }

    def action_create_app(self):
        self.ensure_one()
        assert not self.parent_id, "Only top-level menuitems can create/update apps"

        self._create_views()
        # Create menuitems

    def _create_views(self):
        module_name = self.code
        menuitems = self.search([('type', '=', 'model'), ('id', 'child_of', self.id)])
        for menuitem in menuitems:
            model_views_xml = menuitem.get_model_views_xml()
            model_views_io = io.BytesIO(model_views_xml.encode('utf-8'))
            model_views_io.name = f"{menuitem.ir_model_id.model.replace('.', '_')}_views.xml"
            convert_xml_import(self.env.cr, module_name, model_views_io)
            # path = f"/tmp/{menuitem.ir_model_id.model.replace('.', '_')}_views.xml"
            # with open(path, "w") as f:
            #     f.write(model_views_xml)
            # path = app_path + "/views/" + model["model.underscore"] + "_views.xml"
            # with open(path, "w") as f:
            #     f.write(model_views_xml)

        menus_xml = self.get_menus_xml()
        menus_io = io.BytesIO(menus_xml.encode('utf-8'))
        menus_io.name = "menus.xml"
        convert_xml_import(self.env.cr, module_name, menus_io)
        # with open(app_path + "/views/menus.xml", "w") as f:
        #     f.write(menus_xml)

    def get_menus_xml(self):
        menus_xml = []

        for menu in iterate_recursively(self):
            attr = {
                'name': menu.name,
                'sequence': str(menu.sequence),
            }
            if menu.parent_id:
                attr["parent"] = f"{menu.parent_id.code}_menu"

            if menu.type == "parent":
                attr["id"] = f"{menu.code}_menu"
            elif menu.type == "model":
                model_underscore = menu.ir_model_id.model.replace('.', '_')
                attr["id"] = f"{model_underscore}_menu"
                attr["action"] = f"{model_underscore}_action"
            # elif menu.type == "action":
            #     attr["id"] = f"{menu.code}_menu"
            else:
                continue
            # raise UserError(f"XML: {attr}")
            attr_xml = etree.Element("menuitem", attrib=attr)
            attr_str = etree.tostring(attr_xml).decode('utf-8')
            menus_xml.append(attr_str)

        return t.xml.format(content="".join(menus_xml))

    def get_model_views_xml(self):
        module = self
        while module.parent_id:
            module = module.parent_id

        model_title = self.ir_model_id.name
        model_dot = self.ir_model_id.model
        model_underscore = model_dot.replace(".", "_")
        form_fields = []
        list_fields = []
        search_fields = []
        search_group_by_fields = []

        for field in self.field_ids:
            if field.ir_model_id.model == model_dot:
                form = " ".join(
                    [
                        f'{attr.attribute_id.code}="{attr.value_char}"'
                        for attr in field.attribute_ids.filtered(lambda a: a.view == "form")
                    ]
                )
                list = 'optional="show" '
                if field.ir_model_fields_id.ttype in ("One2many", "Many2many"):
                    list += 'widget="many2many_tags" '
                fld_underscore = field.ir_model_fields_id.name
                form_fields.append(t.field.format(field=fld_underscore, extra=form))
                list_fields.append(t.field.format(field=fld_underscore, extra=list))
                search_fields.append(t.field.format(field=fld_underscore, extra=""))
                title = field.ir_model_fields_id.field_description
                search_group_by_fields.append(
                    t.group_by_field.format(field=fld_underscore, field_title=title)
                )

        form_group = t.group.format(content="".join(form_fields))
        form_sheet = t.sheet.format(content=form_group)
        form_view = t.view.format(
            model=model_dot,
            _model_=model_underscore,
            view="form",
            content=form_sheet,
        )
        list_view = t.view.format(
            model=model_dot,
            _model_=model_underscore,
            view="tree",
            content="".join(list_fields),
        )
        kanban_view = t.view.format(
            model=model_dot,
            _model_=model_underscore,
            view="kanban",
            content=t.kanban,
        )
        pivot_view = t.view.format(
            model=model_dot,
            _model_=model_underscore,
            view="pivot",
            content="",
        )
        search_group_by = t.group_by.format(content="".join(search_group_by_fields))
        search_view = t.view.format(
            model=model_dot,
            _model_=model_underscore,
            view="search",
            content="".join(search_fields) + search_group_by,
        )
        action = t.action.format(
            module=module.code,
            model_title=model_title,
            model=model_dot,
            _model_=model_underscore,
        )
        xml = t.xml.format(
            content=form_view + list_view + kanban_view + pivot_view + search_view + action
        )
        return xml
