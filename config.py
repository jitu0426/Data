"""
HEM Product Catalogue - Configuration Module
All paths, constants, and environment variable loading.
"""
import os
import logging

logger = logging.getLogger(__name__)

# --- Base Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Cloudinary Configuration (from environment variables) ---
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "dnoepbfbr")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "393756212248257")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")

# --- Asset Paths ---
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
SAVED_TEMPLATES_FILE = os.path.join(BASE_DIR, "saved_templates.json")
CUSTOM_ITEMS_FILE = os.path.join(BASE_DIR, "custom_products.json")  # Legacy - for migration
PRODUCTS_DB_FILE = os.path.join(BASE_DIR, "data", "products_db.json")
STORY_IMG_1_PATH = os.path.join(BASE_DIR, "image-journey.png")
COVER_IMG_PATH = os.path.join(BASE_DIR, "assets", "cover page.png")
WATERMARK_IMG_PATH = os.path.join(BASE_DIR, "assets", "watermark.png")

# --- Remote URLs ---
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/jitu0426/Hem-Export-Catalogue/main/"
CASE_SIZE_PATH = f"{GITHUB_RAW_BASE}Case%20Size.xlsx"

COVER_IMAGE_URL = "https://res.cloudinary.com/dnoepbfbr/image/upload/v1770703751/Cover_Page.jpg"
JOURNEY_IMAGE_URL = "https://res.cloudinary.com/dnoepbfbr/image/upload/v1770703751/image-journey.jpg"

# --- Catalogue Definitions ---
CATALOGUE_PATHS = {
    "HEM Product Catalogue": os.path.join(BASE_DIR, "Hem catalogue.xlsx"),
    "Sacred Elements Catalogue": os.path.join(BASE_DIR, "SacredElement.xlsx"),
    "Pooja Oil Catalogue": os.path.join(BASE_DIR, "Pooja Oil Catalogue.xlsx"),
    "Candle Catalogue": os.path.join(BASE_DIR, "Candle Catalogue.xlsx"),
}

# --- Column Mapping ---
GLOBAL_COLUMN_MAPPING = {
    "Category": "Category",
    "Sub-Category": "Subcategory",
    "Item Name": "ItemName",
    "ItemName": "ItemName",
    "Description": "Fragrance",
    "SKU Code": "SKU Code",
    "New Product ( Indication )": "IsNew",
}

REQUIRED_OUTPUT_COLS = [
    'Category', 'Subcategory', 'ItemName', 'Fragrance', 'SKU Code',
    'Catalogue', 'Packaging', 'ImageB64', 'ProductID', 'IsNew',
]

CART_COLUMNS = [
    'SKU Code', 'ItemName', 'Category', 'Subcategory', 'Fragrance',
    'Packaging', 'SerialNo', 'ImageB64', 'Catalogue', 'ProductID', 'IsNew',
]

# --- UI Constants ---
NO_SELECTION_PLACEHOLDER = "Select..."
APP_TITLE = "HEM PRODUCT CATALOGUE"
APP_ICON = "\U0001f6cd\ufe0f"
