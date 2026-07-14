import io

import requests
import streamlit as st
from PIL import Image

from contrast_checker import audit_element


st.set_page_config(
    page_title="UX Lens AI",
    page_icon="🔍",
    layout="wide",
)


def load_image_from_url(image_url):
    """Download a public image from a direct image URL."""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except requests.RequestException:
        return None
    except Image.UnidentifiedImageError:
        return None


def severity_color(severity):
    """Return the UX Lens color associated with an issue severity."""
    colors = {
        "HIGH": "#EF4444",
        "MEDIUM": "#F59E0B",
        "LOW": "#22C55E",
    }
    return colors.get(severity, "#38BDF8")


def severity_icon(severity):
    """Return a simple icon for each UX Lens severity."""
    icons = {
        "HIGH": "●",
        "MEDIUM": "●",
        "LOW": "✓",
    }
    return icons.get(severity, "•")


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
    Generate a prototype UX audit.

    Contrast results are calculated from the user's selected colors.
    Other findings demonstrate how UX Lens could group visual,
    accessibility, and usability insights in a complete audit.
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
                "Data marks should remain visible when viewed on "
                "low-quality displays or in bright environments."
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
                    "title": f"Fix contrast in {contrast_result['element']}",
                    "description": (
                        f"This element has a {ratio}:1 contrast ratio. "
                        "Increase the ratio to at least 4.5:1 for "
                        "normal text."
                    ),
                    "severity": severity,
                },
            )
        else:
            findings.append(
                {
                    "title": f"Contrast passes in {contrast_result['element']}",
                    "description": (
                        f"This element reaches a {ratio}:1 contrast ratio "
                        "and meets its WCAG requirement."
                    ),
                    "severity": "LOW",
                },
            )

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: severity_order[item["severity"]])

    return findings


def score_from_findings(findings):
    """Create a prototype overall UX score from issue severities."""
    penalties = {
        "HIGH": 10,
        "MEDIUM": 5,
        "LOW": 0,
    }

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
            <div class="finding-icon" style="color: {color};">
                {icon}
            </div>
            <div class="finding-content">
                <div class="finding-title">{finding["title"]}</div>
                <div class="finding-description">
                    {finding["description"]}
                </div>
                <span class="severity-chip"
                    style="background-color: {color}22; color: {color};
                    border: 1px solid {color}55;">
                    {finding["severity"]}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
        .stApp {
            background: #061426;
            color: #E9F2FF;
        }

        [data-testid="stHeader"] {
            background: #061426;
        }

        [data-testid="stSidebar"] {
            background: #081B33;
            border-right: 1px solid #173451;
        }

        h1, h2, h3 {
            color: #F5F9FF !important;
        }

        .topbar {
            padding: 5px 0 16px 0;
            border-bottom: 1px solid #173451;
            margin-bottom: 18px;
        }

        .brand {
            color: #F5F9FF;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }

        .breadcrumb {
            color: #7791AE;
            font-size: 12px;
            padding-top: 5px;
        }

        .section-label {
            color: #7E98B8;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .workspace-card {
            background: #071B32;
            border: 1px solid #173451;
            border-radius: 10px;
            padding: 18px;
            min-height: 560px;
        }

        .empty-preview {
            min-height: 445px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            border: 1px dashed #2A4B6D;
            border-radius: 8px;
            color: #7891AE;
            padding: 35px;
            background: #061629;
        }

        .score-card {
            background: #0A203A;
            border: 1px solid #1A4265;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }

        .score-number {
            color: #F5F9FF;
            font-size: 35px;
            font-weight: 800;
            line-height: 1;
        }

        .grade {
            display: inline-block;
            color: #061426;
            background: #22C55E;
            border-radius: 6px;
            padding: 4px 8px;
            margin-left: 8px;
            font-weight: 800;
            font-size: 12px;
        }

        .metric-card {
            background: #0A203A;
            border: 1px solid #173451;
            border-radius: 8px;
            padding: 11px;
            min-height: 92px;
        }

        .metric-title {
            color: #7891AE;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.7px;
        }

        .metric-value {
            font-size: 22px;
            font-weight: 800;
            padding-top: 5px;
        }

        .finding-card {
            display: flex;
            gap: 10px;
            background: #0A203A;
            border: 1px solid #173451;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
        }

        .finding-icon {
            font-size: 16px;
            line-height: 18px;
        }

        .finding-content {
            flex: 1;
        }

        .finding-title {
            color: #E9F2FF;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .finding-description {
            color: #7891AE;
            font-size: 10px;
            line-height: 1.45;
            margin-bottom: 8px;
        }

        .severity-chip {
            border-radius: 999px;
            font-size: 9px;
            font-weight: 800;
            padding: 3px 7px;
        }

        .footer-note {
            color: #6F88A5;
            font-size: 11px;
            padding-top: 14px;
        }

        .stButton > button {
            border-radius: 7px;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Sidebar
with st.sidebar:
    st.markdown("## 🔍 UX LENS")
    st.caption("AI-assisted design review")

    st.divider()

    st.markdown("**Projects**")
    st.caption("▦  Dashboard")
    st.caption("▱  Projects")
    st.caption("◉  Live audit")
    st.caption("▤  Reports")
    st.caption("⚙  Settings")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.success("AI engine online")


# Header
header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">UX LENS</div>
            <div class="breadcrumb">
                Projects &nbsp;›&nbsp; New audit &nbsp;›&nbsp; Accessibility Audit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.write("")
    st.write("")
    st.button("Share", use_container_width=True)


# Input controls
st.markdown("### Start a UX audit")

input_left, input_right, input_action = st.columns([2, 2, 1])

with input_left:
    project_name = st.text_input(
        "Project name",
        value="New interface audit",
        placeholder="Example: Finova Mobile App",
    )

with input_right:
    website_url = st.text_input(
        "Website or Figma prototype URL",
        placeholder="https://your-website.com",
        help=(
            "Use this field to identify the website or prototype "
            "being audited."
        ),
    )

with input_action:
    st.write("")
    st.write("")
    run_audit = st.button(
        "Run audit",
        type="primary",
        use_container_width=True,
    )


source_left, source_right = st.columns(2)

with source_left:
    screenshot_file = st.file_uploader(
        "Upload a web or app screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a screenshot of the page or application you want to audit.",
    )

with source_right:
    image_url = st.text_input(
        "Or paste a direct image URL",
        placeholder="https://example.com/screenshot.png",
        help=(
            "This must be a public direct image link ending in "
            ".png, .jpg, .jpeg, or .webp."
        ),
    )


uploaded_image = None

if screenshot_file is not None:
    uploaded_image = Image.open(screenshot_file)

elif image_url:
    uploaded_image = load_image_from_url(image_url)
    if uploaded_image is None:
        st.warning(
            "The image could not be loaded. Use a public direct image URL "
            "or upload a screenshot instead."
        )


st.divider()

# Contrast checker
with st.expander("Optional: check a specific text contrast pair"):
    contrast_left, contrast_middle, contrast_right = st.columns([2, 2, 1])

    with contrast_left:
        element_name = st.text_input(
            "Element name",
            value="Primary button",
        )
        text_color = st.color_picker(
            "Text color",
            value="#FFFFFF",
        )

    with contrast_middle:
        background_color = st.color_picker(
            "Background color",
            value="#7EC8E3",
        )
        large_text = st.checkbox(
            "Large text",
            help="WCAG large text is at least 18 pt or 14 pt bold.",
        )

    with contrast_right:
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


if "contrast_result" not in st.session_state:
    st.session_state["contrast_result"] = None


if run_audit:
    st.session_state["audit_has_run"] = True


if "audit_has_run" not in st.session_state:
    st.session_state["audit_has_run"] = False


# Main audit workspace
workspace, audit_panel = st.columns([3.25, 1])

with workspace:
    st.markdown(
        f"""
        <div class="section-label">LIVE AUDIT</div>
        <h3>{project_name} — Interface preview</h3>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption=website_url if website_url else "Uploaded interface screenshot",
                use_container_width=True,
            )
        else:
            st.markdown(
                """
                <div class="empty-preview">
                    <div>
                        <h3 style="color: #C7D9ED;">
                            Add an interface to begin
                        </h3>
                        <p>
                            Paste a website URL as project context, then upload
                            a screenshot or add a public direct image URL.<br><br>
                            UX Lens will display the interface here and generate
                            a prioritized prototype audit.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if website_url:
        st.caption(f"Reference URL: {website_url}")


with audit_panel:
    st.markdown('<div class="section-label">UX AUDIT RESULTS</div>', unsafe_allow_html=True)
    st.markdown(f"#### {project_name}")

    if st.session_state["audit_has_run"]:
        findings = build_audit_results(st.session_state["contrast_result"])
        overall_score = score_from_findings(findings)
        grade = calculate_grade(overall_score)

        st.markdown(
            f"""
            <div class="score-card">
                <div class="metric-title">OVERALL SCORE</div>
                <div style="padding-top: 9px;">
                    <span class="score-number">{overall_score}%</span>
                    <span class="grade">{grade}</span>
                </div>
                <div style="color: #7891AE; font-size: 11px; padding-top: 9px;">
                    Prototype score based on identified UX findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        metric_one, metric_two = st.columns(2)

        with metric_one:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">ACCESSIBILITY</div>
                    <div class="metric-value" style="color: #F59E0B;">72%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric_two:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">USABILITY</div>
                    <div class="metric-value" style="color: #22C55E;">86%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        visual_metric, performance_metric = st.columns(2)

        with visual_metric:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">VISUAL CLARITY</div>
                    <div class="metric-value" style="color: #F59E0B;">78%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with performance_metric:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-title">PERFORMANCE</div>
                    <div class="metric-value" style="color: #22C55E;">90%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown(
            f"**Actionable Insights** &nbsp; ` {len(findings)} items `"
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
            "Add a screenshot or image URL, then select **Run audit** "
            "to generate the UX Lens report."
        )

st.markdown(
    """
    <div class="footer-note">
        UX Lens AI prototype · Contrast calculations follow WCAG 2.1
        requirements. Full visual findings are prototype heuristics and
        should be reviewed by a UX/UI designer.
    </div>
    """,
    unsafe_allow_html=True,
)
