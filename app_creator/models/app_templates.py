manifest = """
{{
    "name": "{app_title}",
    "data": [{data}
        "views/menus.xml",
        "security/ir.model.access.csv",
    ],
    "depends": [
        "mail",
    ],
    "version": "1.0",
}}
"""

manifest_data = """\n        "views/{_model_}_views.xml","""

# MODEL

init = "from . import {_model_}\n"

model = """from odoo import api, fields, models

class {Model}(models.Model):
    _name = "{model}"
    _description = "{model}"
    _inherit = ['mail.thread', 'mail.activity.mixin']
{fields_py}
"""

model_field = """\n    {field} = fields.{ttype}({attrs}\n    )"""

model_field_attr = "\n        {attr}={value},"
model_field_attr_quote = """\n        {attr}="{value}","""

# ACCESS

access_header = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
access_line = "access_{_model_},{model},model_{_model_},{group_extid},1,1,1,1\n"

# XML

xml = """<?xml version="1.0" encoding="utf-8" ?>
<odoo>{content}
</odoo>
"""

view = """
    <record id="{_model_}_view_{view}" model="ir.ui.view">
        <field name="name">{model}.view.{view}</field>
        <field name="model">{model}</field>
        <field name="priority" eval="100"/>
        <field name="arch" type="xml">
            <{view}>{content}
            </{view}>
        </field>
    </record>"""

kanban = """
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <field name="display_name" />
                        </div>
                    </t>
                </templates>"""

group_by_field = """
                    <filter
                        string="{field_title}"
                        name="{field}"
                        context="{{'group_by':'{field}'}}"
                    />"""

group_by = """
                <group string="Group By">{content}
                </group>"""

sheet = """
                <sheet>{content}
                </sheet>
                <!-- <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div> -->"""

group = """
                    <group>{content}
                    </group>"""

field = """
                        <field name="{field}" {extra}/>"""

action = """
    <record id="{_model_}_action" model="ir.actions.act_window">
        <field name="name">{model_title}</field>
        <field name="res_model">{model}</field>
        <field name="view_mode">tree,kanban,pivot,form</field>
    </record>
    <record id="{_model_}_action_tree" model="ir.actions.act_window.view">
        <field name="act_window_id" ref="{_model_}_action"/>
        <field name="view_mode">tree</field>
        <field name="view_id" ref="{_model_}_view_tree"/>
    </record>
    <record id="{_model_}_action_form" model="ir.actions.act_window.view">
        <field name="act_window_id" ref="{_model_}_action"/>
        <field name="view_mode">form</field>
        <field name="view_id" ref="{_model_}_view_form"/>
    </record>
    <record id="{_model_}_action_kanban" model="ir.actions.act_window.view">
        <field name="act_window_id" ref="{_model_}_action"/>
        <field name="view_mode">kanban</field>
        <field name="view_id" ref="{_model_}_view_kanban"/>
    </record>
    <record id="{_model_}_action_pivot" model="ir.actions.act_window.view">
        <field name="act_window_id" ref="{_model_}_action"/>
        <field name="view_mode">pivot</field>
        <field name="view_id" ref="{_model_}_view_pivot"/>
    </record>
    
    """
