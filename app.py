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

# Diccionario con las opciones y sus planillas
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

# Selector desplegable
comision_seleccionada = st.selectbox(
    "Seleccione la opción:", list(PLANILLAS.keys())
)
datos_comision = PLANILLAS[comision_seleccionada]


# Función para cargar datos
@st.cache_data(ttl=60)
def cargar_datos(sheet_id, sheet_name):
  sheet_encoded = urllib.parse.quote(sheet_name)
  url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_encoded}"
  df = pd.read_csv(url)
  
  # LIMPIEZA CLAVE: Normalizamos los nombres de las columnas (quitamos espacios y pasamos a mayúsculas)
  df.columns = df.columns.astype(str).str.strip().str.upper()
  return df


# Carga de datos
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

      for _, row in df.iterrows():
        # Obtenemos el DNI de forma segura asegurando que exista la columna
        celda_dni = str(row.get("DNI", ""))
        dni_fila = "".join(filter(str.isdigit, celda_dni))

        if dni_fila == q_dni:
          encontrado = True
          st.success("¡Registro encontrado!")

          # Función auxiliar para extraer el valor y manejar celdas vacías/NaN
          def obtener_valor(columna, defecto="Sin calificar"):
            val = row.get(columna)
            if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
              return defecto
            return val

          # Extraemos los campos usando los nombres normalizados en mayúsculas
          alumno = obtener_valor("ALUMNO", "N/A")
          carrera = obtener_valor("CARRERA", "N/A")
          parcial = obtener_valor("PARCIAL", "-")
          tp2 = obtener_valor("TP2 (ENTREGA FINAL)", obtener_valor("TP 2", "-"))
          presentacion = obtener_valor("PRESENTACIÓN", obtener_valor("PRESENTACION", "-"))
          promedio = obtener_valor("PROMEDIO FINAL", "-")
          condicion = obtener_valor("CONDICIÓN", obtener_valor("CONDICION", "Sin calificar"))

          # Mostramos los resultados
          st.markdown(f"### {alumno}")
          st.markdown(f"**Carrera:** {carrera}")
          st.markdown(f"**Parcial:** {parcial}")
          st.markdown(f"**TP 2 (Entrega Final):** {tp2}")
          st.markdown(f"**Presentación:** {presentacion}")
          st.markdown(f"**Promedio Final:** {promedio}")
          st.markdown(f"**Condición:** **{condicion}**")
          break

      if not encontrado:
        st.error(
            "No se encontró ningún registro coincidente con el DNI ingresado"
            " en esta opción."
        )
    else:
      st.warning("Por favor, ingrese un número de DNI válido.")
