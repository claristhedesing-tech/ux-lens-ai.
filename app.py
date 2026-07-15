"""
UX Lens AI — Main Application

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""

from html import escape
from urllib.parse import urlparse

import streamlit as st


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
# Helpers
# ═════════════════════════════════════════════
def valid_url(url: str) -> bool:
    """Return True only for complete HTTP/HTTPS URLs."""
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def reset_audit() -> None:
    """Clear the current audit state."""
    st.session_state.audit_requested = False
    st.session_state.audit_name = ""
    st.session_state.audit_source = ""


# ═════════════════════════════════════════════
# Session State
# ═════════════════════════════════════════════
if "audit_requested" not in st.session_state:
    st.session_state.audit_requested = False

if "audit_name" not in st.session_state:
    st.session_state.audit_name = ""

if "audit_source" not in st.session_state:
    st.session_state.audit_source = ""


# ═════════════════════════════════════════════
# CSS
# ═════════════════════════════════════════════
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html,
        body,
        [class*="css"] {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: #0B0F1A;
            color: #E8EEF7;
        }

        .block-container {
            max-width: 100%;
            padding: 0 20px 20px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #080C14;
            border-right: 1px solid #0F1B2E;
            min-width: 56px !important;
            max-width: 56px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 16px 0 0;
        }

        [data-testid="stSidebar"] .stMarkdown {
            padding: 0 !important;
        }

        .nav-item {
            align-items: center;
            color: #3A5270;
            cursor: pointer;
            display: flex;
            font-size: 17px;
            height: 40px;
            justify-content: center;
            margin: 0 8px 4px;
            transition: all 0.15s ease;
        }

        .nav-item:hover {
            color: #6A9AD0;
        }

        .nav-item.active {
            background: #0F2A4A;
            border-radius: 8px;
            color: #4A9EFF;
        }

        .online-status {
            color: #22C55E;
            font-size: 10px;
            margin-top: 24px;
            text-align: center;
        }

        .online-status span {
            color: #4A5D75;
            font-size: 8px;
        }

        /* Header */
        .top-bar {
            align-items: center;
            display: flex;
            justify-content: space-between;
            padding: 10px 0 6px;
        }

        .logo-area {
            align-items: center;
            display: flex;
            gap: 10px;
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

        .status-badge {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.28);
            border-radius: 20px;
            color: #3DD476;
            font-size: 10px;
            font-weight: 700;
            padding: 5px 12px;
        }

        /* Cards and preview */
        .workspace-frame,
        .results-panel {
            background: #0E1521;
            border: 1px solid #162236;
            border-radius: 10px;
            overflow: hidden;
        }

        .workspace-header {
            background: #0D1320;
            border-bottom: 1px solid #162236;
            padding: 12px 16px;
        }

        .workspace-title {
            color: #E2EBF8;
            font-size: 13px;
            font-weight: 700;
        }

        .workspace-tags {
            color: #4A6388;
            font-size: 10px;
            margin-top: 3px;
        }

        .preview-body {
            align-items: center;
            background:
                radial-gradient(
                    ellipse 60% 40% at 50% 0%,
                    rgba(30, 90, 160, 0.10),
                    transparent
                ),
                #070B14;
            display: flex;
            justify-content: center;
            min-height: 420px;
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
            margin-bottom: 6px;
        }

        .empty-desc {
            font-size: 12px;
            line-height: 1.5;
            margin: 0;
        }

        /* Results panel */
        .results-panel {
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
            margin-bottom: 12px;
            word-break: break-word;
        }

        .panel-description {
            color: #5D7599;
            font-size: 11px;
            line-height: 1.5;
        }

        .audit-complete {
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(34, 197, 94, 0.24);
            border-radius: 8px;
            color: #86E5AA;
            font-size: 11px;
            line-height: 1.5;
            margin-top: 16px;
            padding: 12px;
        }

        /* Streamlit buttons */
        div[data-testid="stButton"] > button {
            border-radius: 6px !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            min-height: 34px !important;
            transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
        }

        /* Secondary buttons */
        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stButton"] > button[data-testid="stBaseButton-secondary"] {
            background: #0C1322 !important;
            border: 1px solid #1E3A5F !important;
            color: #A8BED8 !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button[data-testid="stBaseButton-secondary"]:hover {
            background: #0F1F36 !important;
            border-color: #4A9EFF !important;
            color: #E8F1FF !important;
        }

        /* Primary buttons */
        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"] {
            background: #2563EB !important;
            border: 1px solid #2563EB !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover,
        div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"]:hover {
            background: #3B82F6 !important;
            border-color: #3B82F6 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stButton"] > button:disabled {
            background: #152033 !important;
            border-color: #233652 !important;
            color: #61728A !important;
            cursor: not-allowed !important;
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

        .stTextInput input {
            background: #0A1120 !important;
            border: 1px solid #1A3355 !important;
            border-radius: 6px !important;
            color: #E2EBF8 !important;
        }

        /* Hide Streamlit elements */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }
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

        <div class="online-status">
            ●<br><span>online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════
# Input and dynamic project details
# ═════════════════════════════════════════════
source_type = st.session_state.get("source_type", "Screenshot")

uploaded_file = None
website_url = ""

if source_type == "Screenshot":
    project_name = "Untitled audit"
    source_description = "Upload a screenshot to begin"
else:
    project_name = "Untitled audit"
    source_description = "Enter a website URL to begin"


# ═════════════════════════════════════════════
# Top Bar
# ═════════════════════════════════════════════
left_col, right_col = st.columns([4, 1.6])

with left_col:
    st.markdown(
        """
        <div class="top-bar">
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
                    <strong>Projects</strong> &nbsp;›&nbsp; Current audit
                    &nbsp;›&nbsp; <strong>Visual hierarchy</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    status_text = "● Scan complete" if st.session_state.audit_requested else "● Ready to scan"

    st.markdown(
        f"""
        <div class="top-bar" style="justify-content:flex-end;">
            <span class="status-badge">{status_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    export_col, share_col = st.columns(2)

    with export_col:
        st.button(
            "Export report",
            use_container_width=True,
            disabled=not st.session_state.audit_requested,
            key="export_report",
        )

    with share_col:
        st.button(
            "Share",
            type="primary",
            use_container_width=True,
            disabled=not st.session_state.audit_requested,
            key="share_report",
        )

st.markdown(
    "<div style='border-bottom:1px solid #111B2E;margin-bottom:16px;'></div>",
    unsafe_allow_html=True,
)


# ═════════════════════════════════════════════
# Main Layout
# ═════════════════════════════════════════════
preview_col, results_col = st.columns([3.2, 1], gap="medium")

with preview_col:
    st.radio(
        "Audit source",
        ["Screenshot", "Website URL"],
        horizontal=True,
        label_visibility="collapsed",
        key="source_type",
    )

    if st.session_state.source_type == "Screenshot":
        uploaded_file = st.file_uploader(
            "Upload screenshot",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed",
            key="screenshot_upload",
        )

        if uploaded_file is not None:
            project_name = uploaded_file.name.rsplit(".", 1)[0]
            source_description = "Screenshot uploaded"
        else:
            project_name = "Untitled audit"
            source_description = "Waiting for a screenshot"

    else:
        website_url = st.text_input(
            "Website URL",
            placeholder="https://your-website.com",
            label_visibility="collapsed",
            key="website_url",
        )

        if website_url and valid_url(website_url):
            project_name = urlparse(website_url).netloc.replace("www.", "")
            source_description = "Live website URL"
        elif website_url:
            project_name = "Untitled audit"
            source_description = "Enter a valid URL starting with https://"
        else:
            project_name = "Untitled audit"
            source_description = "Waiting for a website URL"

    safe_project_name = escape(project_name)
    safe_source_description = escape(source_description)

    st.markdown(
        f"""
        <div class="workspace-frame">
            <div class="workspace-header">
                <div class="workspace-title">{safe_project_name}</div>
                <div class="workspace-tags">{safe_source_description}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption=f"Preview: {project_name}",
            use_container_width=True,
        )
    else:
        st.markdown(
            """
            <div class="preview-body">
                <div class="empty-state">
                    <div class="empty-icon">◈</div>
                    <div class="empty-title">Your interface preview will appear here</div>
                    <p class="empty-desc">
                        Upload a screenshot or switch to Website URL to audit a live page.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════
# Results Column
# ═════════════════════════════════════════════
has_valid_source = uploaded_file is not None or valid_url(website_url)

with results_col:
    st.markdown(
        f"""
        <div class="results-panel">
            <div class="panel-label">UX Audit Results</div>
            <div class="panel-title">{safe_project_name}</div>
            <div class="panel-description">
                {safe_source_description}. Start the audit when your source is ready.
            </div>
        """,
        unsafe_allow_html=True,
    )

    start_audit = st.button(
        "Start UX Audit",
        type="primary",
        use_container_width=True,
        disabled=not has_valid_source,
        key="start_audit",
    )

    if start_audit:
        st.session_state.audit_requested = True
        st.session_state.audit_name = project_name
        st.session_state.audit_source = (
            uploaded_file.name if uploaded_file is not None else website_url
        )

    if st.session_state.audit_requested:
        audit_name = escape(st.session_state.audit_name or "Current audit")

        st.markdown(
            f"""
            <div class="audit-complete">
                <strong>Audit request registered</strong><br>
                {audit_name} is ready for analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Reset audit",
            use_container_width=True,
            key="reset_audit",
        ):
            reset_audit()
            st.rerun()

    st.markdown("<​/div>", unsafe_allow_html=True)
