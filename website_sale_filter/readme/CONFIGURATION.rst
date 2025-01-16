See below how to implement. See also website_event_sale_resource_booking.


.. code-block:: python

from odoo import _, models
from odoo.addons.website_sale_filter.controllers.main import WebsiteSaleFilter


class Website(models.Model):
    _inherit = "website"
    
    def _website_sale_filters(self):
        filters = super()._website_sale_filters()
        filters.append(
            WebsiteSaleFilter(
                priority=50,
                display_type="select",
                related_field="combination_id",
                model_name="resource.booking.combination",
                visible_name=_("Booking"),
            )
        )
        return filters
