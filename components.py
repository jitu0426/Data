"""
HEM Product Catalogue - Shared UI Components
Confirmation dialogs, thumbnails, stats bar, and reusable widgets.
"""
import streamlit as st


def confirm_action(key, label, message, danger=False):
    """Two-step confirmation dialog for destructive actions.
    Returns True only when user clicks 'Yes, confirm'.
    """
    confirm_key = f"_confirm_{key}"
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False

    if not st.session_state[confirm_key]:
        if st.button(label, key=key, use_container_width=True):
            st.session_state[confirm_key] = True
            st.rerun()
        return False
    else:
        css_class = "confirm-dialog-danger" if danger else "confirm-dialog"
        st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Yes, confirm", key=f"{key}_yes", type="primary", use_container_width=True):
                st.session_state[confirm_key] = False
                return True
        with col_no:
            if st.button("Cancel", key=f"{key}_no", use_container_width=True):
                st.session_state[confirm_key] = False
                st.rerun()
        return False


def product_thumbnail_html(image_b64, size=38):
    """Return HTML for a small product thumbnail image."""
    if image_b64 and len(str(image_b64)) > 100:
        return (
            f'<img src="data:image/jpeg;base64,{image_b64}" '
            f'class="product-thumb" '
            f'style="width:{size}px;height:{size}px;" />'
        )
    return (
        f'<div class="product-thumb-placeholder" '
        f'style="width:{size}px;height:{size}px;">N/A</div>'
    )


def stats_bar(items):
    """Render a stats bar. items is a list of (label, value) tuples."""
    spans = " ".join(
        f'<span class="stat-item">{label}: '
        f'<span class="stat-value">{value}</span></span>'
        for label, value in items
    )
    st.markdown(f'<div class="stats-bar">{spans}</div>', unsafe_allow_html=True)


def section_header(text):
    """Render a styled section header."""
    st.markdown(
        f'<div class="section-header">{text}</div>',
        unsafe_allow_html=True,
    )


def empty_state(icon, message):
    """Render a centered empty state message."""
    st.markdown(
        f'<div class="empty-state">'
        f'<div class="empty-state-icon">{icon}</div>'
        f'<div>{message}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
