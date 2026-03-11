from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'Demo: Selection Buttons OWL16'

    name = fields.Char(string='Name')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
        ],
        string='State',
        default='draft',
    )
