"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""
import streamlit as st
import math

# ─────────────────────────────────────────────
# Configuración y Estilos
# ─────────────────────────────────────────────
st.set_page_config(page_title="UX Lens AI", page_icon="◎", layout="wide")

# CSS para replicar la interfaz profesional de la imagen
st.markdown("""
    <style>
        /* Fondo general y fuentes */
        .stApp { background-color: #061426; color: #E9F2FF; }
        
        /* Sidebar minimalista (solo iconos) */
        [data-testid="stSidebar"] { 
            background-color: #050F1E; 
            min-width: 60px !important;
            max-width: 60px !important;
            border-right: 1px solid #0F2540;
        }
        
        /* Contenedores de resultados y preview */
        .result-card { background: #0A203A; border: 1px solid #1A3A5C; border-radius: 10px; padding: 14px; margin-bottom: 10px; }
        .metric-box { background: #0A203A; border: 1px solid #173451; border-radius: 8px; padding: 8px; text-align: left; }
        
        /* Estilo de los hallazgos (insights) */
        .finding-item { 
            background: #0A203A; border: 1px solid #173451; border-radius: 8px; 
            padding: 10px; margin-bottom: 8px; display: flex; gap: 10px;
        }
        
        /* Breadcrumb superior */
        .breadcrumb { color: #4A6A8A; font-size: 12px; margin-bottom: 10px; }
        .breadcrumb b { color: #E9F2FF; font-weight: 500; }
        
        /* Botones */
        .stButton > button { border-radius: 6px !important; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar (Navegación por Iconos y Logo)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding-top:10px;">
    """, unsafe_allow_html=True)
    
    # Aquí insertamos tu imagen cargada
    st.image("mountains.png", width=35)
    
    st.markdown("""
            <div style="color:#268CFF; font-size:20px; margin-top:20px; margin-bottom:20px;">◉</div>
            <div style="color:#4A6A8A; font-size:20px; margin-bottom:20px;">⊞</div>
            <div style="color:#4A6A8A; font-size:20px; margin-bottom:20px;">≡</div>
            <div style="color:#4A6A8A; font-size:20px; margin-bottom:20px;">⚙</div>
        </div>
    """, unsafe_allow_html=True)
# ─────────────────────────────────────────────
# Header / Breadcrumb
# ─────────────────────────────────────────────
h_col1, h_col2 = st.columns([2, 1])
with h_col1:
    st.markdown("""
        <div class="breadcrumb">
            UX LENS &nbsp;›&nbsp; Projects &nbsp;›&nbsp; NOVA ATELIER Page Web &nbsp;›&nbsp; <b>Accessibility Audit</b>
        </div>
    """, unsafe_allow_html=True)
with h_col2:
    status_cols = st.columns([2, 1, 1])
    status_cols[0].markdown('<div style="color:#22C55E; font-size:11px; font-weight:700; padding-top:5px;">● Scan complete</div>', unsafe_allow_html=True)
    status_cols[1].button("Export", use_container_width=True)
    status_cols[2].button("Share", type="primary", use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# Cuerpo Principal (Layout de 2 Columnas)
# ─────────────────────────────────────────────
col_preview, col_results = st.columns([2.5, 1])

with col_preview:
    # Barra de herramientas del Preview
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.markdown("""
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-weight:700; font-size:15px;">NOVA ATELIER — Homepage</span>
                <span style="background:#0D2A4A; border:1px solid #268CFF; border-radius:4px; padding:2px 8px; color:#268CFF; font-size:10px; font-weight:700;">LIVE AUDIT</span>
            </div>
        """, unsafe_allow_html=True)
    with t_col2:
        st.button("New Scan ↻", use_container_width=True)
    
    # Área de la imagen
    uploaded_file = st.file_uploader("Upload screenshot to analyze", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    
    with st.container(border=True):
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)
        else:
            st.markdown('<div style="height:450px; display:flex; align-items:center; justify-content:center; color:#4A6A8A;">Drop interface screenshot here to begin audit</div>', unsafe_allow_html=True)

with col_results:
    st.markdown('<div style="color:#7891AE; font-size:10px; font-weight:800; letter-spacing:1px; margin-bottom:5px;">UX AUDIT RESULTS</div>', unsafe_allow_html=True)
    st.markdown("### Finova Mobile App")
    
    # Donut Score Card
    st.markdown("""
        <div class="result-card">
            <div style="display:flex; align-items:center; gap:15px;">
                <div style="font-size:36px; font-weight:800; color:#F59E0B;">78% <span style="font-size:14px; background:#22C55E; color:#061426; padding:2px 6px; border-radius:4px; vertical-align:middle;">B</span></div>
                <div>
                    <div style="font-weight:700; font-size:14px;">Good foundation</div>
                    <div style="color:#7891AE; font-size:11px;">Accessibility needs attention</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Grid
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown('<div class="metric-box"><div style="color:#7891AE; font-size:9px; font-weight:800;">ACCESSIBILITY</div><div style="color:#EF4444; font-size:22px; font-weight:800;">62%</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-box" style="margin-top:8px;"><div style="color:#7891AE; font-size:9px; font-weight:800;">VISUAL CLARITY</div><div style="color:#F59E0B; font-size:22px; font-weight:800;">81%</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-box"><div style="color:#7891AE; font-size:9px; font-weight:800;">USABILITY</div><div style="color:#22C55E; font-size:22px; font-weight:800;">88%</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-box" style="margin-top:8px;"><div style="color:#7891AE; font-size:9px; font-weight:800;">PERFORMANCE</div><div style="color:#22C55E; font-size:22px; font-weight:800;">90%</div></div>', unsafe_allow_html=True)

    st.markdown("<br><b>Actionable Insights</b> <span style='color:#268CFF; font-size:12px;'>5 items</span>", unsafe_allow_html=True)
    
    # Hallazgos de ejemplo
    findings = [
        ("Fix button contrast", "The 'View details' button has a 2.6:1 ratio.", "#EF4444", "HIGH"),
        ("Increase touch target", "Payments icon is too small for mobile.", "#F59E0B", "MEDIUM")
    ]
    
    for title, desc, color, sev in findings:
        st.markdown(f"""
            <div class="finding-item">
                <div style="color:{color}; font-size:14px; padding-top:2px;">◉</div>
                <div>
                    <div style="font-weight:700; font-size:12px;">{title}</div>
                    <div style="color:#7891AE; font-size:11px;">{desc}</div>
                    <span style="color:{color}; font-size:9px; font-weight:800; border:1px solid {color}44; padding:1px 5px; border-radius:10px;">{sev}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.button("View Full Audit Report", use_container_width=True)
