odoo.define('website_sale_preorder.form', function (require) {
'use strict';

const core = require('web.core');
var FormEditorRegistry = require('website.form_editor_registry');

const _lt = core._lt;

FormEditorRegistry.add('create_product', {
    formFields: [{
        type: 'char',
        modelRequired: true,
        name: 'external_name',
        string: _lt('Product Name'),
    }, {
        type: 'char',
        modelRequired: true,
        name: 'external_url',
        string: _lt('Link to product'),
    }, {
        type: 'float',
        modelRequired: true,
        name: 'external_price',
        string: _lt('Price (USD)'),
    }],
});

});
