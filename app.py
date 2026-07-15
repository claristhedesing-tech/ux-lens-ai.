"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""
import os
import streamlit as st

st.set_page_config(
    page_title="UX Lens AI",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #061426;
            color: #E9F2FF;
        }

        [data-testid="stSidebar"] {
            background-color: #050F1E;
            border-right: 1px solid #0F2540;
        }

        [data-testid="stSidebar"] > div:first-child {
            width: 72px;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }

        .breadcrumb {
            color: #7891AE;
            font-size: 12px;
            padding-top: 7px;
        }

        .breadcrumb b {
            color: #F5F9FF;
        }

        .section-label {
            color: #7891AE;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        .badge-blue {
            background: #0D2A4A;
            border: 1px solid #268CFF;
            border-radius: 4px;
            color: #268CFF;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 7px;
        }

        .result-card {
            background: #0A203A;
            border: 1px solid #1A3A5C;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        }

        .metric-box {
            background: #0A203A;
            border: 1px solid #173451;
            border-radius: 8px;
            min-height: 70px;
            padding: 10px;
            margin-bottom: 8px;
        }

        .finding-item {
            background: #0A203A;
            border: 1px solid #173451;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
        }

        .preview-empty {
            background: #040D1A;
            border: 1px dashed #2A4B6D;
            border-radius: 10px;
            color: #7891AE;
            min-height: 470px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    if os.path.exists("mountains.png"):
        st.image("mountains.png", width=38)
    else:
        st.markdown(
            """
            <div style="
                background:#1A3A5C;
                border-radius:8px;
                color:#F5F9FF;
                font-size:20px;
                height:38px;
                line-height:38px;
                text-align:center;
                width:38px;
            ">△</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center;color:#268CFF;font-size:20px;margin-bottom:22px;">◉</div>
        <div style="text-align:center;color:#4A6A8A;font-size:20px;margin-bottom:22px;">⊞</div>
        <div style="text-align:center;color:#4A6A8A;font-size:20px;margin-bottom:22px;">◫</div>
        <div style="text-align:center;color:#4A6A8A;font-size:20px;margin-bottom:22px;">≡</div>
        <div style="text-align:center;color:#4A6A8A;font-size:20px;margin-bottom:22px;">⚙</div>
        """,
        unsafe_allow_html=True,
    )

header_left, header_right = st.columns([3, 1.4])

with header_left:
    st.markdown(
        """
        <div class="breadcrumb">
            <b>UX LENS</b> &nbsp;›&nbsp; Projects
            &nbsp;›&nbsp; NOVA ATELIER Page Web
            &nbsp;›&nbsp; <b>Accessibility Audit</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    status_col, export_col, share_col = st.columns([1.8, 1, 1])

    with status_col:
        st.markdown(
            "<div style='color:#22C55E;font-size:11px;font-weight:700;padding-top:8px;'>● Scan complete</div>",
            unsafe_allow_html=True,
        )

    with export_col:
        st.button("Export", use_container_width=True)

    with share_col:
        st.button("Share", type="primary", use_container_width=True)

st.divider()

col_preview, col_results = st.columns([2.5, 1], gap="medium")

with col_preview:
    title_col, scan_col = st.columns([3, 1])

    with title_col:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:9px;padding-top:5px;">
                <span style="font-weight:800;font-size:15px;color:#F5F9FF;">
                    NOVA ATELIER — Homepage
                </span>
                <span class="badge-blue">LIVE AUDIT</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with scan_col:
        st.button("New Scan ↻", use_container_width=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload screenshot to analyze",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True)
    else:
        st.markdown(
            """
            <div class="preview-empty">
                <div>
                    <div style="font-size:32px;margin-bottom:10px;">◎</div>
                    <div style="font-weight:700;color:#A9BDD3;">
                        Upload an interface screenshot
                    </div>
                    <div style="font-size:12px;margin-top:5px;">
                        The visual preview will appear here.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_results:
    st.markdown(
        '<div class="section-label">UX AUDIT RESULTS</div>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Finova Mobile App")

    st.markdown(
        """
        <div class="result-card">
            <div style="display:flex;align-items:center;gap:14px;">
                <div style="
                    width:74px;
                    height:74px;
                    border:8px solid #F59E0B;
                    border-left-color:#1A3A5C;
                    border-radius:50%;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    box-sizing:border-box;
                ">
                    <div style="font-size:17px;font-weight:800;color:#F5F9FF;">78%</div>
                    <div style="font-size:10px;font-weight:800;color:#22C55E;">B</div>
                </div>
                <div>
                    <div style="font-size:14px;font-weight:800;color:#F5F9FF;">
                        Good foundation
                    </div>
                    <div style="font-size:11px;color:#7891AE;margin-top:4px;">
                        Accessibility needs attention
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_col_1, metric_col_2 = st.columns(2)

    with metric_col_1:
        st.markdown(
            """
            <div class="metric-box">
                <div class="section-label">ACCESSIBILITY</div>
                <div style="color:#EF4444;font-size:22px;font-weight:800;">62%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="metric-box">
                <div class="section-label">VISUAL CLARITY</div>
                <div style="color:#F59E0B;font-size:22px;font-weight:800;">81%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_col_2:
        st.markdown(
            """
            <div class="metric-box">
                <div class="section-label">USABILITY</div>
                <div style="color:#22C55E;font-size:22px;font-weight:800;">88%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="metric-box">
                <div class="section-label">PERFORMANCE</div>
                <div style="color:#22C55E;font-size:22px;font-weight:800;">90%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin:12px 0 8px 0;">
            <span style="font-size:13px;font-weight:800;color:#F5F9FF;">
                Actionable Insights
            </span>
            <span style="
                background:#0D2A4A;
                border:1px solid #268CFF;
                border-radius:10px;
                color:#268CFF;
                font-size:10px;
                font-weight:800;
                margin-left:6px;
                padding:2px 7px;
            ">2 items</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    findings = [
        (
            "Fix button contrast",
            "The View details button has a 2.6:1 contrast ratio. Increase it to at least 4.5:1.",
            "#EF4444",
            "HIGH",
        ),
        (
            "Increase touch target",
            "The Payments icon is too small for mobile interaction. Use at least 44 × 44 px.",
            "#F59E0B",
            "MEDIUM",
        ),
    ]

    for title, description, color, severity in findings:
        st.markdown(
            f"""
            <div class="finding-item">
                <div style="display:flex;gap:9px;">
                    <div style="color:{color};font-size:14px;">●</div>
                    <div>
                        <div style="font-size:12px;font-weight:800;color:#F5F9FF;">
                            {title}
                        </div>
                        <div style="font-size:11px;color:#7891AE;margin:4px 0 7px 0;">
                            {description}
                        </div>
                        <span style="
                            border:1px solid {color};
                            border-radius:10px;
                            color:{color};
                            font-size:9px;
                            font-weight:800;
                            padding:2px 6px;
                        ">{severity}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("⏱ Last scan: Today, 9:41 AM")
    st.button("View Full Audit Report", use_container_width=True)
    st.button("Apply Safe Fixes", type="primary", use_container_width=True)
