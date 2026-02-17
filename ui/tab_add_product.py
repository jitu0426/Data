"""
HEM Product Catalogue - Tab 4: Add Product
Custom product creation, management, and override/hidden product admin.
"""
import time
import streamlit as st

from config import CATALOGUE_PATHS
from database import (
    load_products_db, add_custom_item, delete_custom_item,
    get_custom_products_from_db, remove_product_override,
    unmark_product_deleted,
)
from ui.components import section_header, confirm_action


def render_add_product_tab(products_df):
    """Render Tab 4: Add Product + Admin panels."""
    section_header("Add New Product")
    st.markdown(
        "Add a custom product to any catalogue. "
        "It will be tagged as **NEW** and included in the product list."
    )

    with st.form("add_product_form", clear_on_submit=True):
        st.markdown("### Product Details")
        col_a, col_b = st.columns(2)

        with col_a:
            existing_catalogues = list(CATALOGUE_PATHS.keys()) + ["Custom Items"]
            new_catalogue = st.selectbox(
                "Catalogue *", existing_catalogues,
                help="Select which catalogue this product belongs to.",
            )
            if not products_df.empty:
                existing_cats = (
                    products_df[products_df['Catalogue'] == new_catalogue]['Category']
                    .unique().tolist()
                )
            else:
                existing_cats = []

            cat_input_mode = st.radio(
                "Category Input",
                ["Select Existing", "Type New"],
                horizontal=True,
            )
            if cat_input_mode == "Select Existing" and existing_cats:
                new_category = st.selectbox("Category *", existing_cats)
            else:
                new_category = st.text_input(
                    "Category Name *",
                    placeholder="e.g. Hexa Incense Sticks",
                )
            new_subcategory = st.text_input(
                "Sub-Category",
                placeholder="e.g. Premium Range (leave blank for N/A)",
            )

        with col_b:
            new_item_name = st.text_input(
                "Item Name *", placeholder="e.g. Lavender Hexa",
            )
            new_fragrance = st.text_input(
                "Fragrance / Description", placeholder="e.g. Lavender",
            )
            new_sku = st.text_input(
                "SKU Code", placeholder="e.g. HEM-LAV-HEX-001",
            )
            new_is_new = st.checkbox("Mark as NEW product", value=True)

        st.markdown("### Product Image")
        new_image = st.file_uploader(
            "Upload product image (optional)",
            type=["jpg", "jpeg", "png", "webp"],
            help="Image will be uploaded to Cloudinary automatically.",
        )
        if new_image:
            st.image(new_image, caption="Preview", width=200)

        submitted = st.form_submit_button(
            "Add Product", use_container_width=True, type="primary",
        )
        if submitted:
            errors = []
            if not new_catalogue:
                errors.append("Catalogue is required.")
            if not new_category:
                errors.append("Category is required.")
            if not new_item_name:
                errors.append("Item Name is required.")
            if errors:
                for err in errors:
                    st.error(err)
            else:
                # Duplicate detection
                if not products_df.empty:
                    duplicate_mask = (
                        (products_df['ItemName'].str.lower() == new_item_name.lower()) &
                        (products_df['Category'].str.lower() == new_category.lower()) &
                        (products_df['Catalogue'] == new_catalogue)
                    )
                    if duplicate_mask.any():
                        st.warning(
                            f"A product named '{new_item_name}' already exists "
                            f"in {new_catalogue} > {new_category}. "
                            f"It will be added as a separate custom product."
                        )

                with st.spinner("Adding product..."):
                    added = add_custom_item(
                        catalogue=new_catalogue, category=new_category,
                        subcategory=new_subcategory, item_name=new_item_name,
                        fragrance=new_fragrance, sku_code=new_sku,
                        is_new=new_is_new, image_file=new_image,
                    )
                st.success(
                    f"Product '{new_item_name}' added successfully! "
                    f"(ID: {added['ProductID']})"
                )
                st.info(
                    "Click **Refresh Cloudinary & Excel** in the sidebar "
                    "to see it in the product list."
                )

    # =========================================================================
    # MANAGE CUSTOM PRODUCTS
    # =========================================================================
    st.markdown("---")
    section_header("Manage Custom Products")

    custom_items = get_custom_products_from_db()
    if custom_items:
        st.markdown(f"**{len(custom_items)} custom product(s) added.**")
        for i, item in enumerate(custom_items):
            col_info, col_del = st.columns([5, 1])
            with col_info:
                new_tag = (
                    " <span class='badge-new'>NEW</span>"
                    if item.get('IsNew', 0) == 1 else ""
                )
                st.markdown(
                    f"**{i+1}.** {item['ItemName']}{new_tag} | "
                    f"{item['Catalogue']} > {item['Category']}",
                    unsafe_allow_html=True,
                )
            with col_del:
                if confirm_action(
                    f"del_custom_{item['ProductID']}",
                    "Delete",
                    f"Delete '{item['ItemName']}'?",
                    danger=True,
                ):
                    delete_custom_item(item['ProductID'])
                    st.session_state.data_timestamp = time.time()
                    st.cache_data.clear()
                    st.toast(f"Deleted '{item['ItemName']}'", icon="\U0001f5d1\ufe0f")
                    st.rerun()
    else:
        st.info("No custom products added yet.")

    # =========================================================================
    # MANAGE PRODUCT OVERRIDES
    # =========================================================================
    st.markdown("---")
    section_header("Manage Product Edits")

    db_for_overrides = load_products_db()
    overrides = db_for_overrides.get("product_overrides", {})
    if overrides:
        st.markdown(f"**{len(overrides)} product(s) have been edited.**")
        for pid, changes in overrides.items():
            change_text = ", ".join([f"{k}: '{v}'" for k, v in changes.items()])
            col_ov_info, col_ov_reset = st.columns([5, 1])
            with col_ov_info:
                st.markdown(f"**{pid}** \u2192 {change_text}")
            with col_ov_reset:
                if st.button("Reset", key=f"reset_override_{pid}", use_container_width=True):
                    remove_product_override(pid)
                    st.session_state.data_timestamp = time.time()
                    st.cache_data.clear()
                    st.toast(f"Reset edits for {pid}", icon="\u21a9\ufe0f")
                    st.rerun()
    else:
        st.info("No product edits have been made.")

    # =========================================================================
    # MANAGE HIDDEN PRODUCTS
    # =========================================================================
    st.markdown("---")
    section_header("Hidden Products")

    deleted_pids = db_for_overrides.get("deleted_products", [])
    if deleted_pids:
        st.markdown(f"**{len(deleted_pids)} product(s) hidden.**")
        for pid in deleted_pids:
            col_del_info, col_del_restore = st.columns([5, 1])
            with col_del_info:
                st.markdown(f"Hidden: **{pid}**")
            with col_del_restore:
                if st.button("Restore", key=f"restore_{pid}", use_container_width=True):
                    unmark_product_deleted(pid)
                    st.session_state.data_timestamp = time.time()
                    st.cache_data.clear()
                    st.toast(f"Restored {pid}", icon="\u2705")
                    st.rerun()
    else:
        st.info("No products have been hidden.")
