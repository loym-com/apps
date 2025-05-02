from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, ValidationError

class TowerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, model=None, date_begin=None, date_end=None, sortby=None, **kwargs):
        values = super()._prepare_home_portal_values(**kwargs)
        partner = request.env.user.partner_id
        values['tower_count'] = request.env['cx.tower.server'].search_count([('partner_id', '=', partner.id)])
        return values

    @http.route(['/my/databases', '/my/databases/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_towers(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        Tower = request.env['cx.tower.server']

        domain = [('partner_id', '=', partner.id)]

        # Count the total number of tower records
        tower_count = Tower.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/databases",
            total=tower_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager
        towers = Tower.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'databases': towers,
            'pager': pager,
            'default_url': '/my/databases',
        })
        return request.render("cetmix_tower_portal.portal_my_towers", values)

    @http.route(['/my/database/<int:tower_id>'], type='http', auth="user", website=True)
    def portal_my_tower(self, tower_id=None, access_token=None, **kw):
        try:
            tower_sudo = self._document_check_access('cx.tower.server', tower_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'database': tower_sudo,
        }
        return request.render("cetmix_tower_portal.portal_my_tower", values)

    @http.route('/my/databases/new', type='http', auth="user", website=True, sitemap=False)
    def new_database(self, **kw):
        countries = request.env['res.country'].search([])
        return request.render("cetmix_tower_portal.database_form", {'countries': countries})

    @http.route('/my/databases/create', type='http', auth="user", website=True, method=['POST'], csrf=False)
    def create_database(self, **post):
        partner = request.env.user.partner_id
        vals = {
            'partner_id': partner.id,
            'name': post.get('name'),
            'reference': post.get('name'),
            "ip_v4_address": "1.2.3.4",
            "ssh_username": "ssh_username",
            "ssh_password": "ssh_password",
            # 'version': post.get('version'),
            # 'company_name': post.get('company_name'),
            # 'country_id': int(post.get('country_id')),
            # 'category': post.get('category'),
        }
        existing_database = request.env['cetmix_tower_portal.database'].sudo().search([('name', '=', post.get('name'))], limit=1)
        if existing_database:
            vals["error"] = "A database with this name already exists. Please choose a different name."
            return request.render("cetmix_tower_portal.database_form", vals)
        try:
            request.env['cetmix.tower.server'].sudo().create(vals)
            return request.redirect('/my/database')
        except ValidationError as e:
            return request.render("cetmix_tower_portal.database_form", {'error': str(e)})
        except Exception as e:
            return request.render("cetmix_tower_portal.database_form", {'error': "An unexpected error occurred."})
