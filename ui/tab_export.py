"""
HEM Product Catalogue - Tab 3: Export
PDF and Excel generation with case size selection.
"""
import os
import json
import logging

import pandas as pd
import streamlit as st

from config import BASE_DIR, LOGO_PATH, CASE_SIZE_PATH
from cloudinary_client import get_image_as_base64_str
from data_loader import load_data_cached
from pdf_generator import generate_pdf_html, generate_excel_file, render_pdf
from ui.components import section_header

logger = logging.getLogger(__name__)


def render_export_tab(products_df):
    """Render Tab 3: Export Catalogue."""
    section_header("Export Catalogue")

    if not st.session_state.cart:
        st.info("Cart is empty. Add products in Tab 1 first.")
        return

    st.markdown("### 1. Select Case Sizes per Category")

    cart_categories = sorted(list(set(
        [item['Category'] for item in st.session_state.cart]
    )))

    # Load case size data
    full_case_size_df = pd.DataFrame()
    DB_PATH = os.path.join(BASE_DIR, "data", "database.json")
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r') as f:
                db_data = json.load(f)
            if db_data.get("case_sizes"):
                full_case_size_df = pd.DataFrame(db_data["case_sizes"])
        except (json.JSONDecodeError, OSError):
            pass

    if full_case_size_df.empty:
        try:
            full_case_size_df = pd.read_excel(CASE_SIZE_PATH, dtype=str)
            full_case_size_df.columns = [c.strip() for c in full_case_size_df.columns]
        except Exception as e:
            st.error(f"Error loading Case Size data: {e}")

    selection_map = {}
    if not full_case_size_df.empty:
        suffix_col = next(
            (c for c in full_case_size_df.columns if "suffix" in c.lower()),
            None,
        )
        cbm_col = next(
            (c for c in full_case_size_df.columns if "cbm" in c.lower()),
            "CBM",
        )
        if not suffix_col:
            st.error(
                f"Could not find 'Carton Suffix' column. "
                f"Found: {full_case_size_df.columns.tolist()}"
            )
        else:
            for cat in cart_categories:
                options = full_case_size_df[
                    full_case_size_df['Category'] == cat
                ].copy()
                if not options.empty:
                    options['DisplayLabel'] = options.apply(
                        lambda x: f"{x.get(suffix_col, '')} (CBM: {x.get(cbm_col, '')})",
                        axis=1,
                    )
                    label_list = options['DisplayLabel'].tolist()
                    selected_label = st.selectbox(
                        f"Select Case Size for **{cat}**",
                        label_list,
                        key=f"select_case_{cat}",
                    )
                    selected_row = options[
                        options['DisplayLabel'] == selected_label
                    ].iloc[0]
                    selection_map[cat] = selected_row.to_dict()
                else:
                    st.warning(f"No Case Size options found for category: {cat}")

    st.markdown("---")

    # Client name
    name = st.text_input("Client Name", "Valued Client", key="export_client_name")

    # Generate button
    if st.button("Generate Catalogue & Order Sheet", use_container_width=True, type="primary"):
        cart_data = st.session_state.cart
        schema_cols = [
            'Catalogue', 'Category', 'Subcategory', 'ItemName',
            'Fragrance', 'SKU Code', 'ImageB64', 'Packaging', 'IsNew',
        ]
        df_final = pd.DataFrame(cart_data)
        for col in schema_cols:
            if col not in df_final.columns:
                df_final[col] = ''

        # Sort by original Excel order
        products_df_fresh = load_data_cached(st.session_state.data_timestamp)
        pid_to_index = {
            row['ProductID']: i for i, row in products_df_fresh.iterrows()
        }
        if 'ProductID' in df_final.columns:
            df_final['excel_sort_order'] = df_final['ProductID'].map(pid_to_index)
            max_idx = len(products_df_fresh)
            df_final['excel_sort_order'] = df_final['excel_sort_order'].fillna(max_idx)
            df_final = df_final.sort_values('excel_sort_order')
            df_final = df_final.drop(columns=['excel_sort_order'])

        df_final['SerialNo'] = range(1, len(df_final) + 1)

        st.toast("Generating files...", icon="\u23f3")

        # Generate Excel
        st.session_state.gen_excel_bytes = generate_excel_file(
            df_final, name, selection_map
        )

        # Generate PDF
        logo = get_image_as_base64_str(LOGO_PATH, resize=True, max_size=(200, 100))
        html = generate_pdf_html(df_final, name, logo, selection_map)
        pdf_bytes, engine_or_error = render_pdf(html)

        if pdf_bytes:
            st.session_state.gen_pdf_bytes = pdf_bytes
            st.toast(f"PDF generated via {engine_or_error}!", icon="\U0001f389")
        else:
            st.session_state.gen_pdf_bytes = None
            st.error(f"PDF generation failed: {engine_or_error}")

    # Download buttons
    c_pdf, c_excel = st.columns(2)
    with c_pdf:
        if st.session_state.gen_pdf_bytes:
            st.download_button(
                "Download PDF Catalogue",
                st.session_state.gen_pdf_bytes,
                f"{name.replace(' ', '_')}_catalogue.pdf",
                type="primary",
                use_container_width=True,
            )
    with c_excel:
        if st.session_state.gen_excel_bytes:
            st.download_button(
                "Download Excel Order Sheet",
                st.session_state.gen_excel_bytes,
                f"{name.replace(' ', '_')}_order.xlsx",
                type="secondary",
                use_container_width=True,
            )
