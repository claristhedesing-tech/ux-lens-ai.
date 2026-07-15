"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""

import io

import requests
import streamlit as st
from PIL import Image

from contrast_checker import audit_element


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="UX Lens AI",
    page_icon="assets/Logo-UX-Lens.png",
    layout="wide",
)


# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────

def load_image_from_url(image_url):
    """Download a public image from a direct image URL."""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except (requests.RequestException, Image.UnidentifiedImageError):
        return None


def severity_color(severity):
    """Return the UX Lens color for a given severity level."""
    return {
        "HIGH": "#EF4444",
        "MEDIUM": "#F59E0B",
        "LOW": "#22C55E",
    }.get(severity, "#38BDF8")


def severity_icon(severity):
    """Return a simple icon for each severity level."""
    return {
        "HIGH": "●",
        "MEDIUM": "●",
        "LOW": "✓",
    }.get(severity, "•")


def calculate_grade(score):
    """Convert a numeric score into a UX Lens letter grade."""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def build_audit_results(contrast_result=None):
    """
    Generate a prototype UX audit finding list.

    Contrast results are calculated from the user's selected colors.
    Other findings demonstrate how UX Lens groups visual,
    accessibility, and usability insights.
    """
    findings = [
        {
            "title": "Improve secondary text readability",
            "description": (
                "Secondary labels may be difficult to read against "
                "light or image-based backgrounds."
            ),
            "severity": "HIGH",
        },
        {
            "title": "Increase touch target size",
            "description": (
                "Some actions appear compact. Mobile touch targets "
                "should be at least 44 × 44 px."
            ),
            "severity": "MEDIUM",
        },
        {
            "title": "Strengthen chart contrast",
            "description": (
                "Data marks should remain visible on low-quality "
                "displays or in bright environments."
            ),
            "severity": "MEDIUM",
        },
        {
            "title": "Navigation structure is clear",
            "description": (
                "The main navigation follows a consistent and "
                "recognizable layout pattern."
            ),
            "severity": "LOW",
        },
    ]

    if contrast_result:
        ratio = contrast_result["contrast_ratio"]
        status = contrast_result["status"]
        severity = contrast_result["severity"]

        if status == "FAIL":
            findings.insert(
                0,
                {
                    "title": (
                        f"Fix contrast in {contrast_result['element']}"
                    ),
                    "description": (
                        f"This element has a {ratio}:1 contrast ratio. "
                        "Increase it to at least 4.5:1 for normal text."
                    ),
                    "severity": severity,
                },
            )
        else:
            findings.append(
                {
                    "title": (
                        f"Contrast passes in {contrast_result['element']}"
                    ),
                    "description": (
                        f"This element reaches {ratio}:1 and meets "
                        "its WCAG requirement."
                    ),
                    "severity": "LOW",
                },
            )

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: severity_order[item["severity"]])
    return findings


def score_from_findings(findings):
    """Calculate a prototype overall UX score from issue severities."""
    penalties = {"HIGH": 10, "MEDIUM": 5, "LOW": 0}
    score = 100
    for finding in findings:
        score -= penalties[finding["severity"]]
    return max(score, 0)


def render_finding(finding):
    """Render one actionable-insight card."""
    color = severity_color(finding["severity"])
    icon = severity_icon(finding["severity"])

    st.markdown(
        f"""
        <div class="finding-card">
            <div class="finding-icon" style="color:{color};">{icon}</div>
            <div class="finding-content">
                <div class="finding-title">{finding["title"]}</div>
                <div class="finding-description">
                    {finding["description"]}
                </div>
                <span class="severity-chip"
                    style="background:{color}22;color:{color};
                    border:1px solid {color}55;">
                    {finding["severity"]}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# Global styles
# ─────────────────────────────────────────────

st.markdown(
    """
    <style>
        .stApp { background:#061426; color:#E9F2FF; }

        [data-testid="stHeader"] { background:#061426; }

        [data-testid="stSidebar"] {
            background:#081B33;
            border-right:1px solid #173451;
        }

        h1,h2,h3 { color:#F5F9FF !important; }

        /* Setup card */
        .setup-card {
            background:#071B32;
            border:1px solid #173451;
            border-radius:12px;
            padding:24px 28px;
            margin-bottom:20px;
        }

        .setup-step {
            color:#7E98B8;
            font-size:10px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:6px;
            margin-top:18px;
        }

        /* Preview area */
        .workspace-card {
            background:#071B32;
            border:1px solid #173451;
            border-radius:10px;
            padding:18px;
        }

        .empty-preview {
            min-height:420px;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            border:1px dashed #2A4B6D;
            border-radius:8px;
            color:#7891AE;
            padding:35px;
            background:#061629;
        }

        /* Score card */
        .score-card {
            background:#0A203A;
            border:1px solid #1A4265;
            border-radius:10px;
            padding:16px;
            margin-bottom:12px;
        }

        .score-number {
            color:#F5F9FF;
            font-size:35px;
            font-weight:800;
            line-height:1;
        }

        .grade {
            display:inline-block;
            color:#061426;
            background:#22C55E;
            border-radius:6px;
            padding:4px 8px;
            margin-left:8px;
            font-weight:800;
            font-size:12px;
        }

        /* Metric cards */
        .metric-card {
            background:#0A203A;
            border:1px solid #173451;
            border-radius:8px;
            padding:11px;
            min-height:80px;
            margin-bottom:8px;
        }

        .metric-title {
            color:#7891AE;
            font-size:9px;
            font-weight:800;
            letter-spacing:0.7px;
        }

        .metric-value {
            font-size:22px;
            font-weight:800;
            padding-top:5px;
        }

        /* Finding cards */
        .finding-card {
            display:flex;
            gap:10px;
            background:#0A203A;
            border:1px solid #173451;
            border-radius:8px;
            padding:12px;
            margin-bottom:8px;
        }

        .finding-icon { font-size:16px; line-height:18px; }

        .finding-content { flex:1; }

        .finding-title {
            color:#E9F2FF;
            font-size:12px;
            font-weight:700;
            margin-bottom:4px;
        }

        .finding-description {
            color:#7891AE;
            font-size:10px;
            line-height:1.45;
            margin-bottom:8px;
        }

        .severity-chip {
            border-radius:999px;
            font-size:9px;
            font-weight:800;
            padding:3px 7px;
        }

        /* Buttons */
        .stButton > button {
            border-radius:7px;
            font-weight:700;
        }

        .stButton > button[kind="primary"] {
            background:#268CFF;
            border:1px solid #3C9BFF;
            color:#FFFFFF;
            min-height:44px;
        }

        .stButton > button[kind="primary"]:hover {
            background:#1678E8;
            border-color:#58ACFF;
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            background:#061629;
            border:1px dashed #2A4B6D;
            border-radius:8px;
            padding:10px;
        }

        .footer-note {
            color:#6F88A5;
            font-size:11px;
            padding-top:14px;
        }

        .section-label {
            color:#7E98B8;
            font-size:10px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:6px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:
    st.image("assets/Logo-UX-Lens.png", width=48)
    st.markdown("## UX LENS")
    st.caption("AI-assisted design review")
    st.divider()
    st.markdown("**Navigation**")
    st.caption("▦  Dashboard")
    st.caption("▱  Projects")
    st.caption("◉  Live audit")
    st.caption("▤  Reports")
    st.caption("⚙  Settings")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.success("AI engine online")


# ─────────────────────────────────────────────
# Top bar
# ─────────────────────────────────────────────

top_left, top_right = st.columns([4, 1])

with top_left:
    st.markdown(
        """
        <div style="padding:5px 0 16px 0;
                    border-bottom:1px solid #173451;
                    margin-bottom:18px;">
            <div style="color:#F5F9FF;font-size:19px;
                        font-weight:800;letter-spacing:0.5px;">
                UX LENS
            </div>
            <div style="color:#7791AE;font-size:12px;padding-top:5px;">
                Projects &nbsp;›&nbsp; New audit
                &nbsp;›&nbsp; Accessibility Audit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.write("")
    st.write("")
    st.button("Share", use_container_width=True)


# ─────────────────────────────────────────────
# Audit setup card
# ─────────────────────────────────────────────

st.markdown("### Create a new audit")
st.caption(
    "Add a screenshot or link to the interface you want "
    "UX Lens to review."
)

with st.container(border=True):

    project_name = st.text_input(
        "Project name",
        value="New Audit",
        placeholder="Example: Nova Atelier checkout",
    )

    st.markdown(
        '<div class="setup-step">STEP 1 — CHOOSE YOUR AUDIT SOURCE</div>',
        unsafe_allow_html=True,
    )

    audit_source = st.radio(
        "Audit source",
        options=[
            "Upload screenshot",
            "Paste image URL",
            "Website or Figma URL",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

    website_url = ""
    image_url = ""
    screenshot_file = None

    if audit_source == "Upload screenshot":
        screenshot_file = st.file_uploader(
            "Upload a website or app screenshot",
            type=["png", "jpg", "jpeg", "webp"],
            help="Accepted formats: PNG, JPG, JPEG, WEBP.",
        )
        st.caption(
            "Best option for visual, hierarchy, accessibility, "
            "and contrast analysis."
        )

    elif audit_source == "Paste image URL":
        image_url = st.text_input(
            "Public direct image URL",
            placeholder="https://example.com/screenshot.png",
            help=(
                "Use a direct public URL ending in "
                ".png, .jpg, .jpeg, or .webp."
            ),
        )
        st.caption(
            "Paste a direct link to a screenshot hosted online."
        )

    else:
        website_url = st.text_input(
            "Website or Figma prototype URL",
            placeholder="https://your-website.com",
            help=(
                "This URL identifies the project. For visual auditing, "
                "also upload a screenshot when possible."
            ),
        )
        screenshot_file = st.file_uploader(
            "Optional: upload a screenshot for visual analysis",
            type=["png", "jpg", "jpeg", "webp"],
        )

    st.markdown(
        '<div class="setup-step">STEP 2 — RUN THE ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    run_audit = st.button(
        "Run full UX audit",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "UX Lens will review visual clarity, hierarchy, "
        "accessibility, and contrast."
    )


# ─────────────────────────────────────────────
# Resolve uploaded image
# ─────────────────────────────────────────────

uploaded_image = None

if screenshot_file is not None:
    uploaded_image = Image.open(screenshot_file)
elif image_url:
    uploaded_image = load_image_from_url(image_url)
    if uploaded_image is None:
        st.warning(
            "The image could not be loaded. Use a public direct "
            "image URL or upload a screenshot instead."
        )


# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────

if "contrast_result" not in st.session_state:
    st.session_state["contrast_result"] = None

if run_audit:
    st.session_state["audit_has_run"] = True

if "audit_has_run" not in st.session_state:
    st.session_state["audit_has_run"] = False


# ─────────────────────────────────────────────
# Main workspace
# ─────────────────────────────────────────────

st.divider()

workspace, audit_panel = st.columns([3.25, 1])

with workspace:
    st.markdown(
        '<div class="section-label">LIVE AUDIT</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"### {project_name} — Interface preview")

    with st.container(border=True):
        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption=(
                    website_url
                    if website_url
                    else "Uploaded interface screenshot"
                ),
                use_container_width=True,
            )
        else:
            st.markdown(
                """
                <div class="empty-preview">
                    <div>
                        <h3 style="color:#C7D9ED;">
                            Add an interface to begin
                        </h3>
                        <p>
                            Choose an audit source above, add your
                            design, and select
                            <strong>Run full UX audit</strong>.<br><br>
                            UX Lens will display the interface here
                            and generate a prioritized report.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if website_url:
        st.caption(f"Reference URL: {website_url}")


with audit_panel:
    st.markdown(
        '<div class="section-label">UX AUDIT RESULTS</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"#### {project_name}")

    if st.session_state["audit_has_run"]:
        findings = build_audit_results(
            st.session_state["contrast_result"]
        )
        overall_score = score_from_findings(findings)
        grade = calculate_grade(overall_score)

        st.markdown(
            f"""
            <div class="score-card">
                <div class="metric-title">OVERALL SCORE</div>
                <div style="padding-top:9px;">
                    <span class="score-number">{overall_score}%</span>
                    <span class="grade">{grade}</span>
                </div>
                <div style="color:#7891AE;font-size:11px;
                            padding-top:9px;">
                    Prototype score based on identified UX findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">ACCESSIBILITY</div>
                    <div class="metric-value"
                        style="color:#F59E0B;">72%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_b:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">USABILITY</div>
                    <div class="metric-value"
                        style="color:#22C55E;">86%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_c, col_d = st.columns(2)

        with col_c:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">VISUAL CLARITY</div>
                    <div class="metric-value"
                        style="color:#F59E0B;">78%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_d:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">PERFORMANCE</div>
                    <div class="metric-value"
                        style="color:#22C55E;">90%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown(
            f"**Actionable Insights** &nbsp; `{len(findings)} items`"
        )

        for finding in findings:
            render_finding(finding)

        st.button("View full report", use_container_width=True)
        st.button(
            "Apply safe fixes",
            type="primary",
            use_container_width=True,
        )

    else:
        st.info(
            "Add a screenshot or image URL above, then select "
            "**Run full UX audit** to generate the report."
        )


# ─────────────────────────────────────────────
# Advanced: contrast checker
# ─────────────────────────────────────────────

st.divider()

with st.expander(
    "Advanced tool: check a specific color contrast pair"
):
    adv_left, adv_middle, adv_right = st.columns([2, 2, 1])

    with adv_left:
        element_name = st.text_input(
            "Element name",
            value="Primary button",
        )
        text_color = st.color_picker(
            "Text color",
            value="#FFFFFF",
        )

    with adv_middle:
        background_color = st.color_picker(
            "Background color",
            value="#7EC8E3",
        )
        large_text = st.checkbox(
            "Large text",
            help="WCAG large text is at least 18 pt or 14 pt bold.",
        )

    with adv_right:
        st.write("")
        st.write("")
        check_contrast = st.button(
            "Check contrast",
            use_container_width=True,
        )

    if check_contrast:
        st.session_state["contrast_result"] = audit_element(
            element_name,
            text_color,
            background_color,
            large_text,
        )

    if st.session_state["contrast_result"]:
        result = st.session_state["contrast_result"]
        ratio = result["contrast_ratio"]
        color = severity_color(result["severity"])

        st.markdown(
            f"""
            <div class="score-card" style="margin-top:14px;">
                <div class="metric-title">CONTRAST RESULT</div>
                <div style="padding-top:8px;">
                    <span class="score-number">{ratio}:1</span>
                    <span class="grade"
                        style="background:{color};">
                        {result["severity"]}
                    </span>
                </div>
                <div style="color:#7891AE;font-size:11px;
                            padding-top:8px;">
                    WCAG level: {result["wcag_level"]}
                    &nbsp;·&nbsp; {result["status"]}
                    &nbsp;·&nbsp; {result["text_type"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result["status"] == "PASS":
            st.success(result["action"])
        else:
            st.error(result["action"])


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

st.markdown(
    """
    <div class="footer-note">
        UX Lens AI prototype · Contrast calculations follow WCAG 2.1
        requirements. Full visual findings are prototype heuristics
        and should be reviewed by a UX/UI designer.
    </div>
    """,
    unsafe_allow_html=True,
)
