STRUCTURE

Standard methods are applied in base and may be used by any model.
Customize a model's behaviour by overriding the standard methods:
- Control the flow with _teamm2odoo() and context
- Identify a record with _teamm2odoo_search_kwargs(kwargs)
- Add values to a record with _teamm2odoo_values(kwargs)


KWARGS

Use kwargs to identify a record and to set values for a record.
{
    "simple_field": "value",
    "many2one_field": id,
    "one2many_field": [ids],
    "many2many_field": [ids],
}


CONTEXT

Use context to send information from one method to another.

Always available:
    teamm_values
    teamm_params
Some places:
    teamm_bed_counter
    teamm_discount (name, amount)
    teamm_room_sharing


METHODS

_teamm2odoo(): 
    Decide whether or not to create one or multiple records
    Set context if needed
    Call _teamm2odoo_set_record() for one record at a time

_teamm2odoo_search_kwargs(kwargs): Identify a record.

_teamm2odoo_values(kwargs): Set values for a record.

