 import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Consulta de Calificaciones", page_icon="📚", layout="centered"
)

st.title("📚 Consulta de Calificaciones")
st.markdown("Ingrese su número de DNI para consultar su estado académico.")

# ID de tu Google Sheet y nombre de la pestaña (sin espacios conflictivos)
SHEET_ID = "1TATrnl23SVmyjK_d5aCUBR1h-5GtMJbbCJeGipakLRU"
SHEET_NAME = "Notas finales 2026_Anuales".strip()


# Función para cargar los datos de la planilla con URL limpia
@st.cache_data(ttl=60)
def cargar_datos():
  url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={requests.utils.quote(SHEET_NAME)}"
  # O de forma directa asegurando que no haya espacios en la URL:
  url_limpia = (
      f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Notas%20finales%202026_Anuales"
  )
  df = pd.read_csv(url_limpia)
  return df
