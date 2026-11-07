import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Consulta de Calificaciones", page_icon="📚", layout="centered"
)

st.title("📚 Consulta de Calificaciones")
st.markdown("Ingrese su número de DNI para consultar su estado académico.")

# ID de tu Google Sheet y nombre de la pestaña
SHEET_ID = "1TATrnl23SVmyjK_d5aCUBR1h-5GtMJbbCJeGipakLRU"
SHEET_NAME = "Notas finales 2026_Anuales"


# Función para cargar los datos de la planilla (con caché de 1 minuto para velocidad)
@st.cache_data(ttl=60)
def cargar_datos():
  url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
  df = pd.read_csv(url)
  return df


try:
  # Cargamos la planilla
  df = cargar_datos()

  # Formulario de consulta
  with st.form("consulta_form"):
    dni_ingresado = st.text_input("Número de DNI")
    submitted = st.form_submit_button("Consultar Calificación")

  if submitted:
    if dni_ingresado:
      # Limpiamos el DNI ingresado (solo números)
      q_dni = "".join(filter(str.isdigit, str(dni_ingresado)))
      encontrado = False

      # Recorremos el DataFrame buscando coincidencia en la Columna B (índice 1)
      for index, row in df.iterrows():
        celda_dni = str(row.iloc[1])
        dni_fila = "".join(filter(str.isdigit, celda_dni))

        if dni_fila == q_dni:
          encontrado = True
          st.success("¡Registro encontrado!")

          # Mostramos los resultados ordenados
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
            "No se encontró ningún registro coincidente con el DNI ingresado."
        )
    else:
      st.warning("Por favor, ingrese un número de DNI válido.")

except Exception as e:
  st.error(
      f"Error al conectar con la planilla. Asegúrese de que sea pública para"
      f" lectura: {e}"
  )
