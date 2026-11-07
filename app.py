import urllib.parse
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Consulta de Calificaciones", page_icon="📚", layout="centered"
)

st.title("📚 Consulta de Calificaciones")
st.markdown(
    "Seleccione su curso e ingrese su número de DNI para consultar su estado"
    " académico."
)

# Diccionario con las opciones actualizadas y sus planillas correspondientes
PLANILLAS = {
    "anuales": {
        "id": "1TATrnl23SVmyjK_d5aCUBR1h-5GtMJbbCJeGipakLRU",
        "sheet": "Notas finales 2026_Anuales",
    },
    "matemática": {
        "id": "1Nh7XP9xiNcM9s0NOiqgz8U-4H4iP0AZfs37V3qpM1qI",
        "sheet": "Notas finales matemática 2026",
    },
}

# Selector desplegable de curso
comision_seleccionada = st.selectbox(
    "Seleccione la opción:", list(PLANILLAS.keys())
)
datos_comision = PLANILLAS[comision_seleccionada]


# Función para cargar datos manejando correctamente espacios y tildes en la URL
@st.cache_data(ttl=60)
def cargar_datos(sheet_id, sheet_name):
  sheet_encoded = urllib.parse.quote(sheet_name)
  url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_encoded}"
  df = pd.read_csv(url)
  return df


# Carga de datos con indicador visual
try:
  with st.spinner(f"Cargando datos de {comision_seleccionada}..."):
    df = cargar_datos(datos_comision["id"], datos_comision["sheet"])
  exito_carga = True
except Exception as e:
  exito_carga = False
  st.error(
      f"No se pudo conectar con la planilla seleccionada. Asegúrese de que sea"
      f" pública: {e}"
  )

# Formulario de consulta
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
          st.markdown(f"### {row.iloc[0]}")  # Nombre (Columna A)
          st.markdown(f"**Carrera:** {row.iloc[2]}")  # Carrera (Columna C)
          st.markdown(
              f"**Parcial:** {row.iloc[6] if len(row) > 6 else 'N/A'}"
          )  # Columna G
          st.markdown(
              f"**Entrega Final:** {row.iloc[7] if len(row) > 7 else 'N/A'}"
          )  # Columna H
          st.markdown(
              f"**Presentación:** {row.iloc[8] if len(row) > 8 else 'N/A'}"
          )  # Columna I
          st.markdown(
              f"**Promedio Final:** {row.iloc[9] if len(row) > 9 else 'N/A'}"
          )  # Columna J
          st.markdown(
              f"**Condición:** **{row.iloc[10] if len(row) > 10 else 'Sin calificar'}**"
          )  # Columna K
          break

      if not encontrado:
        st.error(
            "No se encontró ningún registro coincidente con el DNI ingresado"
            " en esta opción."
        )
    else:
      st.warning("Por favor, ingrese un número de DNI válido.")
