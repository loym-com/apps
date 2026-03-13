/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import { Component, useState, onMounted, onWillStart, onWillUpdateProps, useRef } from "@odoo/owl";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {Many2ManyTagsField} from "@web/views/fields/many2many_tags/many2many_tags_field";

// Selection

export class SelectionButtonsField extends Component {
    static template = "web_widget_popover.SelectionButtonsField";

    setSelection(value) {
        this.props.update(value);
    }
}
registry.category("fields").add("selection_buttons", SelectionButtonsField);

// Relational (Many2one and Many2many)

function setupFetchRecords(context) {
    /* Use records because props.records disappears after clicking the buttons */
    context.records = useState([]);
    onWillStart(() => {
        const model = context.props.record.fields[context.props.name]?.relation;
        context.env.services.orm.searchRead(model, [], ["id", "display_name"])
            .then((records) => {
                context.records.splice(0, context.records.length, ...records);
            });
    });
}

// Many2one

export class Many2oneButtonsField extends Many2ManyTagsField {
    static template = "web_widget_popover.Many2oneButtonsField";

    setup() {
        super.setup();
        setupFetchRecords(this);
    }

    setMany2one(recordId) {
        this.props.update(recordId);
    }
}
registry.category("fields").add("many2one_buttons", Many2oneButtonsField);

// Many2many

export class Many2manyButtonsField extends Many2ManyTagsField {
    static template = "web_widget_popover.Many2manyButtonsField";

    setup() {
        super.setup();
        setupFetchRecords(this);
    }

    toggleMany2many(recordId) {
        const recordObj = { id: recordId }; // Convert recordId to an object

        const currentRecords = this.props.value?.records || [];
        const currentObjs = currentRecords.map(r => ({ id: r.data.id }));

        if (currentObjs.some(obj => obj.id === recordObj.id)) {
            // Deselect
            const ids = this.props.value.currentIds.filter((id) => id !== recordId);
            this.props.value.replaceWith(ids);
        } else {
            // Select
            this.update([recordObj]);
        }
    }
}
registry.category("fields").add("many2many_buttons", Many2manyButtonsField);
