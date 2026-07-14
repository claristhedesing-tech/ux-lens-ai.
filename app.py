import streamlit as st
from contrast_checker import audit_element


st.set_page_config(
    page_title="UX Lens AI",
    page_icon="🔍",
    layout="wide"
)


def severity_color(severity):
    colors = {
        "HIGH": "#EF4444",
        "MEDIUM": "#F59E0B",
        "LOW": "#22C55E",
    }
    return colors.get(severity, "#38BDF8")


def status_message(result, large_text):
    required_ratio = 3.0 if large_text else 4.5

    if result["status"] == "PASS":
        return (
            f"This combination passes WCAG 2.1 {result['wcag_level']} "
            f"for {'large' if large_text else 'normal'} text."
        )

    return (
        f"Increase the contrast ratio to at least {required_ratio}:1 "
        f"for {'large' if large_text else 'normal'} text."
    )


st.title("UX Lens AI")
st.caption("AI-assisted accessibility and visual-clarity reviewer")

st.divider()

left_column, right_column = st.columns([1.2, 1])

with left_column:
    st.subheader("Run a contrast audit")

    project_name = st.text_input(
        "Project name",
        value="New interface audit"
    )

    element_name = st.text_input(
        "UI element",
        value="Primary button"
    )

    text_color = st.color_picker(
        "Text color",
        value="#FFFFFF"
    )

    background_color = st.color_picker(
        "Background color",
        value="#7EC8E3"
    )

    large_text = st.checkbox(
        "This is large text",
        help="WCAG defines large text as at least 18 pt, or 14 pt bold."
    )

    run_audit = st.button("Run UX Lens audit", type="primary")

with right_column:
    st.subheader("UX Audit Results")

    if run_audit:
        result = audit_element(
            element_name,
            text_color,
            background_color,
            large_text
        )

        ratio = result["contrast_ratio"]
        severity = result["severity"]
        status = result["status"]
        color = severity_color(severity)

        st.markdown(
            f"""
            <div style="
                background-color: #0B1C33;
                border: 1px solid #18324F;
                border-radius: 12px;
                padding: 24px;
                color: white;
            ">
                <p style="color: #9DB2CE; margin: 0;">
                    PROJECT
                </p>
                <h3 style="margin-top: 5px;">{project_name}</h3>
                <p style="color: #9DB2CE;">OVERALL CONTRAST RESULT</p>
                <h1 style="font-size: 44px; margin: 0;">{ratio}:1</h1>
                <span style="
                    display: inline-block;
                    margin-top: 12px;
                    padding: 6px 12px;
                    border-radius: 999px;
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                ">
                    {severity} · {status}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.subheader("Actionable insight")

        if status == "PASS":
            st.success(status_message(result, large_text))
        else:
            st.error(status_message(result, large_text))

        st.markdown(
            f"""
            **Element:** {result["element"]}  
            **Text color:** `{result["text_color"]}`  
            **Background color:** `{result["bg_color"]}`  
            **WCAG result:** `{result["wcag_level"]}`
            """
        )

    else:
        st.info(
            "Choose two colors and select **Run UX Lens audit** "
            "to generate an accessibility result."
        )

st.divider()

st.caption(
    "UX Lens AI prototype — Contrast analysis based on WCAG 2.1 color-contrast requirements."
)
