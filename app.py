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
    /* Layout limpio de la auditoría */
.section-heading {
    margin: 4px 0 14px;
}

.eyebrow {
    color: #639AF0;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.1px;
    margin-bottom: 6px;
}

.section-title {
    color: #F3F7FF;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.2;
}

.section-description {
    color: #7890AE;
    font-size: 12px;
    margin-top: 6px;
}

.preview-card-header {
    align-items: center;
    background: #0E1521;
    border: 1px solid #1B2A42;
    border-bottom: 0;
    border-radius: 10px 10px 0 0;
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    padding: 14px 16px;
}

.preview-card-title {
    color: #EAF1FC;
    font-size: 13px;
    font-weight: 700;
}

.preview-card-meta {
    color: #67809F;
    font-size: 11px;
    margin-top: 4px;
}

.source-badge {
    background: #112A4B;
    border: 1px solid #244F82;
    border-radius: 999px;
    color: #85B9FF;
    font-size: 10px;
    font-weight: 700;
    padding: 4px 9px;
}

.preview-placeholder {
    align-items: center;
    background:
        radial-gradient(
            ellipse at top,
            rgba(37, 99, 235, 0.13),
            transparent 50%
        ),
        #080D17;
    border: 1px solid #1B2A42;
    border-radius: 0 0 10px 10px;
    color: #7390B1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 410px;
    padding: 36px;
    text-align: center;
}

.placeholder-icon {
    align-items: center;
    background: #102443;
    border: 1px solid #27558D;
    border-radius: 16px;
    color: #74AEFF;
    display: flex;
    font-size: 28px;
    height: 64px;
    justify-content: center;
    margin-bottom: 18px;
    width: 64px;
}

.placeholder-title {
    color: #DCE9FA;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

.preview-placeholder p {
    font-size: 12px;
    line-height: 1.55;
    margin: 0;
    max-width: 340px;
}

.results-card {
    background: #0E1521;
    border: 1px solid #1B2A42;
    border-radius: 10px;
    margin-bottom: 12px;
    padding: 18px;
}

.results-title {
    color: #F2F6FD;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.25;
    margin-bottom: 8px;
    overflow-wrap: anywhere;
}

.results-description {
    color: #7890AE;
    font-size: 12px;
    line-height: 1.5;
}

.audit-state {
    align-items: flex-start;
    background: rgba(34, 197, 94, 0.10);
    border: 1px solid rgba(74, 222, 128, 0.25);
    border-radius: 8px;
    color: #B3F2C8;
    display: flex;
    font-size: 12px;
    gap: 10px;
    line-height: 1.4;
    margin-top: 14px;
    padding: 12px;
}

.audit-state-icon {
    align-items: center;
    background: #1A9B53;
    border-radius: 50%;
    color: #FFFFFF;
    display: flex;
    flex: 0 0 auto;
    font-size: 11px;
    font-weight: 800;
    height: 18px;
    justify-content: center;
    width: 18px;
}

.audit-state p {
    color: #83C99B;
    margin: 3px 0 0;
}

/* Los botones secundarios no deben verse como botones blancos nativos */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: #101C2E !important;
    border: 1px solid #2A4B73 !important;
    color: #B8CDE8 !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: #172B46 !important;
    border-color: #5B9DFA !important;
    color: #FFFFFF !important;
}

/* Ajusta el espacio bajo radio y uploader */
[data-testid="stRadio"] {
    margin: 4px 0 10px;
}

[data-testid="stFileUploader"] {
    margin-bottom: 0;
}
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
preview_col, results_col = st.columns([2.2, 1], gap="large")

with preview_col:
    st.markdown(
        """
        <div class="section-heading">
            <div>
                <div class="eyebrow">AUDIT SOURCE</div>
                <div class="section-title">Add an interface to analyse</div>
                <div class="section-description">
                    Upload a screenshot or provide a public website URL.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    source_type = st.radio(
        "Source type",
        ["Screenshot", "Website URL"],
        horizontal=True,
        label_visibility="collapsed",
        key="source_type",
    )

    uploaded_file = None
    website_url = ""

    if source_type == "Screenshot":
        uploaded_file = st.file_uploader(
            "Upload screenshot",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed",
            key="screenshot_upload",
        )

        if uploaded_file is not None:
            project_name = uploaded_file.name.rsplit(".", 1)[0]
            source_description = "Screenshot ready for analysis"
        else:
            project_name = "Untitled audit"
            source_description = "No screenshot uploaded yet"

    else:
        website_url = st.text_input(
            "Website URL",
            placeholder="https://your-website.com",
            label_visibility="collapsed",
            key="website_url",
        )

        if website_url and valid_url(website_url):
            project_name = urlparse(website_url).netloc.replace("www.", "")
            source_description = "Website URL ready for analysis"
        elif website_url:
            project_name = "Untitled audit"
            source_description = "Enter a complete URL starting with https://"
        else:
            project_name = "Untitled audit"
            source_description = "No website URL entered yet"

    safe_project_name = escape(project_name)
    safe_source_description = escape(source_description)

    st.markdown(
        f"""
        <div class="preview-card-header">
            <div>
                <div class="preview-card-title">{safe_project_name}</div>
                <div class="preview-card-meta">{safe_source_description}</div>
            </div>
            <span class="source-badge">{escape(source_type)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption=f"Preview · {project_name}",
            use_container_width=True,
        )
    else:
        st.markdown(
            """
            <div class="preview-placeholder">
                <div class="placeholder-icon">◈</div>
                <div class="placeholder-title">Your interface preview will appear here</div>
                <p>
                    Upload a screenshot to view it here, or use a URL to start
                    an audit of a public website.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════
# Results / Action Panel
# ═════════════════════════════════════════════
has_valid_source = uploaded_file is not None or valid_url(website_url)

with results_col:
    st.markdown(
        f"""
        <div class="results-card">
            <div class="eyebrow">UX AUDIT</div>
            <div class="results-title">{safe_project_name}</div>
            <div class="results-description">
                {safe_source_description}
            </div>
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

    if not has_valid_source:
        st.caption("Add a screenshot or a valid public URL to enable the audit.")

    if start_audit:
        st.session_state.audit_requested = True
        st.session_state.audit_name = project_name
        st.session_state.audit_source = (
            uploaded_file.name if uploaded_file is not None else website_url
        )

    if st.session_state.audit_requested:
        saved_name = escape(st.session_state.audit_name or "Current audit")

        st.markdown(
            f"""
            <div class="audit-state">
                <div class="audit-state-icon">✓</div>
                <div>
                    <strong>Audit created</strong>
                    <p>{saved_name} is ready for analysis.</p>
                </div>
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
