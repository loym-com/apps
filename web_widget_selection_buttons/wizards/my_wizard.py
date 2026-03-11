from odoo import api, fields, models


class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _inherit = ['multi.step.wizard.mixin']

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        name="Contact",
        required=True,
        ondelete='cascade',
        default=lambda self: self._default_partner_id(),
    )
    name = fields.Char()
    field1 = fields.Char()
    field2 = fields.Char()
    field3 = fields.Char()

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('configure', 'Configure'),
            ('custom', 'Customize'),
            ('final', 'Final'),
        ]

    @api.model
    def _default_partner_id(self):
        # return self.env.context.get('active_id')
        return self.env.user.partner_id

    def state_exit_start(self):
        self.state = 'configure'

    def state_exit_configure(self):
        self.state = 'custom'

    def state_exit_custom(self):
        self.state = 'final'
