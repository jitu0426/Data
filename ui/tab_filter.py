"""
HEM Product Catalogue - Tab 1: Filter Products
Product browsing with search, filters, thumbnails, and select all/deselect all.
"""
import streamlit as st

from config import NO_SELECTION_PLACEHOLDER
from database import load_products_db
from data_loader import create_safe_id
from cart import add_to_cart, add_selected_visible_to_cart, clear_filters_dropdown
from ui.components import product_thumbnail_html, stats_bar


def _display_product_list(df_to_show, is_global_search=False):
    """Render the product list grouped by category with thumbnails and badges."""
    selected_pids = {
        item.get("ProductID") for item in st.session_state.cart if "ProductID" in item
    }
    if df_to_show.empty:
        st.info("No products match filters/search.")
        return

    db = load_products_db()
    overridden_pids = set(db.get("product_overrides", {}).keys())

    grouped_by_category = df_to_show.groupby('Category', sort=False)
    for category, cat_group_df in grouped_by_category:
        cat_count = len(cat_group_df)
        with st.expander(f"{category} ({cat_count})", expanded=is_global_search):
            c1, c2 = st.columns([3, 1])
            with c2:
                if st.button(
                    f"Add All {cat_count}",
                    key=f"btn_add_cat_{create_safe_id(category)}",
                    use_container_width=True,
                ):
                    add_to_cart(cat_group_df)

            for subcategory, subcat_group_df in cat_group_df.groupby('Subcategory', sort=False):
                subcategory_str = str(subcategory).strip()
                if subcategory_str.upper() != 'N/A' and subcategory_str.lower() != 'nan':
                    st.markdown(
                        f"<div class='subcat-header'>{subcategory_str} ({len(subcat_group_df)})</div>",
                        unsafe_allow_html=True,
                    )

                for idx, row in subcat_group_df.iterrows():
                    pid = row['ProductID']
                    unique_key = f"checkbox_{pid}"
                    initial_checked = pid in selected_pids

                    # Build product name with badges
                    badges = ""
                    if row.get('IsNew') == 1:
                        badges += " <span class='badge-new'>NEW</span>"
                    if pid in overridden_pids:
                        badges += " <span class='badge-modified'>EDITED</span>"
                    if str(pid).startswith("CUST_"):
                        badges += " <span class='badge-custom'>CUSTOM</span>"
                    if pid in selected_pids:
                        badges += " <span class='badge-in-cart'>IN CART</span>"

                    # Thumbnail + Name + Checkbox row
                    col_thumb, col_name, col_check = st.columns([0.5, 7, 1])

                    with col_thumb:
                        thumb = product_thumbnail_html(row.get('ImageB64', ''), size=36)
                        st.markdown(thumb, unsafe_allow_html=True)

                    with col_name:
                        st.markdown(
                            f"**{row['ItemName']}**{badges}",
                            unsafe_allow_html=True,
                        )

                    with col_check:
                        st.checkbox(
                            "Select",
                            value=initial_checked,
                            key=unique_key,
                            label_visibility="hidden",
                        )


def render_filter_tab(products_df):
    """Render Tab 1: Filter Products."""
    if products_df.empty:
        st.error("No Data. Please check Excel file paths or run Admin Sync.")
        return

    final_df = products_df.copy()

    def update_search():
        st.session_state.item_search_query = st.session_state["item_search_input"]

    search_term = st.text_input(
        "Global Search (Products, Fragrance, SKU)",
        value=st.session_state.item_search_query,
        key="item_search_input",
        on_change=update_search,
        placeholder="Type to search across all products...",
    ).lower()

    if search_term:
        final_df = products_df[
            products_df['ItemName'].str.lower().str.contains(search_term, na=False) |
            products_df['Fragrance'].str.lower().str.contains(search_term, na=False) |
            products_df['SKU Code'].str.lower().str.contains(search_term, na=False)
        ]
        stats_bar([
            ("Found", f"{len(final_df)} items matching '{search_term}'"),
            ("Cart", f"{len(st.session_state.cart)} items"),
        ])
        _display_product_list(final_df, is_global_search=True)
    else:
        col_filter, col_btns = st.columns([3, 1])

        with col_filter:
            st.markdown("#### Filters")
            catalogue_options = [NO_SELECTION_PLACEHOLDER] + products_df['Catalogue'].unique().tolist()
            try:
                default_index_cat = catalogue_options.index(
                    st.session_state.selected_catalogue_dropdown
                )
            except ValueError:
                default_index_cat = 0

            sel_cat = st.selectbox(
                "Catalogue",
                catalogue_options,
                key="selected_catalogue_dropdown",
                index=default_index_cat,
            )

            if sel_cat != NO_SELECTION_PLACEHOLDER:
                catalog_subset_df = products_df[products_df['Catalogue'] == sel_cat]
                category_options = catalog_subset_df['Category'].unique().tolist()

                valid_defaults_cat = [
                    c for c in st.session_state.selected_categories_multi
                    if c in category_options
                ]
                if valid_defaults_cat != st.session_state.selected_categories_multi:
                    st.session_state.selected_categories_multi = valid_defaults_cat

                sel_cats_multi = st.multiselect(
                    "Category",
                    category_options,
                    default=st.session_state.selected_categories_multi,
                    key="category_multiselect",
                )
                st.session_state.selected_categories_multi = sel_cats_multi

                # Select All / Deselect All buttons
                col_sel_all, col_desel_all = st.columns(2)
                with col_sel_all:
                    if st.button("Select All Categories", key="sel_all_cats", use_container_width=True):
                        st.session_state.selected_categories_multi = category_options
                        st.rerun()
                with col_desel_all:
                    if st.button("Deselect All", key="desel_all_cats", use_container_width=True):
                        st.session_state.selected_categories_multi = []
                        st.rerun()

                if sel_cats_multi:
                    filtered_dfs = []
                    st.markdown("---")
                    st.markdown("**Sub-Category Options:**")
                    for category in sel_cats_multi:
                        cat_data = catalog_subset_df[catalog_subset_df['Category'] == category]
                        raw_subs = cat_data['Subcategory'].unique().tolist()
                        clean_subs = [
                            s for s in raw_subs
                            if str(s).strip().upper() != 'N/A'
                            and str(s).strip().lower() != 'nan'
                            and str(s).strip() != ''
                        ]

                        if clean_subs:
                            safe_cat_key = create_safe_id(category)
                            sel_subs = st.multiselect(
                                f"Select for **{category}**",
                                clean_subs,
                                default=clean_subs,
                                key=f"sub_select_{safe_cat_key}",
                            )
                            cat_data_filtered = cat_data[
                                cat_data['Subcategory'].isin(sel_subs) |
                                cat_data['Subcategory'].isin(['N/A', 'nan', '']) |
                                cat_data['Subcategory'].isna()
                            ]
                            filtered_dfs.append(cat_data_filtered)
                        else:
                            filtered_dfs.append(cat_data)

                    if filtered_dfs:
                        import pandas as pd
                        final_df = pd.concat(filtered_dfs)
                    else:
                        import pandas as pd
                        final_df = pd.DataFrame(columns=products_df.columns)
                else:
                    final_df = catalog_subset_df

        with col_btns:
            st.markdown("#### Actions")
            if st.button("ADD SELECTED", use_container_width=True, type="primary"):
                add_selected_visible_to_cart(final_df)
            if st.button("ADD FILTERED", use_container_width=True, type="secondary"):
                add_to_cart(final_df)
            st.button(
                "Clear Filters",
                use_container_width=True,
                on_click=clear_filters_dropdown,
            )

        st.markdown("---")

        if sel_cat != NO_SELECTION_PLACEHOLDER:
            stats_bar([
                ("Showing", f"{len(final_df)} products"),
                ("Cart", f"{len(st.session_state.cart)} items"),
            ])
            if not final_df.empty:
                _display_product_list(final_df)
            else:
                st.info("Please select one or more **Categories**.")
        else:
            st.info("Please select a **Catalogue** to begin.")
