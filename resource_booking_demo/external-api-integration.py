# HOW TO USE
# Create a new database and install
# - resource_booking_demo
# - partner_firstname
# - sale_start_end_dates
# Set the DEV variables url & db below.
# python external-api-integration.py DEV

# THIS SCRIPT DEPENDS ON THESE ODOO MODULES:
# partner_contact_birthdate (OCA/partner-contact)
# partner_contact_gender (OCA/partner-contact)
# partner_firstname (OCA/partner-contact)
# partner_product_price (OCA/partner-contact PR 1660)
# resource_booking (OCA/calendar)
# sale_resource_booking (OCA/sale-workflow PR 2661)
# website_sale_resource_booking (OCA/e-commerce PR 851)
# resource_booking_demo (loymcom/dev)
# product_pack (OCA/product-pack PR 147)
# account_invoice_start_end_dates (OCA/account-closing)
# sale_start_end_dates (OCA/sale-workflow)
# contacts (optional)
# sale_management (optional)

# git clone https://github.com/loymcom/dev.git

# git clone https://github.com/OCA/account-closing.git

# git clone https://github.com/OCA/calendar.git

# git clone https://github.com/OCA/e-commerce.git
# git pull origin pull/851/head:16.0-mig-website_sale_resource_booking

# git clone https://github.com/OCA/partner-contact.git
# git pull origin pull/1660/head:16.0-add-partner_product_price

# git clone https://github.com/OCA/product-attribute.git

# git clone https://github.com/OCA/product-pack.git
# git pull origin pull/147/head:16.0-fix-product_pack

# git clone https://github.com/OCA/sale-workflow.git
# git pull origin pull/2661/head:16.0-mig-sale_resource_booking

import xmlrpc.client
import random
import string
import sys

VARIABLES = {
    "PROD": {
        "url": "",
        "db": "",
        "username": "",
        "password": "",
        "product_attribute_id": 15,
        "product_category_id": 78,
        "resource_calendar_id": 103,
    },
    "TEST": {
        "url": "",
        "db": "",
        "username": "",
        "password": "",
        # WITHOUT DEMO
        "product_attribute_id": 2, # Room option
        "product_category_id": 1, # Generic category
        "resource_calendar_id": 4, # Available 24/7
    },
    "DEV": {
        "url": "http://localhost:16069",
        "db": "nodemo",
        "username": "admin",
        "password": "admin",
        # WITHOUT DEMO
        "product_attribute_id": 2, # Room option
        "product_category_id": 1, # Generic category
        "resource_calendar_id": 4, # Available 24/7
    },
}

def show(key, value):
    print("{} = {}".format(key, value))

class integrate():

    def __init__(self, var):
        self.var = var

        # Prevent errors on creating multiple test records with the same name
        self.unique_str = ''.join(random.choices(string.digits, k=5))

        # GENERAL ##############################################################################

        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(var["url"]))
        print("common = {}".format(self.common.version()))

        self.uid = self.common.authenticate(var["db"], var["username"], var["password"], {})
        print("uid = {}".format(self.uid))

        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(var["url"]))

    def do(self, model, method, args, kwargs):
        """ Do something in Odoo. """
        return self.models.execute_kw(self.var["db"], self.uid, self.var["password"], model, method, args, kwargs)

    def ref(self, external_id, model):
        """ Get the internal id from an external id (if it exists).
        Check that the model is correct. """

        module, name = external_id.split(".")
        result_list = self.do("ir.model.data", "search_read", [], {
            "domain": [("module", "=", module), ("name", "=", name)],
            "fields": ["model", "res_id"],
        })
        if len(result_list) == 1:
            if model:
                assert result_list[0]["model"] == model
            return result_list[0]["res_id"]

    # CONTACT ############################################################################

    def do_contact(self, hubspot_str, do_all=False):

        country_id = self.ref("base.no", "res.country")
        partner = {
            "firstname": "First Name",
            "lastname": "Last Name",
            "type": "contact",
            "street": "Address Line 1",
            "street2": "Address Line 2",
            "zip": "3614",
            "city": "Kongsberg",
            "country_id": country_id,
            "phone": "12345678",
            "mobile": "98765432",
            "email": "my@email.com",
            "ref": hubspot_str,
        }

        # search, create, read, write, copy, unlink (delete), deduplicate

        partner_ids = self.do("res.partner", "search", [ [["ref", "=", hubspot_str]] ], {})

        partner_ids += self.do("res.partner", "create", [ [partner] ], {})

        keep_partner_id = partner_ids[0]

        if do_all:

            partners_values = self.do("res.partner", "read", [ partner_ids ], {})

            self.do("res.partner", "write", [ partner_ids, {"firstname": "Kari"} ], {})

            new_partner_id = self.do("res.partner", "copy", [ partner_ids[0] ], {})

            self.do("res.partner", "unlink", [ new_partner_id ], {})

            # Deduplicate contacts
            if len(partner_ids) > 3:
                partner_ids = partner_ids[:3]
            wizard = {"partner_ids": partner_ids, "dst_partner_id": keep_partner_id}
            wizard_id = self.do("base.partner.merge.automatic.wizard", "create", [wizard], {'context': {'active_model': 'res.partner', 'active_ids': partner_ids}})
            self.do("base.partner.merge.automatic.wizard", "action_merge", [ [wizard_id] ], {})

        return keep_partner_id

    # BOOKING CONFIG ##############################################################

    def do_booking_type(self, type):

        # E.g. single room, double room private, double room shared

        resource_booking_type = {
            "name": "Standard double room, {} {}".format(type, self.unique_str),
            "duration": 240,
            "slot_duration": 24,
            "resource_calendar_id": self.var["resource_calendar_id"],
        }
        [resource_booking_type_id] = self.do("resource.booking.type", "create", [ [resource_booking_type] ], {})

        return resource_booking_type_id

    def do_booking_setup(self, resource_booking_type_id_private, resource_booking_type_id_shared):

        # For a double room:
        # Create resource.resource (2 records: bed 1, bed 2)
        # Create resource.booking.combination (3 records: bed 1, bed 2, bed 1 + 2)
        # Create resource.booking.type.combination.rel (3 records)

        resource_resource_list = [
            {
                "name": "Standard double room {}, bed 1".format(self.unique_str),
                "resource_type": "material",
                "calendar_id": self.var["resource_calendar_id"],
            },
            {
                "name": "Standard double room {}, bed 2".format(self.unique_str),
                "resource_type": "material",
                "calendar_id": self.var["resource_calendar_id"],
            },
        ]
        resource_resource_ids = self.do("resource.resource", "create", [ resource_resource_list ], {})

        resource_booking_combination_private = {"resource_ids": [(6, 0, resource_resource_ids )]} # SET = 6 (CLEAR + LINK a list)
        [resource_booking_combination_id_private] = self.do("resource.booking.combination", "create", [ [resource_booking_combination_private] ], {})

        resource_booking_combination_shared_list = [
            {"resource_ids": [ (4, resource_resource_ids[0]) ]}, # LINK one = 4
            {"resource_ids": [ (4, resource_resource_ids[1]) ]}, # LINK one = 4
        ]
        resource_booking_combination_ids_shared = self.do("resource.booking.combination", "create", [ resource_booking_combination_shared_list ], {})

        resource_booking_type_combination_rel_list = [
            {
                "type_id": resource_booking_type_id_private,
                "combination_id": resource_booking_combination_id_private,
            },
            {
                "type_id": resource_booking_type_id_shared,
                "combination_id": resource_booking_combination_ids_shared[0],
            },
            {
                "type_id": resource_booking_type_id_shared,
                "combination_id": resource_booking_combination_ids_shared[1],
            },
        ]
        resource_booking_type_combination_rel_ids = self.do("resource.booking.type.combination.rel", "create", [ resource_booking_type_combination_rel_list ], {})

        return resource_booking_combination_id_private, resource_booking_combination_ids_shared

    # PRODUCT ##############################################################################

    def do_product_attribute_value(self, type, resource_booking_type_id):

        # Create a room option (last part of the pack name).

        product_attribute_value = {
            "attribute_id": self.var["product_attribute_id"],
            "name": "Standard double {} {}".format(type, self.unique_str),
            "resource_booking_type_id": resource_booking_type_id,
        }
        [product_attribute_value_id] = self.do("product.attribute.value", "create", [ [product_attribute_value] ], {})

        return product_attribute_value_id

    def do_product(self, product_attribute_value_id_private, resource_booking_type_id_private,
                         product_attribute_value_id_shared, resource_booking_type_id_shared):

        # Create a program (first part of the pack name).

        product_template = {
            "name": "Newstart Gull 10 dagers opphold" + self.unique_str,
            "sale_ok": True,
            "type": "service",
            "categ_id": self.var["product_category_id"],
            "list_price": 10000,
        }
        [product_template_id] = self.do("product.template", "create", [ [product_template] ], {})

        # Create a program attribute line (linking a room option to the program).

        product_template_attribute_line = {
            "product_tmpl_id": product_template_id,
            "attribute_id": self.var["product_attribute_id"],
            "value_ids": [ [6, 0, [product_attribute_value_id_private] ] ], # SET = 6 (CLEAR + LINK a list)
        }
        [product_template_attribute_line_id] = self.do("product.template.attribute.line", "create", [ [product_template_attribute_line] ], {})

        # Link a new room option to the program attribute line.

        write = {"value_ids": [ [4, product_attribute_value_id_shared] ]} # LINK one = 4
        self.do("product.template.attribute.line", "write", [ [product_template_attribute_line_id], write ], {}) # This will auto-create a new product.product.

        # Get the pack id.

        def get_search(product_template_id, product_attribute_value_id):
            return [
                ["product_tmpl_id", "=", product_template_id],
                ["product_template_attribute_value_ids.product_attribute_value_id", "=", product_attribute_value_id],
            ]
        [product_product_id_private] = self.do("product.product", "search", [ get_search(product_template_id, product_attribute_value_id_private) ], {})
        [product_product_id_shared] = self.do("product.product", "search", [ get_search(product_template_id, product_attribute_value_id_shared) ], {})

        self.do("product.product", "write", [ [product_product_id_private], {"resource_booking_type_id": resource_booking_type_id_private} ], {})
        self.do("product.product", "write", [ [product_product_id_shared], {"resource_booking_type_id": resource_booking_type_id_shared} ], {})

        return product_product_id_private, product_product_id_shared

    # SALE ORDER #########################################################################

    def do_sale_order(self, partner_id, product_product_id):

        sale_order = {
            "partner_id": partner_id,
        }
        [sale_order_id] = self.do("sale.order", "create", [ [sale_order] ], {})

        sale_order_line = {
            "order_id": sale_order_id,
            "product_id": product_product_id,
            "start_date": "2024-05-15",
            "end_date": "2024-05-25",
            "product_uom_qty": 1, # will auto-create 1 booking if the product.product resource_booking_type_id is set.
            "price_unit": 10000,
        }
        [sale_order_line_id] = self.do("sale.order.line", "create", [ [sale_order_line] ], {})

        return sale_order_id, sale_order_line_id

    # BOOKING ############################################################################

    def do_booking(self, sale_order_id, sale_order_line_id, resource_booking_combination_id):

        self.do("sale.order", "action_bookings_resync", [ [sale_order_id] ], {})
        sale_order_line_values = self.do("sale.order.line", "read", [ [sale_order_line_id] ], {})[0]

        resource_booking_id = sale_order_line_values["resource_booking_id"][0]
        write = {
            "combination_id": resource_booking_combination_id,
            "start": sale_order_line_values["start_date"],
            "stop": sale_order_line_values["end_date"],
        }
        self.do("resource.booking", "write", [ [resource_booking_id], write ], {})

        return resource_booking_id

    def do_change_dates(self, sale_order_line_id, resource_booking_id, start_date, end_date):

        self.do("sale.order.line", "write", [ [sale_order_line_id], {"start_date": start_date, "end_date": end_date} ], {})
        self.do("resource.booking", "write", [ [resource_booking_id], {"start": start_date, "stop": end_date} ], {})

    # PAYMENT LINK #########################################################################

    def do_payment_link(self, sale_order_id):

        wizard_id = self.do("payment.link.wizard", "create", [{}], {'context': {'active_model': 'sale.order', 'active_id': sale_order_id}})
        print(wizard_id)

        # testnow = self.do("payment.link.wizard", "read", [ [wizard_id] ], {})
        # testnow = self.do("res.partner", "read", [ partner_ids ], {})

        # wizard = self.do("payment.link.wizard", "read", [ [wizard_id] ], {})
        # wizard = self.do("payment.link.wizard", "browse", [ [wizard_id] ], {})
        wizard = self.do("payment.link.wizard", "read", [ [wizard_id] ], {"fields": ["link"]})
        print(wizard)
        payment_link = wizard[0]["link"]

        return payment_link

############################################################################################
# MAIN #####################################################################################
############################################################################################

will = integrate(VARIABLES[sys.argv[1]])

# CONTACT

hubspot_str = "12345" # Search in Odoo for a contact with this Hubspot ID.
partner_id = will.do_contact(hubspot_str)
show("partner_id", partner_id)

# BOOKING types

resource_booking_type_id_private = will.do_booking_type("private")
print("Double room configuration")
show("resource_booking_type_id_private", resource_booking_type_id_private)

resource_booking_type_id_shared = will.do_booking_type("shared")
show("resource_booking_type_id_shared", resource_booking_type_id_shared)

# Specific room to book, 2 options (private or shared)

resource_booking_combination_id_private, resource_booking_combination_ids_shared = will.do_booking_setup(
    resource_booking_type_id_private, resource_booking_type_id_shared
)
show("resource_booking_combination_id_private (bed 1 and 2)", resource_booking_combination_id_private)
show("resource_booking_combination_ids_shared (bed 1, bed 2)", resource_booking_combination_ids_shared)

# PRODUCT attributes and products

product_attribute_value_id_private = will.do_product_attribute_value("private", resource_booking_type_id_private)
product_attribute_value_id_shared = will.do_product_attribute_value("shared", resource_booking_type_id_shared)
show("product_attribute_value_id_private", product_attribute_value_id_private)
show("product_attribute_value_id_shared", product_attribute_value_id_shared)

product_product_id_private, product_product_id_shared = will.do_product(
    product_attribute_value_id_private, resource_booking_type_id_private,
    product_attribute_value_id_shared, resource_booking_type_id_shared,
)
show("product_product_id_private", product_product_id_private)
show("product_product_id_shared", product_product_id_shared)

# SALE ORDER, BOOKING, PAYMENT LINK

# product_product_id_private = 45
# partner_id = 58

sale_order_id, sale_order_line_id = will.do_sale_order(partner_id, product_product_id_private)
show("sale_order_id", sale_order_id)
show("sale_order_line_id", sale_order_line_id)

resource_booking_id = will.do_booking(
    sale_order_id, sale_order_line_id, resource_booking_combination_id_private
)
show("resource_booking_id", resource_booking_id)

will.do_change_dates(sale_order_line_id, resource_booking_id, "2024-09-10", "2024-09-20")

payment_link = will.do_payment_link(sale_order_id)
show("payment_link", payment_link)
