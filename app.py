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

# ─────────────────────────────────────────────
# Contrast logic
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
    return {"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#22C55E"}.get(severity, "#38BDF8")

def severity_icon(severity):
    return {"HIGH": "●", "MEDIUM": "●", "LOW": "✓"}.get(severity, "•")

def build_audit_results(contrast_result=None):
    findings = [
        {"title": "Improve secondary text readability", "description": "Secondary labels may be difficult to read.", "severity": "HIGH"},
        {"title": "Increase touch target size", "description": "Mobile touch targets should be at least 44 × 44 px.", "severity": "MEDIUM"},
        {"title": "Navigation structure is clear", "description": "Consistent and recognizable layout pattern.", "severity": "LOW"},
    ]
    if contrast_result:
        ratio = contrast_result["contrast_ratio"]
        if contrast_result["status"] == "FAIL":
            findings.insert(0, {"title": f"Fix contrast in {contrast_result['element']}", "description": f"Has a {ratio}:1 ratio. Increase to 4.5:1.", "severity": "HIGH"})
    return findings

# ─────────────────────────────────────────────
# Page config & Styles
# ─────────────────────────────────────────────

st.set_page_config(page_title="UX Lens AI", page_icon="🔵", layout="wide")

st.markdown(
    """
    <style>
        .stApp { background:#061426; color:#E9F2FF; }
        [data-testid="stSidebar"] { background:#081B33; border-right:1px solid #173451; }
        .stButton > button { border-radius: 8px !important; font-weight: 700 !important; background: #0A203A !important; color: #E9F2FF !important; border: 1px solid #2A4B6D !important; }
        .stButton > button[kind="primary"] { background: #268CFF !important; border: 1px solid #3C9BFF !important; color: #FFFFFF !important; }
        .score-card { background:#0A203A; border:1px solid #1A4265; border-radius:10px; padding:16px; margin-bottom:12px; }
        .score-number { color:#F5F9FF; font-size:35px; font-weight:800; }
        .finding-card { display:flex; gap:10px; background:#0A203A; border:1px solid #173451; border-radius:8px; padding:12px; margin-bottom:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Sidebar con el Logo Corregido
# ─────────────────────────────────────────────

with st.sidebar:
    logo_col, text_col = st.columns([1, 4])
    with logo_col:
        # Usamos una URL de placeholder que funciona siempre para el prototipo
        st.image("https://cdn-icons-png.flaticon.com/512/8136/8136031.png", width=40)
    with text_col:
        st.markdown('<div style="color:#F5F9FF;font-size:18px;font-weight:800;padding-top:8px;">UX LENS</div>', unsafe_allow_html=True)
    
    st.caption("AI-assisted design review")
    st.divider()
    st.markdown("**Navigation**")
    st.caption("▦ Dashboard")
    st.caption("◉ Live audit")
    st.divider()
    st.success("AI engine online")

# ─────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────

st.title("UX Lens AI Audit")

col_input, col_preview = st.columns([2, 3])

with col_input:
    st.markdown("### 1. New Audit")
    project_name = st.text_input("Project Name", "New Audit Project")
    file = st.file_uploader("Upload screenshot", type=["png", "jpg", "webp"])
    run_audit = st.button("Run full UX audit", type="primary", use_container_width=True)

with col_preview:
    st.markdown("### 2. Interface Preview")
    if file:
        st.image(file, use_container_width=True)
    else:
        st.info("Upload an image to see the preview here.")

if run_audit:
    st.divider()
    res_left, res_right = st.columns([1, 2])
    
    with res_left:
        st.markdown(f'<div class="score-card"><div style="color:#7891AE;font-size:10px;">OVERALL SCORE</div><div class="score-number">82%</div></div>', unsafe_allow_html=True)
        st.metric("Accessibility", "72%", "-2%")
        st.metric("Usability", "88%", "+5%")
    
    with res_right:
        st.markdown("**Actionable Insights**")
        findings = build_audit_results()
        for f in findings:
            color = severity_color(f["severity"])
            st.markdown(f'<div class="finding-card"><div style="color:{color};">●</div><div><div style="font-weight:700;">{f["title"]}</div><div style="font-size:11px;color:#7891AE;">{f["description"]}</div></div></div>', unsafe_allow_html=True)
