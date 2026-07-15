from pathlib import Path
import base64
import re

app_path = Path("app.py")
logo_path = Path("Logo-UXLens.png")

if not app_path.exists():
    raise FileNotFoundError("No se encontró app.py en esta carpeta.")

if not logo_path.exists():
    raise FileNotFoundError("No se encontró Logo-UXLens.png en esta carpeta.")

logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
app_code = app_path.read_text(encoding="utf-8")

logo_variable = f'LOGO_B64 = "{logo_b64}"'

# Reemplaza un LOGO_B64 existente, aunque sea incompleto.
if "LOGO_B64 =" in app_code:
    app_code = re.sub(
        r'LOGO_B64\s*=\s*".*?"',
        logo_variable,
        app_code,
        count=1,
        flags=re.DOTALL,
    )
else:
    anchor = "from PIL import Image\n"
    app_code = app_code.replace(
        anchor,
        f"{anchor}\n\n{logo_variable}\n",
        1,
    )

# Sustituye el bloque que carga el logo desde GitHub.
old_sidebar_logo = '''    logo_col, text_col = st.columns([1, 4])

    with logo_col:
        st.image(
            "https://raw.githubusercontent.com/claristhedesing-tech/ux-lens-ai/main/assets/Logo-UXLens.png",
            width=40,
        )

    with text_col:
        st.markdown(
            """
            <div style="color:#F5F9FF;font-size:18px;font-weight:800;letter-spacing:0.5px;padding-top:8px;">
                UX LENS
            </div>
            """,
            unsafe_allow_html=True,
        )'''

new_sidebar_logo = '''    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;padding-bottom:8px;">
            <img
                src="data:image/png;base64,{LOGO_B64}"
                width="40"
                style="border-radius:8px;"
                alt="UX Lens logo"
            />
            <span style="color:#F5F9FF;font-size:18px;font-weight:800;letter-spacing:0.5px;">
                UX LENS
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )'''

if old_sidebar_logo not in app_code:
    raise ValueError(
        "No se encontró el bloque actual del logo en la barra lateral. "
        "Asegúrate de que app.py contiene el código original."
    )

app_code = app_code.replace(old_sidebar_logo, new_sidebar_logo, 1)

app_path.write_text(app_code, encoding="utf-8")

print("✅ app.py actualizado correctamente.")
print("✅ El logo se ha incrustado en base64.")
