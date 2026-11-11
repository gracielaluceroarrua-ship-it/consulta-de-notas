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
        # Buscamos la columna de DNI de forma flexible
        celda_dni = ""
        for col in row.index:
          if "DNI" in str(col).upper():
            celda_dni = str(row.get(col, ""))
            break
            
        dni_fila = "".join(filter(str.isdigit, celda_dni))

        if dni_fila == q_dni:
          encontrado = True
          st.success("¡Registro encontrado!")

          # Función auxiliar para buscar columnas por palabras clave (ignora mayúsculas, tildes y caracteres ocultos)
          def obtener_valor_flexible(keyword, defecto):
            for col in row.index:
              if keyword in str(col).upper():
                val = row.get(col)
                if not (pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan"):
                  return val
            return defecto

          # Extracción segura e independiente de formato
          alumno = obtener_valor_flexible("ALUMNO", "N/A")
          carrera = obtener_valor_flexible("CARRERA", "N/A")
          parcial = obtener_valor_flexible("PARCIAL", "-")
          tp2 = obtener_valor_flexible("TP2", obtener_valor_flexible("ENTREGA FINAL", "-"))
          presentacion = obtener_valor_flexible("PRESENTACIÓN", obtener_valor_flexible("PRESENTACION", "-"))
          promedio = obtener_valor_flexible("PROMEDIO", "-")
          condicion = obtener_valor_flexible("CONDICIÓN", obtener_valor_flexible("CONDICION", "Sin calificar"))

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
