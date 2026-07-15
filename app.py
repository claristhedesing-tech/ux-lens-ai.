"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""
from urllib.parse import urlparse

import streamlit as st

# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UX Lens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Estado de la aplicación
# ─────────────────────────────────────────────
if "source_type" not in st.session_state:
    st.session_state.source_type = "Screenshot"

if "audit_requested" not in st.session_state:
    st.session_state.audit_requested = False

if "audit_name" not in st.session_state:
    st.session_state.audit_name = ""

if "audit_source" not in st.session_state:
    st.session_state.audit_source = ""

# ─────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────
def valid_url(url):
    """Comprueba que se haya introducido una URL HTTP o HTTPS válida."""
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def reset_audit():
    """Reinicia el formulario para comenzar una nueva auditoría."""
    st.session_state.audit_requested = False
    st.session_state.audit_name = ""
    st.session_state.audit_source = ""


# ─────────────────────────────────────────────
# Estilos
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
        :root {
            --bg: #061426;
            --panel: #091B31;
            --panel-soft: #0C223C;
            --border: #183A5C;
            --border-soft: #12304D;
            --text: #EDF5FF;
            --muted: #7891AE;
            --blue: #268CFF;
            --blue-hover: #55A8FF;
            --green: #22C55E;
            --yellow: #F59E0B;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #05101F;
            border-right: 1px solid #102B48;
            min-width: 64px;
            max-width: 64px;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.7rem;
        }

        .block-container {
            max-width: 1600px;
            padding-top: 0.8rem;
            padding-bottom: 1rem;
        }

        .top-brand {
            align-items: center;
            display: flex;
            gap: 9px;
            min-height: 34px;
        }

        .brand-symbol {
            align-items: center;
            background: linear-gradient(135deg, #8B5CF6, #1686F9);
            clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
            display: flex;
            height: 22px;
            justify-content: center;
            width: 25px;
        }

        .brand-name {
            color: #F4F8FF;
            font-size: 12px;
            font-weight: 850;
            letter-spacing: 0.7px;
        }

        .breadcrumb {
            color: #627D9B;
            font-size: 11px;
            padding-top: 8px;
            white-space: nowrap;
        }

        .breadcrumb strong {
            color: #C8D8EA;
            font-weight: 700;
        }

        .status-pill {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.28);
            border-radius: 20px;
            color: #42D978;
            display: inline-block;
            font-size: 10px;
            font-weight: 750;
            margin-top: 4px;
            padding: 5px 10px;
            white-space: nowrap;
        }

        .workspace-header {
            align-items: center;
            background: #081A30;
            border: 1px solid #112F4F;
            border-radius: 9px 9px 0 0;
            display: flex;
            justify-content: space-between;
            padding: 12px 16px;
        }

        .workspace-title {
            color: #EAF3FF;
            font-size: 14px;
            font-weight: 800;
        }

        .workspace-subtitle {
            color: #6E89A7;
            font-size: 11px;
            margin-top: 3px;
        }

        .live-badge {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.30);
            border-radius: 4px;
            color: #38D875;
            font-size: 9px;
            font-weight: 800;
            margin-left: 8px;
            padding: 3px 6px;
            vertical-align: middle;
        }

        .preview-area {
            align-items: center;
            background:
                radial-gradient(circle at 50% 0%, rgba(32, 105, 186, 0.12), transparent 48%),
                #040D1A;
            border: 1px solid #112F4F;
            border-radius: 0 0 9px 9px;
            display: flex;
            justify-content: center;
            min-height: 570px;
            padding: 20px;
        }

        .empty-preview {
            color: #7792AF;
            max-width: 440px;
            text-align: center;
        }

        .empty-preview-icon {
            align-items: center;
            background: #0B2542;
            border: 1px solid #1E4C79;
            border-radius: 16px;
            color: #55A8FF;
            display: flex;
            font-size: 30px;
            height: 68px;
            justify-content: center;
            margin: 0 auto 18px;
            width: 68px;
        }

        .empty-preview h3 {
            color: #E4F0FC;
            font-size: 17px;
            margin: 0 0 8px;
        }

        .empty-preview p {
            font-size: 12px;
            line-height: 1.55;
            margin: 0;
        }

        .side-panel {
            background: #081A30;
            border: 1px solid #123454;
            border-radius: 9px;
            padding: 16px;
        }

        .side-label {
            color: #7994B1;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .side-title {
            color: #EDF5FF;
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 17px;
        }

        .source-card {
            background: #0B213A;
            border: 1px solid #163B5D;
            border-radius: 8px;
            margin-bottom: 9px;
            padding: 12px;
        }

        .source-card-title {
            color: #DDEBFA;
            font-size: 12px;
            font-weight: 750;
            margin-bottom: 5px;
        }

        .source-card-text {
            color: #7891AE;
            font-size: 11px;
            line-height: 1.45;
        }

        .ready-card {
            background: linear-gradient(135deg, rgba(38, 140, 255, 0.14), rgba(17, 70, 120, 0.10));
            border: 1px solid rgba(38, 140, 255, 0.35);
            border-radius: 8px;
            margin-top: 14px;
            padding: 13px;
        }

        .ready-title {
            color: #B8DBFF;
            font-size: 12px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .ready-text {
            color: #7FA3C7;
            font-size: 11px;
            line-height: 1.45;
        }

        .nav-icon {
            color: #52718F;
            font-size: 18px;
            margin-bottom: 21px;
            text-align: center;
        }

        .nav-icon-active {
            background: #0A3C70;
            border-radius: 8px;
            color: #55A8FF;
            font-size: 18px;
            margin-bottom: 21px;
            padding: 8px 0;
            text-align: center;
        }

        .stButton > button {
            border-radius: 6px !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            min-height: 34px !important;
        }

        .stTextInput input {
            background: #06182C !important;
            border: 1px solid #1A4269 !important;
            border-radius: 6px !important;
            color: #EAF3FF !important;
            font-size: 12px !important;
        }

        [data-testid="stFileUploader"] {
            background: #06182C;
            border: 1px dashed #296392;
            border-radius: 8px;
            padding: 7px;
        }

        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span {
            color: #88A4C1 !important;
        }

        .stRadio label {
            color: #B9CDE0 !important;
            font-size: 12px !important;
        }

        .stAlert {
            border-radius: 7px;
            font-size: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0 10px 20px;">
            <div class="brand-symbol"></div>
        </div>
        <div class="nav-icon">⊞</div>
        <div class="nav-icon">▱</div>
        <div class="nav-icon-active">◉</div>
        <div class="nav-icon">▤</div>
        <div class="nav-icon">⚙</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            bottom: 18px;
            color: #22C55E;
            font-size: 9px;
            left: 16px;
            position: fixed;
            text-align: center;
        ">
            ●<br><span style="color:#66819E;">online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Cabecera
# ─────────────────────────────────────────────
brand_col, bread_col, actions_col = st.columns([0.8, 4.1, 1.8])

with brand_col:
    st.markdown(
        """
        <div class="top-brand">
            <div class="brand-symbol"></div>
            <div class="brand-name">UX LENS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bread_col:
    st.markdown(
        """
        <div class="breadcrumb">
            <strong>Projects</strong> &nbsp;›&nbsp; New audit
            &nbsp;›&nbsp; <strong>UX analysis workspace</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

with actions_col:
    action_status, action_export, action_share = st.columns([1.35, 1, 0.9])

    with action_status:
        st.markdown(
            '<div class="status-pill">● Ready to audit</div>',
            unsafe_allow_html=True,
        )

    with action_export:
        st.button("⇩ Export", disabled=True, use_container_width=True)

    with action_share:
        st.button("↗ Share", disabled=True, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# Layout principal
# ─────────────────────────────────────────────
preview_col, form_col = st.columns([3.25, 1], gap="medium")

with preview_col:
    workspace_title_col, workspace_action_col = st.columns([4, 1])

    with workspace_title_col:
        st.markdown(
            """
            <div class="workspace-header">
                <div>
                    <div class="workspace-title">
                        New UX Audit <span class="live-badge">LIVE AUDIT</span>
                    </div>
                    <div class="workspace-subtitle">
                        Upload a design or provide a website address to begin.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with workspace_action_col:
        if st.button("New audit", use_container_width=True):
            reset_audit()
            st.rerun()

    source_type = st.radio(
        "Audit source",
        ["Screenshot", "Website URL"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.source_type = source_type

    uploaded_file = None
    website_url = ""

    if source_type == "Screenshot":
        uploaded_file = st.file_uploader(
            "Upload a screenshot or wireframe",
            type=["png", "jpg", "jpeg", "webp"],
            help="Supported formats: PNG, JPG, JPEG and WEBP.",
        )
    else:
        website_url = st.text_input(
            "Website URL",
            placeholder="https://your-website.com",
            help="Enter a public URL beginning with https:// or http://.",
        )

    st.markdown('<div class="preview-area">', unsafe_allow_html=True)

    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True)

    elif website_url.strip():
        if valid_url(website_url):
            st.markdown(
                f"""
                <div class="empty-preview">
                    <div class="empty-preview-icon">↗</div>
                    <h3>Website selected</h3>
                    <p>
                        The URL has been added to the audit request.<br>
                        Start the audit when you are ready.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="empty-preview">
                    <div class="empty-preview-icon">!</div>
                    <h3>Enter a valid URL</h3>
                    <p>
                        Include the full address, for example:
                        https://your-website.com
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.markdown(
            """
            <div class="empty-preview">
                <div class="empty-preview-icon">◈</div>
                <h3>Your interface preview will appear here</h3>
                <p>
                    Upload a website screenshot, a visual wireframe,
                    or switch to <strong>Website URL</strong> to audit a live page.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<​/div>", unsafe_allow_html=True)

with form_col:
    st.markdown(
        """
        <div class="side-panel">
            <div class="side-label">UX AUDIT SETUP</div>
            <div class="side-title">Prepare your audit</div>

            <div class="source-card">
                <div class="source-card-title">◈ Screenshot or wireframe</div>
                <div class="source-card-text">
                    Upload a PNG, JPG, JPEG or WEBP design for visual UX review.
                </div>
            </div>

            <div class="source-card">
                <div class="source-card-title">↗ Live website URL</div>
                <div class="source-card-text">
                    Add a public website URL for an automated page audit.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audit_name = st.text_input(
        "Audit name",
        placeholder="e.g. Nova Atelier — Homepage",
    )

    st.markdown(
        """
        <div class="ready-card">
            <div class="ready-title">No results yet</div>
            <div class="ready-text">
                Select a source and start an audit. Results will be shown here
                once an analysis engine is connected.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    can_start = (
        uploaded_file is not None
        or (website_url.strip() and valid_url(website_url))
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    if st.button(
        "Start UX audit",
        type="primary",
        use_container_width=True,
        disabled=not can_start,
    ):
        st.session_state.audit_requested = True
        st.session_state.audit_name = (
            audit_name.strip()
            or (
                uploaded_file.name
                if uploaded_file is not None
                else urlparse(website_url).netloc
            )
        )
        st.session_state.audit_source = (
            uploaded_file.name
            if uploaded_file is not None
            else website_url.strip()
        )

    if not can_start:
        st.caption("Add a screenshot or a valid website URL to continue.")

# ─────────────────────────────────────────────
# Confirmación de solicitud, sin resultados falsos
# ─────────────────────────────────────────────
if st.session_state.audit_requested:
    st.success(
        f"Audit request created: **{st.session_state.audit_name}**. "
        "The selected source is ready for processing."
    )

    with st.expander("Audit request details", expanded=False):
        st.write(f"**Project:** {st.session_state.audit_name}")
        st.write(f"**Source type:** {st.session_state.source_type}")
        st.write(f"**Source:** {st.session_state.audit_source}")
        st.caption(
            "This interface currently registers audit inputs only. "
            "Connect an analysis service to generate UX findings and scores."
        )
