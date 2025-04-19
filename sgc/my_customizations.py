import frappe

def copy_custom_fields_from_reference(doc, method):
    for item in doc.items:
        reference_item = None

        if item.so_detail:
            reference_item = frappe.get_doc("Sales Order Item", item.so_detail)
        elif item.dn_detail:
            reference_item = frappe.get_doc("Delivery Note Item", item.dn_detail)
        elif item.si_detail:
            reference_item = frappe.get_doc("Sales Invoice Item", item.si_detail)

        if reference_item:
            item.custom_width = reference_item.custom_width
            item.custom_length = reference_item.custom_length
            item.custom_updated_quantity = reference_item.custom_updated_quantity
            item.qty = reference_item.qty  # or recompute if needed

def set_qty_in_sales_order(doc, method):
    for item in doc.items:
        updated_qty = (
            (item.custom_updated_quantity or 1)
            * (item.custom_width or 1)
            * (item.custom_length or 1)
        )
        item.qty = updated_qty

