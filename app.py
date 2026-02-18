"""
HEM Product Catalogue - Main Application Entry Point
=====================================================
This is the top-level file that Streamlit runs.

Usage:
    streamlit run app.py

Structure:
    app.py              ← You are here. Initialises services and renders the layout.
    config.py           ← All paths, constants, and env variables.
    styles.py           ← All CSS injected into the page.
    cloudinary_client.py← Cloudinary SDK wrapper (images, DB backup).
    database.py         ← JSON database: cart, overrides, custom products, templates.
    data_loader.py      ← Loads Excel catalogues and merges with DB overrides.
    cart.py             ← Cart add/remove/clear operations.
    pdf_generator.py    ← PDF (WeasyPrint/pdfkit) and Excel generation.
    ui/
        sidebar.py          ← Sidebar: templates, sync, database info.
        tab_filter.py       ← Tab 1: Filter and browse products.
        tab_review.py       ← Tab 2: Review & edit cart items.
        tab_export.py       ← Tab 3: Generate and download PDF / Excel.
        tab_add_product.py  ← Tab 4: Add custom products.
        components.py       ← Shared reusable UI helpers.
"""
import time      # Used for data_timestamp to bust the data cache
import logging   # Standard library logging

import streamlit as st

# =========================================================================
# Logging Setup
# Configure before any other imports so all modules use the same format
# =========================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# =========================================================================
# Module Imports
# =========================================================================
from config import NO_SELECTION_PLACEHOLDER, APP_TITLE, APP_ICON  # UI constants
from styles import APP_CSS                                          # All CSS styles
from cloudinary_client import init_cloudinary                       # Cloudinary SDK init
from database import load_cart_from_db, migrate_old_custom_items   # DB helpers
from data_loader import load_data_cached                            # Excel loader

# =========================================================================
# Page Configuration
# MUST be the very first Streamlit command called - before any other st.*
# =========================================================================
st.set_page_config(
    page_title=APP_TITLE,   # Browser tab title
    page_icon=APP_ICON,     # Browser tab emoji/icon
    layout="wide",          # Use full browser width
)

# =========================================================================
# Initialize Services
# Connect to Cloudinary using credentials from environment variables
# =========================================================================
init_cloudinary()

# =========================================================================
# Inject CSS
# Injects APP_CSS (from styles.py) into every page render
# =========================================================================
st.markdown(APP_CSS, unsafe_allow_html=True)

# =========================================================================
# Session State Initialization
# Streamlit re-runs this script on every user interaction, so we use
# session_state to preserve values across reruns within one browser session.
# =========================================================================
if "cart" not in st.session_state:
    # Load the last saved cart from the JSON database on first run
    st.session_state.cart = load_cart_from_db()

if "gen_pdf_bytes" not in st.session_state:
    # Stores generated PDF bytes so the download button works after generation
    st.session_state.gen_pdf_bytes = None

if "gen_excel_bytes" not in st.session_state:
    # Stores generated Excel bytes for the download button
    st.session_state.gen_excel_bytes = None

if 'selected_catalogue_dropdown' not in st.session_state:
    # Tracks the currently selected catalogue in Tab 1 filter dropdown
    st.session_state.selected_catalogue_dropdown = NO_SELECTION_PLACEHOLDER

if 'selected_categories_multi' not in st.session_state:
    # Tracks which categories are selected in the multi-select filter
    st.session_state.selected_categories_multi = []

if 'selected_subcategories_multi' not in st.session_state:
    # Tracks which subcategories are selected
    st.session_state.selected_subcategories_multi = []

if 'item_search_query' not in st.session_state:
    # Global search box value persisted across reruns
    st.session_state.item_search_query = ""

if 'master_pid_map' not in st.session_state:
    # dict: ProductID → full product row dict, used for fast lookups when adding to cart
    st.session_state['master_pid_map'] = {}

if 'data_timestamp' not in st.session_state:
    # Timestamp used as a cache key - updating it forces data to reload from disk
    st.session_state.data_timestamp = time.time()

# =========================================================================
# One-time Migration
# Converts legacy custom_products.json file into the new unified DB format
# Only runs once per installation (no-op if already migrated)
# =========================================================================
migrate_old_custom_items()

# =========================================================================
# Load Data
# Reads all Excel catalogues + merges with DB overrides (cached by timestamp)
# =========================================================================
products_df = load_data_cached(st.session_state.data_timestamp)

# Build the master ProductID → row dict map for fast cart lookups
st.session_state['master_pid_map'] = {
    row['ProductID']: row.to_dict() for _, row in products_df.iterrows()
}

# =========================================================================
# Sidebar
# Renders template management, data sync button, and database info
# =========================================================================
from ui.sidebar import render_sidebar
render_sidebar()

# =========================================================================
# Main Title Banner
# =========================================================================
st.markdown(
    f'<div class="main-title">{APP_TITLE}</div>',
    unsafe_allow_html=True,
)

# =========================================================================
# Tab Navigation
# Shows number of items in cart on Tab 2's label
# =========================================================================
cart_count = len(st.session_state.cart)
cart_label = (
    f"2. Review & Edit ({cart_count})"  # e.g. "2. Review & Edit (12)"
    if cart_count > 0
    else "2. Review & Edit"
)

# Create four main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Filter Products",  # Browse and select products
    cart_label,            # Review cart + edit product names
    "3. Export",           # Generate PDF catalogue + Excel order sheet
    "4. Add Product",      # Add custom products not in the Excel files
])

# =========================================================================
# Tab Rendering
# Import each tab's render function and call it inside the correct tab context
# =========================================================================
from ui.tab_filter import render_filter_tab
from ui.tab_review import render_review_tab
from ui.tab_export import render_export_tab
from ui.tab_add_product import render_add_product_tab

with tab1:
    render_filter_tab(products_df)   # Pass full product data to filter tab

with tab2:
    render_review_tab()              # Cart is read from st.session_state.cart

with tab3:
    render_export_tab(products_df)   # Needs products_df for sorting export order

with tab4:
    render_add_product_tab(products_df)  # Needs products_df to check for duplicates
