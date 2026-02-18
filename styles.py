"""
HEM Product Catalogue - Professional CSS Styles
================================================
All application styling lives here as a single injected <style> block.
Imported in app.py and injected via st.markdown(APP_CSS, unsafe_allow_html=True).
"""

APP_CSS = """
<style>
/* ============================================================
   HEM PRODUCT CATALOGUE - PROFESSIONAL UI THEME
   ============================================================ */

/* ===== CSS VARIABLES (design tokens) ===== */
:root {
    --primary-dark:       #1a1a2e;   /* Deep navy - main brand dark */
    --primary-mid:        #16213e;   /* Mid navy */
    --primary-light:      #2d2d5e;   /* Lighter navy for gradients */
    --accent-orange:      #ff9800;   /* HEM signature orange */
    --accent-orange-dark: #f57c00;
    --accent-blue:        #007bff;   /* Action / link blue */
    --accent-blue-dark:   #0056b3;
    --bg-white:           #ffffff;
    --bg-light:           #f8f9fa;
    --bg-lighter:         #f0f2f6;
    --text-primary:       #000000;
    --text-secondary:     #555;
    --text-muted:         #999;
    --border-light:       #dee2e6;
    --border-lighter:     #e0e0e0;
    --shadow-sm:          0 2px 8px rgba(0,0,0,0.06);
    --shadow-md:          0 4px 12px rgba(0,0,0,0.10);
    --shadow-lg:          0 8px 24px rgba(0,0,0,0.15);
    --radius-sm:          6px;
    --radius-md:          10px;
    --radius-lg:          14px;
    --transition-fast:    0.15s ease;
    --transition-normal:  0.25s ease;
}

/* ===== GOOGLE FONT IMPORT ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ===== GLOBAL APP STYLES ===== */
/* Set a clean white background and use Inter for all text */
.stApp {
    background-color: var(--bg-white) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== MAIN HEADER / TITLE ===== */
/* Large gradient banner shown at the top of every page */
.main-title {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 50%, #16213e 100%);
    color: white !important;
    padding: 28px 36px;
    border-radius: var(--radius-lg);
    margin-bottom: 28px;
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 4px solid var(--accent-orange);
    box-shadow: var(--shadow-lg), 0 0 40px rgba(255,152,0,0.12);
    position: relative;
    overflow: hidden;
}
/* Animated shimmer sweep across the title banner */
.main-title::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 200%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    animation: shimmer 3s infinite;
}
/* Subtle decorative bottom glow line */
.main-title::after {
    content: '';
    position: absolute;
    bottom: 0; left: 15%; right: 15%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-orange), transparent);
    border-radius: 2px;
}
@keyframes shimmer {
    0%   { left: -100%; }
    100% { left: 100%; }
}

/* ===== TAB NAVIGATION ===== */
/* Tab bar container */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: var(--bg-lighter);
    padding: 6px 8px;
    border-radius: var(--radius-md);
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.08);
    border: 1px solid #e8eaed;
}
/* Individual tab pill */
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
    color: var(--text-secondary);
    background-color: transparent;
    border: none;
    transition: all var(--transition-fast);
    letter-spacing: 0.2px;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(26,26,46,0.08);
    color: var(--primary-dark);
}
/* Active / selected tab gets dark navy fill */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a1a2e, #0f3460) !important;
    color: white !important;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(26,26,46,0.40);
}

/* ===== PRIMARY BUTTON (orange) ===== */
/* Used for "Generate", "ADD SELECTED", etc. */
button[kind="primary"] {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    transition: all var(--transition-normal);
    padding: 10px 20px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 13px;
    box-shadow: 0 2px 8px rgba(255,152,0,0.25);
}
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #f57c00, #e65100) !important;
    box-shadow: 0 6px 20px rgba(255,152,0,0.50);
    transform: translateY(-2px);
}
button[kind="primary"]:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(255,152,0,0.30);
}

/* ===== SECONDARY BUTTON (blue) ===== */
/* Used for "ADD FILTERED", "Download Excel", etc. */
button[kind="secondary"] {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    transition: all var(--transition-normal);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 13px;
    box-shadow: 0 2px 8px rgba(0,123,255,0.20);
}
button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #0056b3, #003d82) !important;
    box-shadow: 0 6px 20px rgba(0,123,255,0.40);
    transform: translateY(-2px);
}
button[kind="secondary"]:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(0,123,255,0.25);
}

/* ===== TERTIARY / DEFAULT BUTTON ===== */
/* Neutral grey buttons like "Clear Filters" */
button[kind="tertiary"] {
    background-color: var(--bg-lighter) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-light) !important;
    font-weight: 600;
    border-radius: 8px;
    transition: all var(--transition-fast);
    font-size: 13px;
}
button[kind="tertiary"]:hover {
    background-color: #e3e7f0 !important;
    border-color: #adb5bd !important;
    color: var(--primary-dark) !important;
}

/* ===== DATA EDITOR / TABLE ===== */
div[data-testid="stDataEditor"] {
    background-color: var(--bg-white) !important;
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

/* ===== FILTER INPUTS ===== */
/* Rounded corners on dropdowns and multiselects */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 8px;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(0,123,255,0.12) !important;
}
/* Text inputs */
.stTextInput input {
    border-radius: 8px !important;
    border: 1px solid var(--border-light) !important;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
    font-size: 14px;
    padding: 8px 12px;
}
.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(0,123,255,0.12) !important;
}

/* ===== EXPANDER (Category groups in filter tab) ===== */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, var(--bg-light), #eef1f7);
    border-radius: 8px !important;
    font-weight: 600;
    color: var(--primary-dark);
    transition: all var(--transition-fast);
    border: 1px solid var(--border-lighter);
    padding: 10px 16px !important;
}
.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, #e4e9f5, #dde5f4);
    border-color: #c5cfe0;
}
.streamlit-expanderContent {
    border-left: 3px solid var(--accent-blue);
    padding-left: 15px;
    background-color: rgba(248, 250, 255, 0.6);
    border-radius: 0 0 8px 0;
}

/* ===== SUBCATEGORY HEADER (in product list) ===== */
.subcat-header {
    background: linear-gradient(135deg, #e8f4fd, #dceefb);
    padding: 10px 16px;
    margin: 14px 0 8px 0;
    border-left: 4px solid var(--accent-blue);
    font-weight: 700;
    color: var(--primary-dark);
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    letter-spacing: 0.4px;
    box-shadow: 0 1px 4px rgba(0,123,255,0.08);
}

/* ===== SIDEBAR ===== */
/* Dark navy gradient sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f1a2e 60%, #0a1020 100%);
    border-right: 1px solid #2a2a4e;
}
section[data-testid="stSidebar"] .stMarkdown {
    color: #c8cfe0;
}
/* Sidebar headings in orange */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--accent-orange) !important;
    font-weight: 700;
    letter-spacing: 0.5px;
}
/* Sidebar buttons inherit orange styling */
section[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, #ff9800, #f57c00) !important;
    color: var(--primary-dark) !important;
    font-weight: bold;
    border-radius: 8px;
    border: none !important;
    transition: all var(--transition-normal);
}
section[data-testid="stSidebar"] button:hover {
    background: linear-gradient(135deg, #f57c00, #e65100) !important;
    transform: translateY(-1px);
}
/* Sidebar text inputs in dark style */
section[data-testid="stSidebar"] .stTextInput input {
    background-color: #2a2a4e;
    color: #ffffff;
    border-color: var(--accent-orange);
    border-radius: var(--radius-sm);
}
section[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #8888aa;
}
/* Sidebar captions */
section[data-testid="stSidebar"] .stCaption {
    color: #8899bb !important;
    font-size: 12px;
}
/* Sidebar expanders */
section[data-testid="stSidebar"] .streamlit-expanderHeader {
    background: rgba(255,255,255,0.05) !important;
    color: #d0d8ec !important;
    border-color: rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
    background: rgba(255,255,255,0.10) !important;
}

/* ===== PRODUCT STATS BAR ===== */
/* Horizontal stats strip above product list */
.stats-bar {
    background: linear-gradient(135deg, #f0f7ff 0%, #e6f0fd 100%);
    padding: 12px 24px;
    border-radius: var(--radius-md);
    margin: 12px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #c5d8f0;
    box-shadow: var(--shadow-sm);
}
.stats-bar .stat-item {
    font-size: 13px;
    color: #444;
    font-weight: 500;
}
.stats-bar .stat-value {
    font-weight: 800;
    color: var(--primary-dark);
    font-size: 16px;
}

/* ===== STATUS BADGES ===== */
/* Small pill-shaped badges shown next to product names */
.badge-modified {
    display: inline-block;
    background: linear-gradient(135deg, #fff3cd, #ffeeba);
    color: #856404;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid #ffc107;
    margin-left: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-custom {
    display: inline-block;
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    color: #155724;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid #28a745;
    margin-left: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
/* NEW badge pulses to draw attention */
.badge-new {
    display: inline-block;
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    color: #721c24;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid #dc3545;
    margin-left: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    animation: pulse-badge 2s ease-in-out infinite;
}
@keyframes pulse-badge {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.65; }
}
.badge-in-cart {
    display: inline-block;
    background: linear-gradient(135deg, #cce5ff, #b8daff);
    color: #004085;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid #007bff;
    margin-left: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ===== SECTION HEADERS (inside tabs) ===== */
/* Dark navy strip at the top of each tab section */
.section-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d5e 100%);
    color: white;
    padding: 14px 24px;
    border-radius: var(--radius-md);
    margin: 18px 0 16px 0;
    font-size: 18px;
    font-weight: 700;
    border-left: 5px solid var(--accent-orange);
    box-shadow: var(--shadow-md);
    letter-spacing: 0.6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ===== FORM STYLING ===== */
.stForm {
    background: linear-gradient(135deg, #fafbff, #f4f7ff);
    border: 1px solid #dde3f0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: var(--shadow-sm);
}

/* ===== PRODUCT ROW (list view in filter tab) ===== */
.product-row {
    display: flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: var(--radius-sm);
    transition: background-color var(--transition-fast);
    margin: 1px 0;
    border: 1px solid transparent;
}
.product-row:hover {
    background-color: #f4f7ff;
    border-color: #dde8ff;
}
/* Small thumbnail image next to product name */
.product-thumb {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 1px solid var(--border-lighter);
    object-fit: cover;
    background-color: #f5f5f5;
    flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
/* Grey placeholder when no image available */
.product-thumb-placeholder {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 1px solid var(--border-lighter);
    background: linear-gradient(135deg, #f0f0f0, #e4e4e4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    color: var(--text-muted);
    flex-shrink: 0;
}

/* ===== CONFIRMATION DIALOGS ===== */
/* Warning / confirm action boxes */
.confirm-dialog {
    background: linear-gradient(135deg, #fff8e1, #fff3cd);
    border: 2px solid #ffc107;
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: var(--shadow-md);
}
/* Danger / destructive action confirmation */
.confirm-dialog-danger {
    background: linear-gradient(135deg, #fff1f1, #f8d7da);
    border: 2px solid #dc3545;
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: var(--shadow-md);
}

/* ===== CUSTOM PRODUCT CARD (in Add Product tab) ===== */
.custom-product-card {
    background: var(--bg-white);
    border: 1px solid var(--border-lighter);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: all var(--transition-normal);
}
.custom-product-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--accent-blue);
    transform: translateY(-1px);
}

/* ===== ALERTS / INFO BOXES ===== */
.stAlert {
    border-radius: var(--radius-md);
}

/* ===== DIVIDERS ===== */
hr {
    border: none;
    border-top: 2px solid var(--bg-lighter);
    margin: 20px 0;
}

/* ===== CART COUNT BADGE (shown in tab label) ===== */
.cart-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-orange);
    color: white;
    font-size: 11px;
    font-weight: 800;
    min-width: 20px;
    height: 20px;
    border-radius: 10px;
    padding: 0 6px;
    margin-left: 6px;
}

/* ===== EMPTY STATE (when cart is empty, no results, etc.) ===== */
.empty-state {
    text-align: center;
    padding: 50px 20px;
    color: var(--text-muted);
}
.empty-state-icon {
    font-size: 52px;
    margin-bottom: 16px;
    opacity: 0.45;
}

/* ===== PROGRESS BAR ===== */
/* Orange→blue gradient on all Streamlit progress bars */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-orange), var(--accent-blue)) !important;
    border-radius: 4px;
}

/* ===== METRIC CARDS ===== */
/* Style Streamlit metric elements (used in stats) */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #f8faff, #eef3ff);
    border: 1px solid #dde5f5;
    border-radius: var(--radius-md);
    padding: 14px 18px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition-fast);
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md);
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    color: var(--primary-dark);
    font-weight: 800;
    font-size: 26px;
}

/* ===== DOWNLOAD BUTTONS ===== */
/* Special styling for download button wrappers */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #28a745, #1e7e34) !important;
    color: white !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    transition: all var(--transition-normal);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 13px;
    box-shadow: 0 2px 8px rgba(40,167,69,0.25);
}
[data-testid="stDownloadButton"] button:hover {
    background: linear-gradient(135deg, #218838, #155724) !important;
    box-shadow: 0 6px 20px rgba(40,167,69,0.40);
    transform: translateY(-2px);
}

/* ===== SCROLLBAR STYLING ===== */
/* Custom thin scrollbars for a clean look */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: var(--bg-lighter);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb {
    background: #b0b8c4;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #8a94a1;
}

/* ===== TOOLTIP ===== */
[data-testid="stTooltipIcon"] {
    color: var(--accent-blue);
}

/* ===== CHECKBOX STYLING ===== */
/* Slightly larger clickable checkboxes */
[data-testid="stCheckbox"] label {
    font-size: 14px;
}

/* ===== TOAST NOTIFICATIONS ===== */
/* Streamlit toast pop-up - slightly rounded */
[data-testid="stToast"] {
    border-radius: var(--radius-md) !important;
    font-weight: 600;
}

/* ===== RESPONSIVE HELPERS ===== */
/* Compact layout on small screens (tablets / narrow viewports) */
@media (max-width: 768px) {
    .main-title {
        font-size: 20px;
        padding: 18px 16px;
        letter-spacing: 1px;
    }
    .stats-bar {
        flex-direction: column;
        gap: 6px;
        text-align: center;
    }
    .section-header {
        font-size: 15px;
        padding: 10px 16px;
    }
}
</style>
"""
