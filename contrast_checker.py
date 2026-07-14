"""
UX Lens AI — Contrast Checker Prototype

A small, dependency-free Python prototype for checking text and
background color contrast using WCAG 2.1 guidelines.

The examples represent the three UX Lens AI audit screens:
1. Finova mobile banking app
2. Nova Atelier e-commerce website
3. Travelo.co travel website

Run:
    python contrast_checker.py
"""


def validate_hex_color(hex_color):
    """Validate a color in #RRGGBB hexadecimal format."""
    if not isinstance(hex_color, str):
        raise ValueError("Color must be a string in #RRGGBB format.")

    if len(hex_color) != 7 or not hex_color.startswith("#"):
        raise ValueError(
            f"Invalid color '{hex_color}'. Use the format #RRGGBB."
        )

    try:
        int(hex_color[1:], 16)
    except ValueError as error:
        raise ValueError(
            f"Invalid hexadecimal color: '{hex_color}'."
        ) from error


def hex_to_rgb(hex_color):
    """Convert a #RRGGBB color into an RGB tuple."""
    validate_hex_color(hex_color)

    return (
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16),
    )


def relative_luminance(rgb):
    """
    Calculate relative luminance according to WCAG 2.1.

    RGB values must be integers between 0 and 255.
    """
    converted_channels = []

    for channel in rgb:
        normalized = channel / 255

        if normalized <= 0.03928:
            converted_channels.append(normalized / 12.92)
        else:
            converted_channels.append(
                ((normalized + 0.055) / 1.055) ** 2.4
            )

    red, green, blue = converted_channels

    return (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)


def contrast_ratio(text_color, background_color):
    """
    Calculate the WCAG contrast ratio between two hexadecimal colors.

    Returns a number from 1.0:1 to 21.0:1.
    """
    text_luminance = relative_luminance(hex_to_rgb(text_color))
    background_luminance = relative_luminance(hex_to_rgb(background_color))

    lighter = max(text_luminance, background_luminance)
    darker = min(text_luminance, background_luminance)

    return round((lighter + 0.05) / (darker + 0.05), 2)


def wcag_result(ratio, large_text=False):
    """
    Evaluate a contrast ratio against WCAG 2.1 standards.

    Normal text:
    - AA: 4.5:1
    - AAA: 7:1

    Large text:
    - AA: 3:1
    - AAA: 4.5:1
    """
    aa_threshold = 3.0 if large_text else 4.5
    aaa_threshold = 4.5 if large_text else 7.0

    if ratio >= aaa_threshold:
        return "AAA", "PASS"

    if ratio >= aa_threshold:
        return "AA", "PASS"

    return "FAIL", "FAIL"


def severity_level(ratio, large_text=False):
    """
    Assign UX Lens severity labels for contrast-related issues.

    HIGH: major failure below 60% of the minimum requirement
    MEDIUM: below the minimum requirement
    LOW: passes contrast requirements
    """
    minimum_ratio = 3.0 if large_text else 4.5

    if ratio < minimum_ratio * 0.6:
        return "HIGH"

    if ratio < minimum_ratio:
        return "MEDIUM"

    return "LOW"


def recommended_action(ratio, large_text=False):
    """Return an actionable UX Lens-style recommendation."""
    minimum_ratio = 3.0 if large_text else 4.5

    if ratio >= minimum_ratio:
        return "Contrast meets the required WCAG threshold."

    if large_text:
        return "Increase contrast to at least 3.0:1 for large text."

    return "Increase contrast to at least 4.5:1 for normal text."


def audit_element(name, text_color, background_color, large_text=False):
    """Audit one interface element and return a structured result."""
    ratio = contrast_ratio(text_color, background_color)
    wcag_level, status = wcag_result(ratio, large_text)
    severity = severity_level(ratio, large_text)

    return {
        "element": name,
        "text_color": text_color,
        "background_color": background_color,
        "contrast_ratio": ratio,
        "text_type": "Large text" if large_text else "Normal text",
        "wcag_level": wcag_level,
        "status": status,
        "severity": severity,
        "action": recommended_action(ratio, large_text),
    }


def calculate_score(results):
    """
    Calculate a simple prototype accessibility score.

    Each passed element counts as one successful check.
    """
    if not results:
        return 0

    passed_elements = sum(
        1 for result in results if result["status"] == "PASS"
    )

    return round((passed_elements / len(results)) * 100)


def letter_grade(score):
    """Convert a percentage score into a dashboard-style grade."""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def print_report(project_name, elements):
    """Print a UX Lens-style contrast audit report in the terminal."""
    results = []

    for element in elements:
        result = audit_element(
            name=element["name"],
            text_color=element["text_color"],
            background_color=element["background_color"],
            large_text=element.get("large_text", False),
        )
        results.append(result)

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    results.sort(key=lambda result: severity_order[result["severity"]])

    issues = [
        result for result in results
        if result["status"] == "FAIL"
    ]

    passed = [
        result for result in results
        if result["status"] == "PASS"
    ]

    score = calculate_score(results)
    grade = letter_grade(score)

    print("\n" + "=" * 64)
    print("UX LENS AI — ACCESSIBILITY CONTRAST AUDIT")
    print(f"Project: {project_name}")
    print("=" * 64)

    print(f"\nOVERALL SCORE: {score}%  |  GRADE: {grade}")
    print(f"Elements checked: {len(results)}")
    print(f"Issues found: {len(issues)}")
    print(f"Passed checks: {len(passed)}")

    if issues:
        print("\nACTIONABLE INSIGHTS")
        print("-" * 64)

        for item in issues:
            print(f"\n[{item['severity']}] {item['element']}")
            print(f"Text type: {item['text_type']}")
            print(f"Contrast ratio: {item['contrast_ratio']}:1")
            print(f"WCAG result: {item['wcag_level']}")
            print(f"Text color: {item['text_color']}")
            print(f"Background color: {item['background_color']}")
            print(f"Suggested action: {item['action']}")

    if passed:
        print("\nPASSED CHECKS")
        print("-" * 64)

        for item in passed:
            print(
                f"[PASS] {item['element']} — "
                f"{item['contrast_ratio']}:1 ({item['wcag_level']})"
            )

    print("\n" + "=" * 64)
    print("UX Lens AI — Scan complete")
    print("=" * 64)


# ------------------------------------------------------------
# EXAMPLE 1 — Finova Mobile Banking App
# Visual reference: finance-full-ux-audit.png
# ------------------------------------------------------------

finova_elements = [
    {
        "name": "Account balance secondary label",
        "text_color": "#B8BDC8",
        "background_color": "#FFFFFF",
    },
    {
        "name": "View details button",
        "text_color": "#FFFFFF",
        "background_color": "#7EC8E3",
    },
    {
        "name": "Helper text below balance",
        "text_color": "#C5CAD4",
        "background_color": "#FFFFFF",
    },
    {
        "name": "Bottom navigation inactive label",
        "text_color": "#AAAAAA",
        "background_color": "#F8F9FC",
    },
    {
        "name": "Action card icon on pastel background",
        "text_color": "#FFFFFF",
        "background_color": "#A8D8B9",
    },
    {
        "name": "Monthly spending chart bars",
        "text_color": "#B2DFC0",
        "background_color": "#F0FAF3",
    },
    {
        "name": "Primary account balance heading",
        "text_color": "#1A1A2E",
        "background_color": "#FFFFFF",
    },
]


# ------------------------------------------------------------
# EXAMPLE 2 — Nova Atelier E-commerce Homepage
# Visual reference: e-commerce-full-ux-audit.png
#
# This prototype checks contrast-related elements. The complete
# UX Lens concept would additionally inspect CTA hierarchy,
# badges, filters, product-card density, and layout structure.
# ------------------------------------------------------------

nova_atelier_elements = [
    {
        "name": "Shop Women CTA button",
        "text_color": "#FFFFFF",
        "background_color": "#B8A99A",
    },
    {
        "name": "Shop Men CTA button",
        "text_color": "#FFFFFF",
        "background_color": "#B8A99A",
    },
    {
        "name": "Explore Collection CTA button",
        "text_color": "#FFFFFF",
        "background_color": "#B8A99A",
    },
    {
        "name": "Shop now link on hero image",
        "text_color": "#D4C5B8",
        "background_color": "#8C7B6E",
    },
    {
        "name": "Product badge text",
        "text_color": "#FFFFFF",
        "background_color": "#C4A882",
    },
    {
        "name": "Product title",
        "text_color": "#1A1A1A",
        "background_color": "#FAF8F5",
    },
    {
        "name": "Filter label",
        "text_color": "#9A8F87",
        "background_color": "#FAF8F5",
    },
    {
        "name": "Newsletter card heading",
        "text_color": "#1A1A1A",
        "background_color": "#EDE8E2",
    },
]


# ------------------------------------------------------------
# EXAMPLE 3 — Travelo.co Travel Homepage
# Visual reference: header-image.png
# ------------------------------------------------------------

travelo_elements = [
    {
        "name": "Hero headline on image",
        "text_color": "#FFFFFF",
        "background_color": "#3A5A7A",
        "large_text": True,
    },
    {
        "name": "Hero body text on image",
        "text_color": "#E0E8F0",
        "background_color": "#4A6A8A",
    },
    {
        "name": "Navigation links",
        "text_color": "#8BAABF",
        "background_color": "#1B3A52",
    },
    {
        "name": "Sign up CTA button",
        "text_color": "#FFFFFF",
        "background_color": "#19D3E6",
    },
    {
        "name": "Destination card title",
        "text_color": "#1A1A2E",
        "background_color": "#FFFFFF",
    },
    {
        "name": "Destination country label",
        "text_color": "#8899AA",
        "background_color": "#FFFFFF",
    },
    {
        "name": "Footer links",
        "text_color": "#7A8FA0",
        "background_color": "#0D1F2D",
    },
]


if __name__ == "__main__":
    print_report("Finova — Mobile Banking App", finova_elements)
    print_report("Nova Atelier — E-commerce Homepage", nova_atelier_elements)
    print_report("Travelo.co — Travel Homepage", travelo_elements)
