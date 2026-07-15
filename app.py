import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="UX Lens - Design Audit",
    page_icon="🕵️‍♀️",
    layout="wide"
)

# Header superior
col_logo, col_title, col_status = st.columns([1, 3, 2])

with col_logo:
    st.markdown("### UX Lens")

with col_title:
    st.markdown("## Design Audit Dashboard")
    st.caption("Visual Hierarchy & UX Audit")

with col_status:
    st.markdown("#### Overall Score: 72%")
    st.markdown("**Status:** Needs Attention")

st.markdown("---")

# Layout principal: izquierda (placeholder de interfaz), derecha (panel de auditoría)
left, right = st.columns([2, 1])

with left:
    st.markdown("### Audited Interface Preview")
    st.info(
        "Here you can embed a screenshot or live preview of the interface being audited.\n\n"
        "For now, this area is a placeholder where you would show the product page, "
        "app screen, or any UI you are evaluating."
    )

with right:
    st.markdown("### Audit Summary")

    st.markdown("#### Scores")
    st.progress(0.72)
    st.write("**Overall UX Score:** 72%")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Visual Hierarchy:** 64%")
        st.write("**Usability:** 82%")
    with col2:
        st.write("**Accessibility:** 89%")
        st.write("**Performance:** 91%")

    st.markdown("#### Actionable Insights")
    st.markdown("- **Medium:** Choose one primary CTA")
    st.markdown("- **Medium:** Increase main action visibility")
    st.markdown("- **Medium:** Reduce competing visual elements")
    st.markdown("- **Medium:** Reorder secondary content below key results")
    st.markdown("- **Low:** Brand visual identity is consistent")

st.markdown("---")

# Sección de detalles de auditoría
st.markdown("### Audit Details")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**Audit Type**")
    st.write("Visual Hierarchy Audit")

with col_b:
    st.markdown("**Issues Found**")
    st.write("5")

with col_c:
    st.markdown("**Last Run**")
    st.write("2026-07-15")

st.markdown("#### Notes")
st.write(
    "This audit focuses on how clearly primary actions are communicated, how content is "
    "prioritized visually, and whether users can quickly understand what to do next."
)

st.markdown("#### Next Steps")
st.markdown("- Refine CTA hierarchy and reduce visual noise.")
st.markdown("- Validate changes with quick usability testing.")
st.markdown("- Re-run audit after design updates to compare scores.")
