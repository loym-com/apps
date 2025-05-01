from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError

class TowerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, model=None, date_begin=None, date_end=None, sortby=None, **kwargs):
        values = super()._prepare_home_portal_values(**kwargs)
        partner = request.env.user.partner_id

        tower_count = request.env['cx.tower.server'].search_count([('partner_id', '=', partner.id)])
        values['tower_count'] = tower_count

        return values

    @http.route(['/my/towers', '/my/towers/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_towers(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        Tower = request.env['cx.tower.server']

        domain = [('partner_id', '=', partner.id)]

        # Count the total number of tower records
        tower_count = Tower.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/towers",
            total=tower_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager
        towers = Tower.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'towers': towers,
            'pager': pager,
            'default_url': '/my/towers',
        })
        return request.render("cetmix_tower_portal.portal_my_towers", values)

    @http.route(['/my/tower/<int:tower_id>'], type='http', auth="user", website=True)
    def portal_my_tower(self, tower_id=None, access_token=None, **kw):
        try:
            tower_sudo = self._document_check_access('cx.tower.server', tower_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'tower': tower_sudo,
        }
        return request.render("cetmix_tower_portal.portal_my_tower", values)
