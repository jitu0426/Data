"""
HEM Product Catalogue - Enhanced Professional CSS
All application styling in one place.
"""

APP_CSS = """
<style>
/* ============================================================
   HEM PRODUCT CATALOGUE - PROFESSIONAL UI THEME
   ============================================================ */

/* ===== CSS VARIABLES ===== */
:root {
    --primary-dark: #1a1a2e;
    --primary-mid: #16213e;
    --primary-light: #2d2d5e;
    --accent-orange: #ff9800;
    --accent-orange-dark: #f57c00;
    --accent-blue: #007bff;
    --accent-blue-dark: #0056b3;
    --bg-white: #ffffff;
    --bg-light: #f8f9fa;
    --bg-lighter: #f0f2f6;
    --text-primary: #000000;
    --text-secondary: #555;
    --text-muted: #999;
    --border-light: #dee2e6;
    --border-lighter: #e0e0e0;
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.15);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --transition-fast: 0.15s ease;
    --transition-normal: 0.25s ease;
}

/* ===== GLOBAL APP STYLES ===== */
.stApp {
    background-color: var(--bg-white) !important;
    color: var(--text-primary) !important;
}

/* ===== HEADER / TITLE ===== */
.main-title {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 50%, #16213e 100%);
    color: white !important;
    padding: 24px 30px;
    border-radius: var(--radius-lg);
    margin-bottom: 24px;
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 4px solid var(--accent-orange);
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}
.main-title::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 200%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    animation: shimmer 3s infinite;
}
@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* ===== TAB NAVIGATION ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: var(--bg-lighter);
    padding: 6px 8px;
    border-radius: var(--radius-md);
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 14px;
    color: var(--text-secondary);
    background-color: transparent;
    border: none;
    transition: all var(--transition-fast);
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(26,26,46,0.08);
    color: var(--primary-dark);
}
.stTabs [aria-selected="true"] {
    background-color: var(--primary-dark) !important;
    color: white !important;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(26,26,46,0.35);
}

/* ===== BUTTON STYLES ===== */
button[kind="primary"] {
    background: linear-gradient(135deg, #ff9800, #f57c00) !important;
    color: white !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    transition: all var(--transition-normal);
    padding: 8px 18px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 13px;
}
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #f57c00, #e65100) !important;
    box-shadow: 0 4px 16px rgba(255,152,0,0.45);
    transform: translateY(-1px);
}
button[kind="secondary"] {
    background: linear-gradient(135deg, #007bff, #0056b3) !important;
    color: white !important;
    border: none !important;
    font-weight: 700;
    border-radius: 8px;
    transition: all var(--transition-normal);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 13px;
}
button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #0056b3, #003d82) !important;
    box-shadow: 0 4px 16px rgba(0,123,255,0.35);
    transform: translateY(-1px);
}

/* ===== DATA EDITOR / TABLE ===== */
div[data-testid="stDataEditor"] {
    background-color: var(--bg-white) !important;
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

/* ===== FILTER PANEL ===== */
.stSelectbox > div > div {
    border-radius: 8px;
}
.stMultiSelect > div > div {
    border-radius: 8px;
}

/* ===== EXPANDER (Category groups) ===== */
.streamlit-expanderHeader {
    background-color: var(--bg-light);
    border-radius: 8px;
    font-weight: 600;
    color: var(--primary-dark);
    transition: background-color var(--transition-fast);
}
.streamlit-expanderHeader:hover {
    background-color: #e8ecf1;
}
.streamlit-expanderContent {
    border-left: 3px solid var(--accent-blue);
    padding-left: 15px;
}

/* ===== SUBCATEGORY HEADER ===== */
.subcat-header {
    background: linear-gradient(135deg, #e8f4fd, #dceefb);
    padding: 10px 16px;
    margin: 14px 0 8px 0;
    border-left: 4px solid var(--accent-blue);
    font-weight: 700;
    color: var(--primary-dark);
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    letter-spacing: 0.3px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f1a2e 100%);
}
section[data-testid="stSidebar"] .stMarkdown {
    color: #d0d0e0;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--accent-orange) !important;
}
section[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, #ff9800, #f57c00) !important;
    color: var(--primary-dark) !important;
    font-weight: bold;
    border-radius: 8px;
    border: none !important;
}
section[data-testid="stSidebar"] .stTextInput input {
    background-color: #2a2a4e;
    color: white;
    border-color: var(--accent-orange);
    border-radius: var(--radius-sm);
}

/* ===== PRODUCT STATS BAR ===== */
.stats-bar {
    background: linear-gradient(135deg, #f0f7ff 0%, #e3f0fd 100%);
    padding: 12px 24px;
    border-radius: var(--radius-md);
    margin: 12px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #c8ddf0;
    box-shadow: var(--shadow-sm);
}
.stats-bar .stat-item {
    font-size: 14px;
    color: #444;
    font-weight: 500;
}
.stats-bar .stat-value {
    font-weight: 800;
    color: var(--primary-dark);
    font-size: 16px;
}

/* ===== STATUS BADGES ===== */
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
    50% { opacity: 0.7; }
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

/* ===== SECTION HEADERS ===== */
.section-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2d5e 100%);
    color: white;
    padding: 14px 24px;
    border-radius: var(--radius-md);
    margin: 18px 0 12px 0;
    font-size: 18px;
    font-weight: 700;
    border-left: 5px solid var(--accent-orange);
    box-shadow: var(--shadow-md);
    letter-spacing: 0.5px;
}

/* ===== FORM STYLING ===== */
.stForm {
    background-color: var(--bg-light);
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    padding: 20px;
}

/* ===== PRODUCT ROW IN LIST ===== */
.product-row {
    display: flex;
    align-items: center;
    padding: 6px 8px;
    border-radius: var(--radius-sm);
    transition: background-color var(--transition-fast);
    margin: 1px 0;
}
.product-row:hover {
    background-color: #f8f9ff;
}
.product-thumb {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 1px solid var(--border-lighter);
    object-fit: cover;
    background-color: #f5f5f5;
    flex-shrink: 0;
}
.product-thumb-placeholder {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 1px solid var(--border-lighter);
    background: linear-gradient(135deg, #f5f5f5, #ececec);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    color: var(--text-muted);
    flex-shrink: 0;
}

/* ===== CONFIRMATION DIALOG ===== */
.confirm-dialog {
    background: linear-gradient(135deg, #fff3cd, #ffeeba);
    border: 2px solid #ffc107;
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: var(--shadow-md);
}
.confirm-dialog-danger {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    border: 2px solid #dc3545;
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: var(--shadow-md);
}

/* ===== CUSTOM PRODUCT CARD ===== */
.custom-product-card {
    background: var(--bg-white);
    border: 1px solid var(--border-lighter);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: all var(--transition-normal);
}
.custom-product-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--accent-blue);
}

/* ===== INFO BOXES ===== */
.stAlert {
    border-radius: var(--radius-md);
}

/* ===== DIVIDERS ===== */
hr {
    border: none;
    border-top: 2px solid var(--bg-lighter);
    margin: 16px 0;
}

/* ===== CART COUNT BADGE (for tab) ===== */
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

/* ===== EMPTY STATE ===== */
.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-muted);
}
.empty-state-icon {
    font-size: 48px;
    margin-bottom: 12px;
    opacity: 0.5;
}

/* ===== LOADING / PROGRESS ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-orange), var(--accent-blue)) !important;
}

/* ===== SCROLLBAR STYLING ===== */
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

/* ===== TOOLTIP STYLE ===== */
[data-testid="stTooltipIcon"] {
    color: var(--accent-blue);
}

/* ===== RESPONSIVE HELPERS ===== */
@media (max-width: 768px) {
    .main-title {
        font-size: 20px;
        padding: 16px 20px;
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
