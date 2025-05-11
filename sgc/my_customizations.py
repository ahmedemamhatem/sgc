import frappe

def copy_custom_fields_from_reference(doc, method):
    """
    Copies custom fields (custom_width, custom_length, custom_updated_quantity)
    from the reference document (Sales Order Item, Delivery Note Item, or Sales Invoice Item)
    into the current document's items.
    """
    for item in doc.items:
        reference_item = None

        # Determine the reference item based on the detail type
        if item.so_detail:
            reference_item = frappe.get_doc("Sales Order Item", item.so_detail)
        elif item.dn_detail:
            reference_item = frappe.get_doc("Delivery Note Item", item.dn_detail)
    

        # Copy custom fields if reference item exists
        if reference_item:
            item.custom_width = reference_item.get("custom_width") or 0
            item.custom_length = reference_item.get("custom_length") or 0
            item.custom_updated_quantity = reference_item.get("custom_updated_quantity") or 0
            item.qty = reference_item.get("qty") or 0


def set_qty_in_sales_order(doc, method):
    """
    Calculates and sets the `qty` for each item in a Sales Order
    based on custom fields (custom_updated_quantity, custom_width, custom_length).
    """
    for item in doc.items:
        # Calculate the updated quantity
        updated_qty = (
            (item.custom_updated_quantity or 1) *
            (item.custom_width or 1) *
            (item.custom_length or 1)
        )
        item.qty = updated_qty


def set_qty_in_sales_invoice(doc, method):
    """
    Updates the `qty` for each item in a Sales Invoice, ensuring calculations are
    made only if the item is not linked to a Sales Order or Delivery Note.
    """
    for item in doc.items:
        # Only update qty if no reference to Sales Order or Delivery Note
        if not item.so_detail and not item.dn_detail:
            updated_qty = (
                (item.custom_updated_quantity or 1) *
                (item.custom_width or 1) *
                (item.custom_length or 1)
            )
            item.qty = updated_qty