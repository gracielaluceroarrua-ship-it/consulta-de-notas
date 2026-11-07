import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Consulta de Calificaciones", page_icon="📚", layout="centered"
)

st.title("📚 Consulta de Calificaciones")
st.markdown("Ingrese su número de DNI para consultar su estado académico.")

# ID de tu Google Sheet
SHEET_ID = "1TATrnl23SVmyjK_d5aCUBR1h-5GtMJbbCJeGipakLRU"


# Función para cargar los datos de la planilla
@st.cache_data(ttl=60)
def cargar_datos():
  url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Notas%20finales%202026_Anuales"
  df = pd.read_csv(url)
  return df


# Intentamos cargar los datos con un indicador visual
try:
  with st.spinner("Cargando datos de la planilla..."):
    df = cargar_datos()
  exito_carga = True
except Exception as e:
  exito_carga = False
  st.error(
      f"No se pudo conectar con la planilla. Verifica que sea pública: {e}"
  )

# Si los datos cargaron correctamente, mostramos el formulario
if exito_carga:
  with st.form("consulta_form"):
    dni_ingresado = st.text_input("Número de DNI")
    submitted = st.form_submit_button("Consultar Calificación")

  if submitted:
    if dni_ingresado:
      q_dni = "".join(filter(str.isdigit, str(dni_ingresado)))
      encontrado = False

      for index, row in df.iterrows():
        celda_dni = str(row.iloc[1])
        dni_fila = "".join(filter(str.isdigit, celda_dni))

        if dni_fila == q_dni:
          encontrado = True
          st.success("¡Registro encontrado!")
          st.markdown(f"### {row.iloc[0]}")  # Nombre
          st.markdown(f"**Carrera:** {row.iloc[2]}")  # Carrera
          st.markdown(
              f"**Parcial:** {row.iloc[6] if len(row) > 6 else 'N/A'}"
          )  # G
          st.markdown(
              f"**Entrega Final:** {row.iloc[7] if len(row) > 7 else 'N/A'}"
          )  # H
          st.markdown(
              f"**Presentación:** {row.iloc[8] if len(row) > 8 else 'N/A'}"
          )  # I
          st.markdown(
              f"**Promedio Final:** {row.iloc[9] if len(row) > 9 else 'N/A'}"
          )  # J
          st.markdown(
              f"**Condición:** **{row.iloc[10] if len(row) > 10 else 'Sin calificar'}**"
          )  # K
          break

      if not encontrado:
        st.error(
            "No se encontró ningún registro coincidente con el DNI ingresado."
        )
    else:
      st.warning("Por favor, ingrese un número de DNI válido.")
