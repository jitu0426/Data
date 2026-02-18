"""
HEM Product Catalogue - Tab 1: Filter Products
===============================================
This tab is the main product browsing interface.

Features:
  - Global search across ItemName, Fragrance, and SKU Code
  - Catalogue → Category → Subcategory drill-down filters
  - Checkbox-based individual product selection (ADD SELECTED)
  - Bulk add all visible products (ADD FILTERED)
  - Inline thumbnail previews next to each product name
  - Badges: NEW, EDITED, CUSTOM, IN CART
"""
import streamlit as st

from config import NO_SELECTION_PLACEHOLDER
from database import load_products_db
from data_loader import create_safe_id
from cart import add_to_cart, add_selected_visible_to_cart, clear_filters_dropdown
from ui.components import product_thumbnail_html, stats_bar


def _display_product_list(df_to_show, is_global_search=False):
    """
    Render the product list grouped by Category, with subcategory headers,
    thumbnails, badges, and per-product checkboxes.

    Args:
        df_to_show (pd.DataFrame): Filtered/searched product rows to display.
        is_global_search (bool): If True, expand all category sections by default
                                  (useful when search returns scattered results).
    """
    # Build a set of ProductIDs already in the cart for fast badge lookup
    selected_pids = {
        item.get("ProductID") for item in st.session_state.cart if "ProductID" in item
    }

    # Nothing to show - give the user a helpful message
    if df_to_show.empty:
        st.info("No products match filters/search.")
        return

    # Load DB to check which products have been manually overridden
    db = load_products_db()
    overridden_pids = set(db.get("product_overrides", {}).keys())

    # Group by Category so we can render one expander section per category
    grouped_by_category = df_to_show.groupby('Category', sort=False)
    for category, cat_group_df in grouped_by_category:
        cat_count = len(cat_group_df)

        # Each category is shown in a collapsible expander
        with st.expander(f"{category} ({cat_count})", expanded=is_global_search):

            # "Add All" button to bulk-add every product in this category
            c1, c2 = st.columns([3, 1])
            with c2:
                if st.button(
                    f"Add All {cat_count}",
                    key=f"btn_add_cat_{create_safe_id(category)}",
                    use_container_width=True,
                ):
                    add_to_cart(cat_group_df)

            # Iterate subcategories within the category
            for subcategory, subcat_group_df in cat_group_df.groupby('Subcategory', sort=False):
                subcategory_str = str(subcategory).strip()

                # Only show subcategory header if it's a real label (not N/A or empty)
                if subcategory_str.upper() != 'N/A' and subcategory_str.lower() != 'nan':
                    st.markdown(
                        f"<div class='subcat-header'>{subcategory_str} ({len(subcat_group_df)})</div>",
                        unsafe_allow_html=True,
                    )

                # Render each individual product row
                for idx, row in subcat_group_df.iterrows():
                    pid = row['ProductID']
                    unique_key = f"checkbox_{pid}"                   # Unique key per product for session state
                    initial_checked = pid in selected_pids           # Pre-check if already in cart

                    # ---- Build badge HTML ----
                    badges = ""
                    if row.get('IsNew') == 1:
                        badges += " <span class='badge-new'>NEW</span>"          # Red NEW badge
                    if pid in overridden_pids:
                        badges += " <span class='badge-modified'>EDITED</span>"  # Yellow EDITED badge
                    if str(pid).startswith("CUST_"):
                        badges += " <span class='badge-custom'>CUSTOM</span>"    # Green CUSTOM badge
                    if pid in selected_pids:
                        badges += " <span class='badge-in-cart'>IN CART</span>"  # Blue IN CART badge

                    # ---- 3-column row: thumbnail | name+badges | checkbox ----
                    col_thumb, col_name, col_check = st.columns([0.5, 7, 1])

                    with col_thumb:
                        # Small 36px thumbnail from base64 image data
                        thumb = product_thumbnail_html(row.get('ImageB64', ''), size=36)
                        st.markdown(thumb, unsafe_allow_html=True)

                    with col_name:
                        # Product name in bold with any applicable status badges
                        st.markdown(
                            f"**{row['ItemName']}**{badges}",
                            unsafe_allow_html=True,
                        )

                    with col_check:
                        # Checkbox - label is hidden visually but required by Streamlit
                        st.checkbox(
                            "Select",
                            value=initial_checked,
                            key=unique_key,
                            label_visibility="hidden",
                        )


def render_filter_tab(products_df):
    """
    Render Tab 1: Filter Products.

    Layout:
      - Global search bar at the top (searches across all catalogues)
      - If search is active: show matching products immediately
      - Otherwise: Catalogue → Category → Subcategory filters
                  + Action buttons (ADD SELECTED, ADD FILTERED, Clear Filters)
                  + Product list grouped by category

    Args:
        products_df (pd.DataFrame): Full products DataFrame loaded from Excel + DB.
    """
    # Guard: if data didn't load, show error
    if products_df.empty:
        st.error("No Data. Please check Excel file paths or run Admin Sync.")
        return

    # Start with the full dataset; filtering narrows it down
    final_df = products_df.copy()

    # ------------------------------------------------------------------
    # Global Search Bar
    # Searches across ItemName, Fragrance, and SKU Code simultaneously
    # ------------------------------------------------------------------
    def update_search():
        """Sync the text input widget value into session state."""
        st.session_state.item_search_query = st.session_state["item_search_input"]

    search_term = st.text_input(
        "Global Search (Products, Fragrance, SKU)",
        value=st.session_state.item_search_query,
        key="item_search_input",
        on_change=update_search,
        placeholder="Type to search across all products...",
    ).lower()   # Convert to lowercase for case-insensitive matching

    # ------------------------------------------------------------------
    # SEARCH MODE: show results directly, skip category filters
    # ------------------------------------------------------------------
    if search_term:
        # Filter across all three text columns
        final_df = products_df[
            products_df['ItemName'].str.lower().str.contains(search_term, na=False) |
            products_df['Fragrance'].str.lower().str.contains(search_term, na=False) |
            products_df['SKU Code'].str.lower().str.contains(search_term, na=False)
        ]
        # Show a stats bar with the match count
        stats_bar([
            ("Found", f"{len(final_df)} items matching '{search_term}'"),
            ("Cart", f"{len(st.session_state.cart)} items"),
        ])
        # Render results with all categories expanded (is_global_search=True)
        _display_product_list(final_df, is_global_search=True)

    else:
        # ------------------------------------------------------------------
        # FILTER MODE: Catalogue → Category → Subcategory drilldown
        # ------------------------------------------------------------------
        col_filter, col_btns = st.columns([3, 1])

        with col_filter:
            st.markdown("#### Filters")

            # ---- Catalogue Dropdown ----
            # First level: pick one catalogue (or keep "Select..." placeholder)
            catalogue_options = [NO_SELECTION_PLACEHOLDER] + products_df['Catalogue'].unique().tolist()
            try:
                # Preserve the previously selected catalogue across reruns
                default_index_cat = catalogue_options.index(
                    st.session_state.selected_catalogue_dropdown
                )
            except ValueError:
                default_index_cat = 0  # Fall back to placeholder if state is stale

            sel_cat = st.selectbox(
                "Catalogue",
                catalogue_options,
                key="selected_catalogue_dropdown",
                index=default_index_cat,
            )

            # ---- Category Multi-Select (only if a catalogue is chosen) ----
            if sel_cat != NO_SELECTION_PLACEHOLDER:
                # Narrow the product set to the selected catalogue
                catalog_subset_df = products_df[products_df['Catalogue'] == sel_cat]
                category_options = catalog_subset_df['Category'].unique().tolist()

                # Clean up session state if previously selected categories no longer exist
                valid_defaults_cat = [
                    c for c in st.session_state.selected_categories_multi
                    if c in category_options
                ]
                if valid_defaults_cat != st.session_state.selected_categories_multi:
                    st.session_state.selected_categories_multi = valid_defaults_cat

                # Multi-select for one or more categories within the catalogue
                sel_cats_multi = st.multiselect(
                    "Category",
                    category_options,
                    default=st.session_state.selected_categories_multi,
                    key="category_multiselect",
                )
                # Keep session state in sync with widget value
                st.session_state.selected_categories_multi = sel_cats_multi

                # ---- Subcategory filters per selected Category ----
                if sel_cats_multi:
                    filtered_dfs = []
                    st.markdown("---")
                    st.markdown("**Sub-Category Options:**")

                    for category in sel_cats_multi:
                        # Get all products in this category
                        cat_data = catalog_subset_df[catalog_subset_df['Category'] == category]
                        raw_subs = cat_data['Subcategory'].unique().tolist()

                        # Filter out empty / placeholder subcategory values
                        clean_subs = [
                            s for s in raw_subs
                            if str(s).strip().upper() != 'N/A'
                            and str(s).strip().lower() != 'nan'
                            and str(s).strip() != ''
                        ]

                        if clean_subs:
                            # Show subcategory picker for this category, defaulting to all selected
                            safe_cat_key = create_safe_id(category)
                            sel_subs = st.multiselect(
                                f"Select for **{category}**",
                                clean_subs,
                                default=clean_subs,           # Start with all selected
                                key=f"sub_select_{safe_cat_key}",
                            )
                            # Filter products: show selected subcategories PLUS items with no subcategory
                            cat_data_filtered = cat_data[
                                cat_data['Subcategory'].isin(sel_subs) |
                                cat_data['Subcategory'].isin(['N/A', 'nan', '']) |
                                cat_data['Subcategory'].isna()
                            ]
                            filtered_dfs.append(cat_data_filtered)
                        else:
                            # No subcategories for this category - include all products
                            filtered_dfs.append(cat_data)

                    # Combine filtered results from all selected categories
                    if filtered_dfs:
                        import pandas as pd
                        final_df = pd.concat(filtered_dfs)
                    else:
                        import pandas as pd
                        final_df = pd.DataFrame(columns=products_df.columns)
                else:
                    # No categories selected yet - show full catalogue
                    final_df = catalog_subset_df

        # ---- Action Buttons column ----
        with col_btns:
            st.markdown("#### Actions")

            # ADD SELECTED: adds only the checkbox-ticked products currently visible
            if st.button("ADD SELECTED", use_container_width=True, type="primary"):
                add_selected_visible_to_cart(final_df)

            # ADD FILTERED: adds every product currently visible (regardless of checkboxes)
            if st.button("ADD FILTERED", use_container_width=True, type="secondary"):
                add_to_cart(final_df)

            # CLEAR FILTERS: resets all dropdowns and search back to defaults
            st.button(
                "Clear Filters",
                use_container_width=True,
                on_click=clear_filters_dropdown,   # Callback runs before the next rerun
            )

        st.markdown("---")

        # ---- Show stats + product list when a catalogue is selected ----
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
            # Prompt the user to start by picking a catalogue
            st.info("Please select a **Catalogue** to begin.")
