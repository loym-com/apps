from odoo import api, fields, models

from . import app_templates as t


class AppMenuitem(models.Model):
    _name = "app.menuitem"
    _description = "app.menuitem"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    type = fields.Selection(
        selection=[('parent', 'Submenus'), ('model', 'Content'), ('action', 'Action')],
    )
    parent_id = fields.Many2one(
        comodel_name="app.menuitem",
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
    )

    def action_create_app(self):
        self.ensure_one()
        assert not self.parent_id, "Only top-level menuitems can create/update apps"
        # Create views
        # Create actions
        # Create menuitems

    def _create_views(self):
        menuitems = self.search([('type', '=', 'model'), ('id', 'child_of', self.id))]))
        for menuitem in menuitems:
            model_views_xml = menuitem.get_model_views_xml()
            # path = app_path + "/views/" + model["model.underscore"] + "_views.xml"
            # with open(path, "w") as f:
            #     f.write(model_views_xml)

        # menus_xml = get_menus_xml(app, models)
        # with open(app_path + "/views/menus.xml", "w") as f:
        #     f.write(menus_xml)

    def get_model_views_xml(self):
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
                    t.group_by_field.format(field=field[fld_underscore], field_title=title)
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
            model_title=model_title,
            model=model_dot,
            _model_=model_underscore,
        )
        xml = t.xml.format(
            content=form_view + list_view + kanban_view + pivot_view + search_view + action
        )
        return xml
