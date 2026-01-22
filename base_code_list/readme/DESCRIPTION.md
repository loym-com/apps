This module adds the technical basis for the use of the code lists.
It is a copy of [base_unece](https://github.com/OCA/community-data-files/tree/18.0/base_unece).

Changes:

- unece.code.list -> code.list.item
- Use many2one ("list_id") instead of selection ("type") to associate a code with a list.

New:

- code.list
- code.list.mixin
- code.list.usage
