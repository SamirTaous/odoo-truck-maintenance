/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";

export class TruckOwnershipTreeController extends ListController {
    setup() {
        super.setup();
    }

    /**
     * Override to add ownership-specific CSS classes to rows
     */
    async _updateSelection() {
        await super._updateSelection();
        this._addOwnershipClasses();
    }

    /**
     * Add CSS classes based on ownership type
     */
    _addOwnershipClasses() {
        if (!this.model.root.records) return;
        
        const rows = this.el.querySelectorAll('.o_data_row');
        this.model.root.records.forEach((record, index) => {
            const row = rows[index];
            if (row && record.data.ownership_type) {
                // Remove existing ownership classes
                row.classList.remove('truck-owned', 'truck-rented', 'truck-subcontracted');
                
                // Add new ownership class
                const ownershipType = record.data.ownership_type;
                row.classList.add(`truck-${ownershipType}`);
            }
        });
    }
}

registry.category("views").add("truck_ownership_tree", {
    ...registry.category("views").get("list"),
    Controller: TruckOwnershipTreeController,
});