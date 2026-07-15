"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""

import os
from urllib.parse import urlparse

import streamlit as st

# ═════════════════════════════════════════════
# Session State
# ═════════════════════════════════════════════
if "source_type" not in st.session_state:
    st.session_state.source_type = "Screenshot"
if "audit_requested" not in st.session_state:
    st.session_state.audit_requested = False
if "audit_name" not in st.session_state:
    st.session_state.audit_name = ""
if "audit_source" not in st.session_state:
    st.session_state.audit_source = ""


def valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def reset_audit():
    st.session_state.audit_requested = False
    st.session_state.audit_name = ""
    st.session_state.audit_source = ""


# ═════════════════════════════════════════════
# Page Config
# ═════════════════════════════════════════════
st.set_page_config(
    page_title="UX Lens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════
# CSS — diseño fiel a la referencia UX Lens
# ═════════════════════════════════════════════
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: #0B0F1A;
            color: #E8EEF7;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #080C14;
            border-right: 1px solid #0F1B2E;
            min-width: 56px !important;
            max-width: 56px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 16px 0 0 0;
        }

        [data-testid="stSidebar"] .stMarkdown {
            padding: 0 !important;
        }

        /* Main content padding */
        .block-container {
            max-width: 100%;
            padding: 0 20px 20px 20px;
        }

        /* Top bar */
        .top-bar {
            align-items: center;
            border-bottom: 1px solid #111B2E;
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
        }

        .logo-area {
            align-items: center;
            display: flex;
            gap: 10px;
        }

        .logo-icon {
            align-items: center;
            display: flex;
            justify-content: center;
        }

        .logo-text {
            color: #F0F5FF;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }

        .breadcrumb {
            color: #5D7599;
            font-size: 11px;
            margin-left: 24px;
        }

        .breadcrumb strong {
            color: #8FA8C8;
            font-weight: 600;
        }

        .top-actions {
            align-items: center;
            display: flex;
            gap: 10px;
        }

        .status-badge {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.28);
            border-radius: 20px;
            color: #3DD476;
            font-size: 10px;
            font-weight: 700;
            padding: 5px 12px;
        }

        /* Preview workspace */
        .workspace-frame {
            background: #0E1521;
            border: 1px solid #162236;
            border-radius: 10px;
            overflow: hidden;
        }

        .workspace-header {
            align-items: center;
            background: #0D1320;
            border-bottom: 1px solid #162236;
            display: flex;
            justify-content: space-between;
            padding: 12px 16px;
        }

        .workspace-title {
            color: #E2EBF8;
            font-size: 13px;
            font-weight: 700;
        }

        .live-badge {
            background: rgba(34, 197, 94, 0.14);
            border: 1px solid rgba(34, 197, 94, 0.32);
            border-radius: 4px;
            color: #3DD476;
            font-size: 9px;
            font-weight: 800;
            margin-left: 8px;
            padding: 2px 7px;
            vertical-align: middle;
        }

        .workspace-tags {
            color: #4A6388;
            font-size: 10px;
            margin-top: 3px;
        }

        .workspace-actions {
            display: flex;
            gap: 8px;
        }

        .preview-body {
            align-items: center;
            background:
                radial-gradient(ellipse 60% 40% at 50% 0%, rgba(30, 90, 160, 0.10), transparent),
                #070B14;
            display: flex;
            justify-content: center;
            min-height: 560px;
            padding: 24px;
        }

        .empty-state {
            color: #5A7398;
            max-width: 380px;
            text-align: center;
        }

        .empty-icon {
            align-items: center;
            background: #0F1F36;
            border: 1px solid #1E3A5F;
            border-radius: 16px;
            color: #4A9EFF;
            display: flex;
            font-size: 28px;
            height: 64px;
            justify-content: center;
            margin: 0 auto 16px;
            width: 64px;
        }

        .empty-title {
            color: #C8D8EE;
            font-size: 15px;
            font-weight: 700;
            margin: 0 0 6px;
        }

        .empty-desc {
            font-size: 12px;
            line-height: 1.5;
            margin: 0;
        }

        /* Right panel */
        .results-panel {
            background: #0E1521;
            border: 1px solid #162236;
            border-radius: 10px;
            padding: 18px;
        }

        .panel-label {
            color: #4E6788;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1.2px;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .panel-title {
            color: #F0F5FF;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .score-donut {
            align-items: center;
            display: flex;
            gap: 16px;
            margin-bottom: 20px;
        }

        .donut-ring {
            align-items: center;
            display: flex;
            height: 72px;
            justify-content: center;
            position: relative;
            width: 72px;
        }

        .donut-ring svg {
            position: absolute;
            transform: rotate(-90deg);
        }

        .donut-text {
            position: relative;
            text-align: center;
            z-index: 2;
        }

        .donut-value {
            color: #F0F5FF;
            font-size: 20px;
            font-weight: 800;
            line-height: 1;
        }

        .donut-grade {
            color: #9AB;
            font-size: 11px;
            font-weight: 700;
        }

        .score-info-title {
            color: #D0DFF0;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 3px;
        }

        .score-info-desc {
            color: #5D7599;
            font-size: 11px;
            line-height: 1.4;
        }

        /* Metrics grid */
        .metric-box {
            background: #0C1322;
            border: 1px solid #142238;
            border-radius: 8px;
            margin-bottom: 8px;
            padding: 10px 12px;
        }

        .metric-label {
            color: #4E6788;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
            text-transform: uppercase;
        }

        .metric-value {
            align-items: baseline;
            display: flex;
            gap: 8px;
        }

        .metric-number {
            font-size: 22px;
            font-weight: 800;
            line-height: 1;
        }

        .metric-grade {
            border-radius: 4px;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 6px;
        }

        /* Insights */
        .insights-header {
            align-items: center;
            display: flex;
            justify-content: space-between;
            margin: 16px 0 10px;
        }

        .insights-title {
            color: #D0DFF0;
            font-size: 13px;
            font-weight: 700;
        }

        .insights-count {
            background: #0F2848;
            border: 1px solid #1B4A7A;
            border-radius: 10px;
            color: #4A9EFF;
            font-size: 9px;
            font-weight: 800;
            padding: 3px 8px;
        }

        .finding-item {
            background: #0C1322;
            border: 1px solid #142238;
            border-radius: 8px;
            margin-bottom: 8px;
            padding: 11px 12px;
        }

        .finding-top {
            align-items: center;
            display: flex;
            gap: 8px;
            margin-bottom: 5px;
        }

        .finding-dot {
            border-radius: 50%;
            flex-shrink: 0;
            height: 8px;
            width: 8px;
        }

        .finding-title {
            color: #D8E4F5;
            flex: 1;
            font-size: 12px;
            font-weight: 700;
        }

        .finding-sev {
            border-radius: 4px;
            font-size: 9px;
            font-weight: 800;
            padding: 2px 7px;
        }

        .finding-desc {
            color: #5D7599;
            font-size: 11px;
            line-height: 1.45;
            margin-left: 16px;
        }

        /* Buttons override */
        .stButton > button {
            border-radius: 6px !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            min-height: 34px !important;
        }

        .stButton > button[kind="primary"] {
            background: #2563EB !important;
            border-color: #2563EB !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: #3B82F6 !important;
            border-color: #3B82F6 !important;
        }

        /* Inputs */
        .stTextInput input {
            background: #0A1120 !important;
            border: 1px solid #1A3355 !important;
            border-radius: 6px !important;
            color: #E2EBF8 !important;
            font-size: 12px !important;
        }

        .stRadio label {
            color: #A8BED8 !important;
            font-size: 12px !important;
        }

        [data-testid="stFileUploader"] {
            background: #0A1120;
            border: 1px dashed #2A5588;
            border-radius: 8px;
            padding: 6px;
        }

        /* Nav icons sidebar */
        .nav-item {
            align-items: center;
            color: #3A5270;
            cursor: pointer;
            display: flex;
            font-size: 17px;
            height: 40px;
            justify-content: center;
            margin: 0 8px 4px;
            transition: all 0.15s;
        }

        .nav-item:hover {
            color: #6A9AD0;
        }

        .nav-item.active {
            background: #0F2A4A;
            border-radius: 8px;
            color: #4A9EFF;
        }

        /* Hide streamlit default elements /
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════
# Sidebar
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0 14px 18px;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5z" fill="#6366F1"/>
                <path d="M2 17l10 5 10-5" stroke="#6366F1" stroke-width="2" fill="none"/>
                <path d="M2 12l10 5 10-5" stroke="#4F46E5" stroke-width="2" fill="none"/>
            </svg>
        </div>
        <div class="nav-item">⊞</div>
        <div class="nav-item">▱</div>
        <div class="nav-item active">◉</div>
        <div class="nav-item">▤</div>
        <div class="nav-item">⚙</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            bottom: 14px;
            color: #22C55E;
            font-size: 10px;
            position: fixed;
            text-align: center;
            width: 56px;
        ">
            ●<br><span style="color:#4A5D75;font-size:8px;">online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ═════════════════════════════════════════════
# Top Bar
# ═════════════════════════════════════════════
left_col, right_col = st.columns([4, 1.6])

with left_col:
    st.markdown(
        """
        <div class="top-bar" style="border-bottom:none;padding-bottom:6px;">
            <div style="display:flex;align-items:center;">
                <div class="logo-area">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                        <path d="M12 2L2 7l10 5 10-5-10-5z" fill="#6366F1"/>
                        <path d="M2 17l10 5 10-5" stroke="#6366F1" stroke-width="2" fill="none"/>
                        <path d="M2 12l10 5 10-5" stroke="#4F46E5" stroke-width="2" fill="none"/>
                    </svg>
                    <span class="logo-text">UX LENS</span>
                </div>
                <div class="breadcrumb">
                    <strong>Projects</strong> &nbsp;›&nbsp; Nova Atelier Page Web
                    &nbsp;›&nbsp; <strong>Visual Hierarchy Audit</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class="top-bar" style="border-bottom:none;justify-content:flex-end;padding-bottom:6px;">
            <div class="top-actions">
                <span class="status-badge">● Scan complete</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    export_col, share_col = st.columns([1, 1])
    with export_col:
        st.button("Export report", use_container_width=True)
    with share_col:
        st.button("Share", type="primary", use_container_width=True)

st.markdown("<div style='border-bottom:1px solid #111B2E;margin-bottom:16px;'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════
# Main Layout
# ═════════════════════════════════════════════
preview_col, results_col = st.columns([3.2, 1], gap="medium")

# ── Preview Column ──
with preview_col:
    st.markdown(
        """
        <div class="workspace-frame">
            <div class="workspace-header">
                <div>
                    <span class="workspace-title">
                        Nova Atelier — E-commerce Homepage
                        <span class="live-badge">LIVE AUDIT</span>
                    </span>
                    <div class="workspace-tags">
                        Desktop web &nbsp;•&nbsp; 1440 px viewport &nbsp;•&nbsp; Visual hierarchy &nbsp;•&nbsp; 5 issues found
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Selección de fuente (URL o Imagen)
    source_type = st.radio(
        "",
        ["Screenshot", "Website URL"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.source_type = source_type

    if source_type == "Screenshot":
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
    else:
        website_url = st.text_input("", placeholder="https://your-website.com", label_visibility="collapsed")

    # Cuerpo del Preview
    st.markdown('<div class="preview-body">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">◈</div>
            <div class="empty-title">Your interface preview will appear here</div>
            <p class="empty-desc">Upload a screenshot or switch to Website URL to audit a live page.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<​/div>", unsafe_allow_html=True)

# --- Columna de Resultados (Derecha) ---
with results_col:
    st.markdown(
        """
        <div class="results-panel">
            <div class="panel-label">UX Audit Results</div>
            <div class="panel-title">Nova Atelier</div>
            <div style="color:#4A6388;font-size:11px;text-align:center;padding:20px 0;">
                No issues detected yet.<br>Run an audit to populate findings.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("Start UX Audit", type="primary", use_container_width=True):
        st.session_state.audit_requested = True

if st.session_state.audit_requested:
    st.success("Audit request registered. Connect an AI engine to see real findings.")
