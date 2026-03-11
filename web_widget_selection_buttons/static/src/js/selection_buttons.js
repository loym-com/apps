/** @odoo-module **/
import { useState } from "@odoo/owl";
import AbstractField from "web.AbstractField";
import fieldRegistry from "web.field_registry";

export default class SelectionButtons extends AbstractField {
    setup() {
        super.setup();
        this.state = useState({ value: this.value });
    }

    _onClick(option) {
        this._setValue(option[0]);
        this.state.value = option[0];
    }
}

fieldRegistry.add("selection_buttons", SelectionButtons);
