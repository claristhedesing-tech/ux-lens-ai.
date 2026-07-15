"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""

import io
import math

import requests
import streamlit as st
from PIL import Image


LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAYAAAB/HSuDAAAQAElEQVR4Aey9B6AsW1XnvXdVdZ9z78OMo5IUVCQIiCKOwMBIkAwSZUCCBHlkeOQHSE4PUHIcMgoSVAYB4yh+4xjGMIzOKEbEMDPfzHwOyLv3dHdV7e+/9jnVt8+5nU7Hqupfn1q9d+241m9X2HtVd5/E8YIABCAAAQhAAAIQgAAEIAABCECg7QQcDoDWDzEGQgACEIAABCAAAQhAAAIQgAAEHA4ADgIIQAACEIAABCAAAQhAAAIQgEDrCchAPgEgCGwQgAAEIAABCEAAAhCAAAQgAIE2EzDbcAAYBQQCEIAABCAAAQhAAAIQgAAEINBeAtEyHAARA28QgAAEIAABCEAAAhCAAAQgAIG2Eji
...

Longitud total del base64: 115632 caracteres
✅ Base64 generated correctly

# ─────────────────────────────────────────────
# Contrast logic (self-contained)
# ─────────────────────────────────────────────

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(hex1, hex2):
    lum1 = relative_luminance(hex_to_rgb(hex1))
    lum2 = relative_luminance(hex_to_rgb(hex2))
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def audit_element(name, text_hex, bg_hex, large_text=False):
    ratio = round(contrast_ratio(text_hex, bg_hex), 2)
    required = 3.0 if large_text else 4.5
    status = "PASS" if ratio >= required else "FAIL"
    severity = "LOW" if status == "PASS" else "HIGH"
    wcag = "AAA" if ratio >= 7 else ("AA" if ratio >= required else "Fail")
    action = (
        f"{name} passes WCAG contrast requirements."
        if status == "PASS"
        else f"Increase contrast for {name} to at least {required}:1."
    )
    return {
        "element": name,
        "contrast_ratio": ratio,
        "status": status,
        "severity": severity,
        "wcag_level": wcag,
        "text_type": "Large text" if large_text else "Normal text",
        "action": action,
    }


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def load_image_from_url(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except Exception:
        return None


def severity_color(severity):
    return {"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#22C55E"}.get(
        severity, "#38BDF8"
    )


def severity_icon(severity):
    return {"HIGH": "●", "MEDIUM": "●", "LOW": "✓"}.get(severity, "•")


def calculate_grade(score):
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def build_audit_results(contrast_result=None):
    findings = [
        {
            "title": "Improve secondary text readability",
            "description": "Secondary labels may be difficult to read against light or image-based backgrounds.",
            "severity": "HIGH",
        },
        {
            "title": "Increase touch target size",
            "description": "Some actions appear compact. Mobile touch targets should be at least 44 × 44 px.",
            "severity": "MEDIUM",
        },
        {
            "title": "Strengthen chart contrast",
            "description": "Data marks should remain visible on low-quality displays or in bright environments.",
            "severity": "MEDIUM",
        },
        {
            "title": "Navigation structure is clear",
            "description": "The main navigation follows a consistent and recognizable layout pattern.",
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
                    "description": f"This element has a {ratio}:1 contrast ratio. Increase it to at least 4.5:1 for normal text.",
                    "severity": severity,
                },
            )
        else:
            findings.append(
                {
                    "title": f"Contrast passes in {contrast_result['element']}",
                    "description": f"This element reaches {ratio}:1 and meets its WCAG requirement.",
                    "severity": "LOW",
                },
            )

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: severity_order[item["severity"]])
    return findings


def score_from_findings(findings):
    penalties = {"HIGH": 10, "MEDIUM": 5, "LOW": 0}
    score = 100 - sum(penalties[f["severity"]] for f in findings)
    return max(score, 0)


def render_finding(finding):
    color = severity_color(finding["severity"])
    icon = severity_icon(finding["severity"])
    st.markdown(
        f"""
        <div class="finding-card">
            <div class="finding-icon" style="color:{color};">{icon}</div>
            <div class="finding-content">
                <div class="finding-title">{finding["title"]}</div>
                <div class="finding-description">{finding["description"]}</div>
                <span class="severity-chip" style="background:{color}22;color:{color};border:1px solid {color}55;">
                    {finding["severity"]}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="UX Lens AI",
    page_icon="🔵",
    layout="wide",
)


# ─────────────────────────────────────────────
# Styles — BUTTONS FIXED
# ─────────────────────────────────────────────

st.markdown(
    """
    <style>
        .stApp { background:#061426; color:#E9F2FF; }
        [data-testid="stHeader"] { background:#061426; }
        [data-testid="stSidebar"] { background:#081B33; border-right:1px solid #173451; }
        h1,h2,h3 { color:#F5F9FF !important; }

        /* ── Buttons (ALL types) ── */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 700 !important;
            min-height: 40px !important;
            border: 1px solid #2A4B6D !important;
            color: #E9F2FF !important;
            background: #0A203A !important;
            box-shadow: none !important;
        }

        /* Primary (Run audit, Apply safe fixes) */
        .stButton > button[kind="primary"] {
            background: #268CFF !important;
            border: 1px solid #3C9BFF !important;
            color: #FFFFFF !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: #1678E8 !important;
            border-color: #58ACFF !important;
        }

        /* Secondary / default (Share, View full report) */
        .stButton > button:hover {
            background: #122B4A !important;
            border-color: #3C9BFF !important;
            color: #F5F9FF !important;
        }

        /* Active / clicked state */
        .stButton > button:active {
            background: #0D1F36 !important;
            border-color: #268CFF !important;
        }

        /* Focus ring */
        .stButton > button:focus {
            outline: 2px solid #268CFF !important;
            outline-offset: 2px !important;
        }

        .setup-card { background:#071B32; border:1px solid #173451; border-radius:12px; padding:24px 28px; margin-bottom:20px; }
        .setup-step { color:#7E98B8; font-size:10px; font-weight:800; letter-spacing:1px; margin-bottom:6px; margin-top:18px; }
        .workspace-card { background:#071B32; border:1px solid #173451; border-radius:10px; padding:18px; }
        .empty-preview { min-height:420px; display:flex; align-items:center; justify-content:center; text-align:center; border:1px dashed #2A4B6D; border-radius:8px; color:#7891AE; padding:35px; background:#061629; }

        .score-card { background:#0A203A; border:1px solid #1A4265; border-radius:10px; padding:16px; margin-bottom:12px; }
        .score-number { color:#F5F9FF; font-size:35px; font-weight:800; line-height:1; }
        .grade { display:inline-block; color:#061426; background:#22C55E; border-radius:6px; padding:4px 8px; margin-left:8px; font-weight:800; font-size:12px; }

        .metric-card { background:#0A203A; border:1px solid #173451; border-radius:8px; padding:11px; min-height:80px; margin-bottom:8px; }
        .metric-title { color:#7891AE; font-size:9px; font-weight:800; letter-spacing:0.7px; }
        .metric-value { font-size:22px; font-weight:800; padding-top:5px; }

        .finding-card { display:flex; gap:10px; background:#0A203A; border:1px solid #173451; border-radius:8px; padding:12px; margin-bottom:8px; }
        .finding-icon { font-size:16px; line-height:18px; }
        .finding-content { flex:1; }
        .finding-title { color:#E9F2FF; font-size:12px; font-weight:700; margin-bottom:4px; }
        .finding-description { color:#7891AE; font-size:10px; line-height:1.45; margin-bottom:8px; }
        .severity-chip { border-radius:999px; font-size:9px; font-weight:800; padding:3px 7px; }

        [data-testid="stFileUploader"] { background:#061629; border:1px dashed #2A4B6D; border-radius:8px; padding:10px; }
        .footer-note { color:#6F88A5; font-size:11px; padding-top:14px; }
        .section-label { color:#7E98B8; font-size:10px; font-weight:800; letter-spacing:1px; margin-bottom:6px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;padding-bottom:8px;">
            <img src="data:image/png;base64,{LOGO_B64}" width="40" style="border-radius:8px;"/>
            <span style="color:#F5F9FF;font-size:18px;font-weight:800;letter-spacing:0.5px;">
                UX LENS
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
# Header
# ─────────────────────────────────────────────

top_left, top_right = st.columns([4, 1])

with top_left:
    st.markdown(
        """
        <div style="padding:5px 0 16px 0; border-bottom:1px solid #173451; margin-bottom:18px;">
            <div style="color:#F5F9FF;font-size:19px;font-weight:800;letter-spacing:0.5px;">
                UX LENS
            </div>
            <div style="color:#7791AE;font-size:12px;padding-top:5px;">
                Projects &nbsp;›&nbsp; New audit &nbsp;›&nbsp; Accessibility Audit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.write("")
    st.write("")
    if st.button("Share", use_container_width=True, key="btn_share"):
        st.toast("Share link copied to clipboard (prototype).", icon="🔗")


# ─────────────────────────────────────────────
# Audit setup
# ─────────────────────────────────────────────

st.markdown("### Create a new audit")
st.caption("Add a screenshot or link to the interface you want UX Lens to review.")

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
        options=["Upload screenshot", "Paste image URL", "Website or Figma URL"],
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
            "Best option for visual, hierarchy, accessibility, and contrast analysis."
        )

    elif audit_source == "Paste image URL":
        image_url = st.text_input(
            "Public direct image URL",
            placeholder="https://example.com/screenshot.png",
            help="Use a direct public URL ending in .png, .jpg, .jpeg, or .webp.",
        )
        st.caption("Paste a direct link to a screenshot hosted online.")

    else:
        website_url = st.text_input(
            "Website or Figma prototype URL",
            placeholder="https://your-website.com",
            help="This URL identifies the project. For visual auditing, also upload a screenshot when possible.",
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
        key="btn_run_audit",
    )

    st.caption("UX Lens will review visual clarity, hierarchy, accessibility, and contrast.")


# ─────────────────────────────────────────────
# Load image
# ─────────────────────────────────────────────

uploaded_image = None

if screenshot_file is not None:
    uploaded_image = Image.open(screenshot_file)
elif image_url:
    uploaded_image = load_image_from_url(image_url)
    if uploaded_image is None:
        st.warning(
            "The image could not be loaded. Use a public direct image URL or upload a screenshot instead."
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
    st.markdown('<div class="section-label">LIVE AUDIT</div>', unsafe_allow_html=True)
    st.markdown(f"### {project_name} — Interface preview")

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
                        <h3 style="color:#C7D9ED;">Add an interface to begin</h3>
                        <p>
                            Choose an audit source above, add your design, and select <strong>Run full UX audit</strong>.<br><br>
                            UX Lens will display the interface here and generate a prioritized report.
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
                <div style="padding-top:9px;">
                    <span class="score-number">{overall_score}%</span>
                    <span class="grade">{grade}</span>
                </div>
                <div style="color:#7891AE;font-size:11px;padding-top:9px;">
                    Prototype score based on identified UX findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                '<div class="metric-card"><div class="metric-title">ACCESSIBILITY</div><div class="metric-value" style="color:#F59E0B;">72%</div></div>',
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                '<div class="metric-card"><div class="metric-title">USABILITY</div><div class="metric-value" style="color:#22C55E;">86%</div></div>',
                unsafe_allow_html=True,
            )

        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown(
                '<div class="metric-card"><div class="metric-title">VISUAL CLARITY</div><div class="metric-value" style="color:#F59E0B;">78%</div></div>',
                unsafe_allow_html=True,
            )
        with col_d:
            st.markdown(
                '<div class="metric-card"><div class="metric-title">PERFORMANCE</div><div class="metric-value" style="color:#22C55E;">90%</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown(f"**Actionable Insights** &nbsp; `{len(findings)} items`")

        for finding in findings:
            render_finding(finding)

        if st.button("View full report", use_container_width=True, key="btn_view_report"):
            st.info("Full PDF report generation is a premium feature in the UX Lens roadmap.")

        if st.button(
            "Apply safe fixes",
            type="primary",
            use_container_width=True,
            key="btn_apply_fixes",
        ):
            st.success("Safe fixes applied (prototype simulation).")

    else:
        st.info(
            "Add a screenshot or image URL above, then select **Run full UX audit** to generate the report."
        )


# ─────────────────────────────────────────────
# Advanced: contrast checker
# ─────────────────────────────────────────────

st.divider()

with st.expander("Advanced tool: check a specific color contrast pair"):
    adv_left, adv_middle, adv_right = st.columns([2, 2, 1])

    with adv_left:
        element_name = st.text_input("Element name", value="Primary button")
        text_color = st.color_picker("Text color", value="#FFFFFF")

    with adv_middle:
        background_color = st.color_picker("Background color", value="#7EC8E3")
        large_text = st.checkbox(
            "Large text", help="WCAG large text is at least 18 pt or 14 pt bold."
        )

    with adv_right:
        st.write("")
        st.write("")
        if st.button("Check contrast", use_container_width=True, key="btn_contrast"):
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
                    <span class="grade" style="background:{color};">{result["severity"]}</span>
                </div>
                <div style="color:#7891AE;font-size:11px;padding-top:8px;">
                    WCAG level: {result["wcag_level"]} &nbsp;·&nbsp; {result["status"]} &nbsp;·&nbsp; {result["text_type"]}
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
        UX Lens AI prototype · Contrast calculations follow WCAG 2.1 requirements.
        Full visual findings are prototype heuristics and should be reviewed by a UX/UI designer.
    </div>
    """,
    unsafe_allow_html=True,
)
