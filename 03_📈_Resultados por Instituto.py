import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.graph_objects as go

# Autenticación para acceder a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
gc = gspread.authorize(credentials)

# Apertura de una hoja de cálculo específica
spreadsheet_key = "18Z1d9Ir_KyQyOgyaKZKk0Us07xgsP0xp6jMkWOGQ2Sg"
worksheet = gc.open_by_key(spreadsheet_key).sheet1

# INFORMACIÓN OBTENIDA

# Leer todas las columnas necesarias de una sola vez
data = worksheet.get_all_values()

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Eliminar la primera fila que contiene los nombres de las columnas
df = df.iloc[1:]

# Seleccionar las columnas relevantes para las competencias
competencias = df.iloc[:, 31:36]  # Las columnas de la 32 a la 36 (índice 31 a 35)
competencias = competencias.apply(pd.to_numeric, errors='coerce').fillna(0)
#st.write(competencias)


# ENCABEZADO
st.title("Resultados por Instituto")

st.markdown('***')
st.markdown("*ATENCIÓN: Los gráficos mostrados pueden no reflejar de manera adecuada la información recopilada si la cantidad de datos recopilados es escasa. Usted podrá acceder a este sitio posteriormente cuando se cuente con un mayor número de datos relevados.*")
st.markdown('***')


st.markdown("#### GRAFICOS DE RESULTADOS")

# Obtener lista de institutos únicos
institutos = df.iloc[:, 3].unique().tolist()

# Interfaz de usuario
selected_institute = st.selectbox('Selecciona un instituto:', institutos)

# Filtrar datos por instituto seleccionado
competencias_filtradas = df[df.iloc[:, 3] == selected_institute].iloc[:, 31:36]
competencias_filtradas = competencias_filtradas.apply(pd.to_numeric, errors='coerce').fillna(0)
#st.write(competencias_filtradas)

# Suma la cantidad de docentes en el nivel 1, 2 y 3 para cada competencia
docentes_por_nivel = competencias_filtradas.apply(pd.Series.value_counts).fillna(0)

# Transponer el DataFrame para que los índices sean los niveles y las columnas sean las competencias
docentes_por_nivel = docentes_por_nivel.T

st.markdown("ℹ️ Información por Instituto")

st.markdown("### Cantidad de Docentes Encuestados: " + str(len(competencias_filtradas)))

# GRÁFICOS DE COMPETENCIAS POR INSTITUTO

st.markdown('### Gráfico comparativo de niveles por competencia')

column_names = ['CT', 'CP', 'CC', 'CG', 'CI']

# Define colores para cada competencia
paleta_colores = {
    'CT': ['#FBC315', '#EDBC17', '#FC791E'],  # Naranja
    'CP': ['#00FF00', '#32CD32', '#006400'],  # Verde oscuro
    'CC': ['#00FFFF', '#40E0D0',  '#20B2AA'],  # Turquesa
    'CG': ['#AACC83', '#556832','#424632'],  # Oliva
    'CI': ['#D4B9D7', '#B378A3', '#8673A1']   # Violeta
}

# Ajustar el gráfico para solo tres niveles
posiciones = list(range(1, len(column_names)*3+1, 3))  # Posiciones de las barras
ancho_barra = 0.5  # Ancho de las barras

# Crear figura
fig = go.Figure()

# Recorrer las competencias y niveles
for i, (competencia, niveles) in enumerate(zip(column_names, docentes_por_nivel.values)):
    for j, cantidad in enumerate(niveles[:3], start=1):  # Tomar solo los tres primeros niveles
        # Calcular la posición de la barra actual
        x = posiciones[i] + j - 1

        # Obtener el color para la competencia actual
        color_competencia = paleta_colores[competencia][j-1]

        # Añadir barra al gráfico
        fig.add_trace(go.Bar(
            x=[x],
            y=[cantidad],
            marker_color=color_competencia,
            width=ancho_barra,
            name=f'{competencia} - Nivel {j}',
            text=[str(int(cantidad))],
            textposition='outside'
        ))

# Actualizar diseño del gráfico
fig.update_layout(
    title=f'Distribución de docentes por nivel en {selected_institute}',
    xaxis=dict(title='Competencias', tickvals=[pos + 1 for pos in posiciones], ticktext=column_names),
    yaxis=dict(title='Cantidad de Docentes'),
    barmode='group',
    showlegend=True
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig)

st.write('💡 Desplace el puntero sobre el gráfico para más detalles')
st.write('********')
