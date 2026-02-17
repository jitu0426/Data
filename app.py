"""
HEM Product Catalogue - Main Application Entry Point
Professional product catalogue management system.

Run with: streamlit run app.py
"""
import time
import logging

import streamlit as st

# =========================================================================
# Logging Setup (before any other imports)
# =========================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# =========================================================================
# Module Imports
# =========================================================================
from config import NO_SELECTION_PLACEHOLDER, APP_TITLE, APP_ICON
from styles import APP_CSS
from cloudinary_client import init_cloudinary
from database import load_cart_from_db, migrate_old_custom_items
from data_loader import load_data_cached

# =========================================================================
# Page Configuration (must be the first Streamlit command)
# =========================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

# =========================================================================
# Initialize Services
# =========================================================================
init_cloudinary()

# =========================================================================
# Inject CSS
# =========================================================================
st.markdown(APP_CSS, unsafe_allow_html=True)

# =========================================================================
# Session State Initialization
# =========================================================================
if "cart" not in st.session_state:
    st.session_state.cart = load_cart_from_db()
if "gen_pdf_bytes" not in st.session_state:
    st.session_state.gen_pdf_bytes = None
if "gen_excel_bytes" not in st.session_state:
    st.session_state.gen_excel_bytes = None
if 'selected_catalogue_dropdown' not in st.session_state:
    st.session_state.selected_catalogue_dropdown = NO_SELECTION_PLACEHOLDER
if 'selected_categories_multi' not in st.session_state:
    st.session_state.selected_categories_multi = []
if 'selected_subcategories_multi' not in st.session_state:
    st.session_state.selected_subcategories_multi = []
if 'item_search_query' not in st.session_state:
    st.session_state.item_search_query = ""
if 'master_pid_map' not in st.session_state:
    st.session_state['master_pid_map'] = {}
if 'data_timestamp' not in st.session_state:
    st.session_state.data_timestamp = time.time()

# =========================================================================
# One-time Migration (legacy custom_products.json -> new DB)
# =========================================================================
migrate_old_custom_items()

# =========================================================================
# Load Data
# =========================================================================
products_df = load_data_cached(st.session_state.data_timestamp)
st.session_state['master_pid_map'] = {
    row['ProductID']: row.to_dict() for _, row in products_df.iterrows()
}

# =========================================================================
# Sidebar
# =========================================================================
from ui.sidebar import render_sidebar
render_sidebar()

# =========================================================================
# Header
# =========================================================================
st.markdown(
    f'<div class="main-title">{APP_TITLE}</div>',
    unsafe_allow_html=True,
)

# =========================================================================
# Tabs
# =========================================================================
cart_count = len(st.session_state.cart)
cart_label = (
    f"2. Review & Edit ({cart_count})" if cart_count > 0
    else "2. Review & Edit"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Filter Products",
    cart_label,
    "3. Export",
    "4. Add Product",
])

# --- Tab Rendering ---
from ui.tab_filter import render_filter_tab
from ui.tab_review import render_review_tab
from ui.tab_export import render_export_tab
from ui.tab_add_product import render_add_product_tab

with tab1:
    render_filter_tab(products_df)

with tab2:
    render_review_tab()

with tab3:
    render_export_tab(products_df)

with tab4:
    render_add_product_tab(products_df)
