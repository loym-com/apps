# -*- coding: utf-8 -*-

from odoo import api, fields, models


class BaseModuleUpdate(models.TransientModel):
    _inherit = "base.module.update"

    def update_module(self):
        super().update_module()
        self.env["ir.module.module"].search([]).import_prices()
        return False
