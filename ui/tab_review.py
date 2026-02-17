"""
HEM Product Catalogue - Tab 2: Review & Edit Cart
Cart management with inline editing, change detection, and confirmation dialogs.
"""
import time
import pandas as pd
import streamlit as st

from database import (
    load_products_db, save_product_override, save_cart_to_db,
)
from cart import remove_from_cart, clear_cart
from ui.components import section_header, stats_bar, confirm_action


def render_review_tab():
    """Render Tab 2: Review & Edit."""
    section_header("Review & Edit Cart Items")

    if not st.session_state.cart:
        st.info("Cart is empty. Go to **Tab 1** to add products.")
        return

    cart_df = pd.DataFrame(st.session_state.cart)

    # Search within cart
    cart_search = st.text_input(
        "Find in Cart...",
        placeholder="Type product name...",
        key="cart_search_input",
    ).lower()
    if cart_search:
        cart_df = cart_df[cart_df['ItemName'].str.lower().str.contains(cart_search, na=False)]

    # Load DB for override indicators
    db = load_products_db()
    overridden_pids = set(db.get("product_overrides", {}).keys())

    # Status column
    def get_status(pid):
        parts = []
        if pid in overridden_pids:
            parts.append("Edited")
        if str(pid).startswith("CUST_"):
            parts.append("Custom")
        return ", ".join(parts) if parts else ""

    cart_df['Status'] = cart_df['ProductID'].apply(get_status)
    cart_df['Remove'] = False

    editable_display_cols = [
        'Catalogue', 'Category', 'Subcategory', 'ItemName',
        'Fragrance', 'SKU Code', 'Status', 'Remove',
    ]
    for col in editable_display_cols:
        if col not in cart_df.columns:
            cart_df[col] = ''

    # Stats bar
    stats_bar([
        ("Total Items", str(len(cart_df))),
        ("Edited", str(len([p for p in cart_df['ProductID'] if p in overridden_pids]))),
        ("Custom", str(len([p for p in cart_df['ProductID'] if str(p).startswith('CUST_')]))),
    ])

    # Data editor
    edited_df = st.data_editor(
        cart_df[editable_display_cols],
        column_config={
            "Remove": st.column_config.CheckboxColumn("Remove?", default=False, width="small"),
            "Catalogue": st.column_config.TextColumn("Catalogue", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Subcategory": st.column_config.TextColumn("Sub-Category", width="medium"),
            "ItemName": st.column_config.TextColumn("Product Name", width="large"),
            "Fragrance": st.column_config.TextColumn("Fragrance", width="medium"),
            "SKU Code": st.column_config.TextColumn("SKU Code", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small", disabled=True),
        },
        hide_index=True,
        key="cart_data_editor_v2",
        use_container_width=True,
        num_rows="fixed",
    )

    # --- Detect Changes ---
    editable_fields = ['Catalogue', 'Category', 'Subcategory', 'ItemName', 'Fragrance', 'SKU Code']
    changes_detected = {}

    for idx in range(min(len(cart_df), len(edited_df))):
        pid = cart_df.iloc[idx]['ProductID']
        field_changes = {}
        for field in editable_fields:
            original_val = str(cart_df.iloc[idx].get(field, '')).strip()
            edited_val = str(edited_df.iloc[idx].get(field, '')).strip()
            if original_val != edited_val:
                field_changes[field] = edited_val
        if field_changes:
            changes_detected[pid] = field_changes

    # --- Action Buttons ---
    col_save, col_remove, col_clear = st.columns([1, 1, 1])

    with col_save:
        save_disabled = len(changes_detected) == 0
        btn_label = (
            f"Save {len(changes_detected)} Edit(s)"
            if changes_detected
            else "No Changes"
        )
        if st.button(
            btn_label,
            disabled=save_disabled,
            use_container_width=True,
            type="primary",
        ):
            for pid, field_changes in changes_detected.items():
                save_product_override(pid, field_changes)
                for item in st.session_state.cart:
                    if item.get("ProductID") == pid:
                        item.update(field_changes)
            save_cart_to_db(st.session_state.cart)
            st.session_state.data_timestamp = time.time()
            st.cache_data.clear()
            st.toast(f"Saved {len(changes_detected)} product edit(s)!", icon="\u2705")
            st.rerun()

    with col_remove:
        indices_to_remove = edited_df[edited_df['Remove'] == True].index.tolist()
        pids_to_remove = (
            cart_df.loc[indices_to_remove, 'ProductID'].tolist()
            if indices_to_remove else []
        )
        if st.button(
            f"Remove {len(pids_to_remove)} Selected",
            disabled=not pids_to_remove,
            use_container_width=True,
        ):
            remove_from_cart(pids_to_remove)
            st.rerun()

    with col_clear:
        if confirm_action(
            "clear_cart",
            "Clear Cart",
            "Are you sure you want to remove ALL items from the cart? This cannot be undone.",
            danger=True,
        ):
            clear_cart()
            st.rerun()

    # --- Change Preview ---
    if changes_detected:
        with st.expander(f"Preview {len(changes_detected)} Pending Edit(s)", expanded=True):
            for pid, changes in changes_detected.items():
                orig_row = cart_df[cart_df['ProductID'] == pid]
                orig_name = orig_row.iloc[0]['ItemName'] if not orig_row.empty else pid
                change_text = ", ".join(
                    [f"**{k}**: '{v}'" for k, v in changes.items()]
                )
                st.markdown(f"- **{orig_name}** \u2192 {change_text}")
            st.info("Click **Save Edit(s)** above to persist these changes permanently.")
