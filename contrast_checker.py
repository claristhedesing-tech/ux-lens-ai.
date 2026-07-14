# ============================================================
# UX LENS AI — Contrast Checker Prototype
# contrast_checker.py
#
# This script replicates the core accessibility logic behind
# the "UX Audit Results" panel shown in the UX Lens interface.
# It checks color contrast ratios against WCAG 2.1 AA standards
# and generates a prioritized list of actionable insights.
#
# Three audits included, matching the project examples:
#   1. Finova Mobile Banking App     (finance-full-ux-audit.png)
#   2. Nova Atelier E-commerce       (ecommerce-full-ux-audit.png)
#   3. Travelo.co Travel Homepage    (header-image.png)
# ============================================================


def hex_to_rgb(hex_color):
    """Convert a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    """Calculate the relative luminance of an RGB color."""
    values = []
    for channel in rgb:
        c = channel / 255
        if c <= 0.03928:
            values.append(c / 12.92)
        else:
            values.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def contrast_ratio(color1, color2):
    """Calculate the contrast ratio between two hex colors."""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def wcag_grade(ratio, large_text=False):
    """
    Return WCAG 2.1 compliance level.
    Normal text: AA requires 4.5:1, AAA requires 7:1.
    Large text:  AA requires 3.0:1, AAA requires 4.5:1.
    """
    threshold_aa  = 3.0 if large_text else 4.5
    threshold_aaa = 4.5 if large_text else 7.0

    if ratio >= threshold_aaa:
        return "AAA", "PASS"
    elif ratio >= threshold_aa:
        return "AA",  "PASS"
    else:
        return "Fail", "FAIL"


def severity_label(ratio, large_text=False):
    """Map contrast ratio to UX Lens severity: HIGH, MEDIUM, LOW."""
    threshold = 3.0 if large_text else 4.5
    if ratio < threshold * 0.6:
        return "HIGH"
    elif ratio < threshold:
        return "MEDIUM"
    else:
        return "LOW"


def audit_element(name, text_color, bg_color, large_text=False):
    """Audit a single UI element and return a structured result."""
    ratio          = contrast_ratio(text_color, bg_color)
    level, status  = wcag_grade(ratio, large_text)
    severity       = severity_label(ratio, large_text)

    return {
        "element":        name,
        "text_color":     text_color,
        "bg_color":       bg_color,
        "contrast_ratio": ratio,
        "wcag_level":     level,
        "status":         status,
        "severity":       severity,
    }


def generate_ux_lens_report(project_name, elements):
    """
    Generate a UX Lens-style accessibility audit report
    for a list of UI elements.
    """
    print("=" * 60)
    print(f"  UX LENS AI — Accessibility Audit")
    print(f"  Project: {project_name}")
    print("=" * 60)

    issues = []
    passed = []

    for el in elements:
        result = audit_element(
            el["name"],
            el["text_color"],
            el["bg_color"],
            el.get("large_text", False)
        )
        if result["status"] == "FAIL":
            issues.append(result)
        else:
            passed.append(result)

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    issues.sort(key=lambda x: severity_order[x["severity"]])

    total = len(elements)
    score = round((len(passed) / total) * 100) if total > 0 else 0

    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"

    print(f"\n  OVERALL SCORE : {score}%  |  Grade: {grade}")
    print(f"  {len(issues)} issue(s) found  |  {len(passed)} passed\n")

    if issues:
        print("  ACTIONABLE INSIGHTS")
        print("  " + "-" * 50)
        for item in issues:
            print(f"\n  [{item['severity']}] {item['element']}")
            print(f"  Contrast ratio : {item['contrast_ratio']}:1  ({item['wcag_level']})")
            print(f"  Text color     : {item['text_color']}")
            print(f"  Background     : {item['bg_color']}")
            if item["severity"] == "HIGH":
                print(f"  Action         : Increase contrast to at least 4.5:1")
            elif item["severity"] == "MEDIUM":
                print(f"  Action         : Review and adjust color combination")

    if passed:
        print(f"\n  PASSED ELEMENTS ({len(passed)})")
        print("  " + "-" * 50)
        for item in passed:
            print(f"  [OK] {item['element']} — {item['contrast_ratio']}:1 ({item['wcag_level']})")

    print("\n" + "=" * 60)
    print("  UX Lens AI — Scan complete")
    print("=" * 60 + "\n")


# ============================================================
# EXAMPLE 1: Finova Mobile Banking App
# Reference image: finance-full-ux-audit.png
# Issues: low-contrast labels, weak CTA button, tiny helper
#         text, pale chart bars, undersized touch targets.
# ============================================================

finova_elements = [
    {"name": "Account balance secondary label", "text_color": "#B8BDC8", "bg_color": "#FFFFFF"},
    {"name": "View details button",             "text_color": "#FFFFFF", "bg_color": "#7EC8E3"},
    {"name": "Helper text below balance",       "text_color": "#C5CAD4", "bg_color": "#FFFFFF"},
    {"name": "Bottom nav inactive label",       "text_color": "#AAAAAA", "bg_color": "#F8F9FC"},
    {"name": "Action card icon on pastel",      "text_color": "#FFFFFF", "bg_color": "#A8D8B9"},
    {"name": "Chart bars vs background",        "text_color": "#B2DFC0", "bg_color": "#F0FAF3"},
    {"name": "Primary heading balance",         "text_color": "#1A1A2E", "bg_color": "#FFFFFF"},
    {"name": "Recent activity label",           "text_color": "#2D3748", "bg_color": "#FFFFFF"},
]

generate_ux_lens_report("Finova — Mobile Banking App", finova_elements)


# ============================================================
# EXAMPLE 2: Nova Atelier E-commerce Homepage
# Reference image: ecommerce-full-ux-audit.png
# Issues: three competing CTAs with equal visual weight,
#         hidden Shop now link, overloaded product badges,
#         unclear filter labels, newsletter interrupting grid.
# ============================================================

nova_atelier_elements = [
    {"name": "Shop Women CTA button",           "text_color": "#FFFFFF", "bg_color": "#B8A99A"},
    {"name": "Shop Men CTA button",             "text_color": "#FFFFFF", "bg_color": "#B8A99A"},
    {"name": "Explore Collection CTA button",   "text_color": "#FFFFFF", "bg_color": "#B8A99A"},
    {"name": "Shop now text link on hero",      "text_color": "#D4C5B8", "bg_color": "#8C7B6E"},
    {"name": "Product badge on card",           "text_color": "#FFFFFF", "bg_color": "#C4A882"},
    {"name": "Product title large",             "text_color": "#1A1A1A", "bg_color": "#FAF8F5"},
    {"name": "Product price label",             "text_color": "#3D3D3D", "bg_color": "#FAF8F5"},
    {"name": "Filter label Edit selection",     "text_color": "#9A8F87", "bg_color": "#FAF8F5"},
    {"name": "Newsletter card heading",         "text_color": "#1A1A1A", "bg_color": "#EDE8E2"},
    {"name": "Navigation links header",         "text_color": "#2C2C2C", "bg_color": "#FAF8F5"},
]

generate_ux_lens_report("Nova Atelier — E-commerce Homepage", nova_atelier_elements)


# ============================================================
# EXAMPLE 3: Travelo.co Travel Homepage
# Reference image: header-image.png
# Issues: hero text over image, unclear hero copy,
#         competing Sign up vs search, low-contrast nav,
#         crowded destination cards, footer link contrast.
# ============================================================

travelo_elements = [
    {"name": "Hero headline on image",      "text_color": "#FFFFFF", "bg_color": "#3A5A7A", "large_text": True},
    {"name": "Hero body text on image",     "text_color": "#E0E8F0", "bg_color": "#4A6A8A"},
    {"name": "Navigation links",            "text_color": "#8BAABF", "bg_color": "#1B3A52"},
    {"name": "Sign up CTA button",          "text_color": "#FFFFFF", "bg_color": "#19D3E6"},
    {"name": "Destination card title",      "text_color": "#1A1A2E", "bg_color": "#FFFFFF"},
    {"name": "Card country label",          "text_color": "#8899AA", "bg_color": "#FFFFFF"},
    {"name": "Footer links",                "text_color": "#7A8FA0", "bg_color": "#0D1F2D"},
]

generate_ux_lens_report("Travelo.co — Travel Homepage", travelo_elements)
