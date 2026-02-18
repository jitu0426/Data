"""
HEM Product Catalogue - Sidebar Module
Template management, sync controls, and database info.
"""
import time
import streamlit as st

from database import (
    load_products_db, load_cart_from_db, save_cart_to_db,
    load_saved_templates, save_template_to_disk, delete_template,
)


def render_sidebar():
    """Render the sidebar with templates, sync, and DB info."""
    with st.sidebar:
        st.header("Manage Templates")

        # --- Save Template ---
        with st.expander("Save Current Cart"):
            new_template_name = st.text_input("Template Name", key="sidebar_template_name")
            if st.button("Save Template", use_container_width=True, key="sidebar_save_template"):
                if new_template_name:
                    save_template_to_disk(new_template_name, st.session_state.cart)
                else:
                    st.warning("Please enter a template name.")

        # --- Load Template ---
        saved_templates = load_saved_templates()
        if saved_templates:
            with st.expander("Load Template"):
                sel_temp = st.selectbox(
                    "Select Template",
                    list(saved_templates.keys()),
                    key="sidebar_load_select",
                )
                col_load, col_del_temp = st.columns(2)
                with col_load:
                    if st.button("Load", use_container_width=True, key="sidebar_load_btn"):
                        st.session_state.cart = saved_templates[sel_temp]
                        save_cart_to_db(st.session_state.cart)
                        st.toast(f"Template '{sel_temp}' loaded!", icon="\u2705")
                        st.rerun()
                with col_del_temp:
                    if st.button("Delete", use_container_width=True, key="sidebar_del_template"):
                        delete_template(sel_temp)
                        st.rerun()

        # --- Debug Logs ---
        with st.expander("Image Sync Debugger", expanded=False):
            if 'debug_logs' in st.session_state:
                for line in st.session_state['debug_logs']:
                    st.text(line)

        st.markdown("---")

        # --- Data Sync ---
        st.markdown("### Data Sync")
        if st.button(
            "Refresh Cloudinary & Excel",
            help="Click if you uploaded new images or changed the Excel file.",
            use_container_width=True,
            key="sidebar_refresh",
        ):
            st.session_state.data_timestamp = time.time()
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")

        # --- Database Info ---
        st.markdown("### Database Info")
        db_info = load_products_db()
        st.caption(f"Overrides: {len(db_info.get('product_overrides', {}))}")
        st.caption(f"Custom Products: {len(db_info.get('custom_products', []))}")
        st.caption(f"Hidden Products: {len(db_info.get('deleted_products', []))}")
        st.caption(f"Cart Items: {len(db_info.get('saved_cart', []))}")
        if db_info.get('last_updated'):
            st.caption(f"Last Updated: {db_info['last_updated'][:19]}")
