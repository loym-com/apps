from collections.abc import Iterable

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo(self):
        record = self._teamm2odoo_set_record()
        return record

    @api.model
    def _teamm2odoo_set_record(self):
        """
        kwargs are used both to search for and to create/update a record.
        kwargs format:
        {
            "simple_field": "value",
            "many2one_field": id,
            "one2many_field": [ids],
            "many2many_field": [ids],
        }
        """
        record = self._teamm2odoo_search()
        odoo_values = self._teamm2odoo_values({})
        if odoo_values:
            if len(record) == 1:
                record.write(odoo_values)
            else:
                record = record.create(odoo_values)
            record._teamm2odoo_after_create_or_write()
        return record

    @api.model
    def _teamm2odoo_values(self, kwargs):
        # Add param fields
        for model_field in self._teamm2odoo_fields():
            field = model_field.replace(self._name + ".", "")
            kwargs[field] = self._teamm2odoo_get_value(model_field)
        # Add search fields
        odoo_values = self._teamm2odoo_search_kwargs({}) | kwargs
        # Handle many2many
        for x2many_field, ids in self._teamm2odoo_x2many(odoo_values).items():
            if self._fields[x2many_field].type =="many2many":
                # This makes odoo_values different than kwargs
                odoo_values[x2many_field] = [fields.Command.set(ids)]
        return odoo_values

    @api.model
    def _teamm2odoo_search(self):
        domain = self._teamm2odoo_domain()
        if self._name == "product.product":
            debug = True
        # Don't search if there is no search domain
        record = self.search(domain) if domain else self
        x2many = self._teamm2odoo_x2many()
        if x2many:
            # Check if record.x2many_field.ids == kwargs[x2many_field]
            record = record.filtered(
                lambda r: all(
                    set(getattr(r, field).ids) == set(ids)
                    for field, ids in x2many.items()
                )
            )
        assert len(record) in (0, 1), f"Error: multiple records ({str(record)}) match the search {domain}."
        return record
    
    @api.model
    def _teamm2odoo_domain(self):
        kwargs = self._teamm2odoo_search_kwargs({})
        domain = []
        x2many = self._teamm2odoo_x2many()
        for key, value in kwargs.items():
            operator = "in" if key in x2many else "="
            domain.append((key, operator, value))
        return domain
    
    @api.model
    def _teamm2odoo_x2many(self, kwargs={}):
        kwargs = kwargs or self._teamm2odoo_search_kwargs({})
        x2many_kwargs = {
            key: val for key, val in kwargs.items()
            if self._fields[key].type in ("one2many", "many2many")
        }
        return x2many_kwargs
    
    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        kwargs = kwargs or self._teamm2odoo_default_kwargs()
        return kwargs
    
    @api.model
    def _teamm2odoo_default_kwargs(self):
        name = self._teamm2odoo_name()
        return {"name": name} if name else {}

    @api.model
    def _teamm2odoo_name(self):
        name = self.env.context.get(self._name)
        if name:
            return name
        else:
            names = self._teamm2odoo_names()
            return names[0] if names else None

    @api.model
    def _teamm2odoo_names(self):
        # Return list of names
        # E.g. a product template may have multiple product attributes.
        names = self._teamm2odoo_get_value(self._name)
        if names:
            return [str(name).strip() for name in names.split(",")]
        else:
            return []

    @api.model
    def _teamm2odoo_get_value(self, key):
        return self.env.context["teamm_values"][key]

    def _teamm2odoo_after_create_or_write(self):
        pass

    def _teamm2odoo_fields(self):
        """ TODO: teamm_fields with model, field, alias
        Params may be used to define fields to import.
        type:   code
        key:    model.name
        value:  field1, field2

        Aliases may be used to convert CSV header to model.name.field1
        name:   model.name.field1
        aliases:CSV header
        """
        fields = self.env.context["teamm_params"].get(self._name)
        if fields:
            return [f"{self._name}.{field.strip()}" for field in fields.split(",")]
        else:
            return []
