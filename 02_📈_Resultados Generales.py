import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np

# PARTE GENERAL

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
#data.columns = data.iloc[0]
data = data[1:]

# Seleccionar las columnas relevantes para las preguntas
preguntas_df = df.iloc[:, 7:15]  # Las columnas de la 7 a la 15
preguntas = preguntas_df.iloc[1:, :]
#st.write(preguntas)

# Seleccionar las columnas necesarias y convertirlas a DataFrames
sexo_doc = pd.DataFrame(df.iloc[:, 1])  # Índice 1 corresponde a la columna de sexo
edades_doc = pd.DataFrame(df.iloc[:, 2])  # Índice 2 corresponde a la columna de edades
instituto_doc = pd.DataFrame(df.iloc[:, 3])  # Índice 3 corresponde a la columna de instituto
formacion_tipo = pd.DataFrame(df.iloc[:, 4])  # Índice 4 corresponde a la columna de tipo de formación
area_conoc = pd.DataFrame(df.iloc[:, 5])  # Índice 5 corresponde a la columna de área de conocimiento

# Seleccionar las columnas relevantes para las competencias]
competencias = df.iloc[:, 31:36]  # Las columnas de la 31 a la 35 (índice 31 a 35)
competencias = competencias.iloc[1:, :]
#st.write(competencias)


# ENCABEZADO
st.title("Resultados Generales")

st.markdown('***')
st.markdown("*ATENCIÓN: Los gráficos mostrados pueden no reflejar de manera adecuada la información si la cantidad de datos recopilados es escasa. Usted podrá acceder a este sitio posteriormente cuando se cuente con un mayor número de datos relevados.*")
st.markdown('***')

st.markdown("ℹ️ Información General")

st.markdown("### Cantidad de Docentes Encuestados: " + str(len(edades_doc)-1))

st.markdown("#### GRAFICOS DE RESULTADOS")

# GRÁFICO DE RESPUESTAS NEGATIVAS EN MOMENTOS

st.markdown("#### Gráfico de respuestas Negativas en los Momentos del Diagnóstico Individual")

# Definir las etiquetas de las preguntas
preguntas = ['Uso autónomo',
             'Uso educativo cotidiano',
             'Implicaciones éticas',
             'Integra las TIC',
             'Combina lenguajes y herramientas',
             'Adopta nuevas ideas',
             'Argumenta',
             'Comparte actividades/estrategias']

# Contar la cantidad de "No" en cada columna
conteo_no = (preguntas_df == 'No').sum()

# Convertir el conteo a un DataFrame para facilitar el graficado
conteo_no_df = pd.DataFrame({'Pregunta': preguntas, 'No': conteo_no.values})

# Crear un gráfico de barras
fig = px.bar(conteo_no_df, x='Pregunta', y='No', title='Cantidad de "No" por Pregunta', labels={'No': 'Cantidad de No', 'Pregunta': 'Pregunta'})

# Actualizar el diseño del gráfico
fig.update_layout(
    title={'font': {'size': 18, 'family': 'Arial'}},
    xaxis_title={'font': {'size': 16,  'color': 'black'}, 'text': 'Pregunta'},
    yaxis_title={'font': {'size': 16,  'color': 'black'}, 'text': 'Cantidad de No'},
    font=dict(
        size=10,
        color="black",
    )
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# GRÁFICO DOCENTES POR SEXO

# Tomo las edades excluyendo el nombre de la columna
sexo = sexo_doc.iloc[1:, 0]

# Conteo de edades para crear el gráfico
conteo_sexo = sexo.value_counts()
conteo_sexo = conteo_sexo.astype(int)

# Se generar una lista de colores para cada barra
colors = ['blue','pink', 'grey'] 


# Create the figure
fig, ax = plt.subplots()

# Elimino los decimales del eje y
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(''))

# Genero la figura correspondiente al gráfico de barras
ax.bar(conteo_sexo.index, conteo_sexo,color=colors)
plt.xlabel("Sexo", fontsize = 10, fontweight='bold')
plt.ylabel("Cantidad por sexo", fontsize = 10, fontweight='bold')
plt.title('Cantidad de docentes por Sexo', fontsize = 10, fontweight='bold')
for i, v in enumerate(conteo_sexo):
    plt.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')

# Muestro la figura
st.pyplot(fig)
st.markdown('***')

# GRÁFICO DOCENTES POR EDAD

# Tomo las edades excluyendo el nombre de la columna
edades = edades_doc.iloc[1:, 0]
#st.write(edades)

# Conteo de edades para crear el gráfico
conteo_edades = edades.value_counts()
conteo_edades = conteo_edades.astype(int)

# Se generar una lista de colores para cada barra
colors = ['purple', 'blue','green', 'red', 'orange','yellow'] 

# Create the figure
fig, ax = plt.subplots()

# Elimino los decimales del eje y
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(''))

# Genero la figura correspondiente al gráfico de barras
ax.bar(conteo_edades.index, conteo_edades,color=colors)
plt.xlabel("Rangos de edades", fontsize = 10, fontweight='bold')
plt.ylabel("Cantidad por edad", fontsize = 10, fontweight='bold')
plt.xticks(rotation=45)
plt.title('Cantidad de docentes por Rango Etario', fontsize = 12, fontweight='bold')
for i, v in enumerate(conteo_edades):
    plt.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')

# Muestro la figura
st.pyplot(fig)
st.markdown('***')

# GRÁFICO DOCENTES POR INSTITUTO

# Tomo los institutos excluyendo el nombre de la columna
institutos = instituto_doc.iloc[1:, 0]

# Conteo de institutos para crear el gráfico
conteo_institutos = institutos.value_counts()
conteo_institutos= conteo_institutos.astype(int)


# Create the figure
fig, ax = plt.subplots()

# Elimino los decimales del eje y
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(''))

# Genero la figura correspondiente al gráfico de barras
ax.bar(conteo_institutos.index, conteo_institutos)
plt.xlabel("Institutos", fontsize = 6, fontweight='bold')
plt.ylabel("Cantidad de Docentes", fontsize = 12, fontweight='bold')
plt.title("Cantidad de docentes por Instituto", fontsize = 12, fontweight='bold')

# Recortar las etiquetas del eje x para tomar solo la última parte del texto
recortadas = [etiqueta.split()[-1] for etiqueta in conteo_institutos.index]
ax.set_xticklabels(recortadas, rotation=45, fontsize=8)

# Añadir las etiquetas de las barras con un tamaño de fuente más pequeño y en negrita
for i, v in enumerate(conteo_institutos):
    plt.text(i, v, str(v), ha='center', va='bottom')

# Muestro la figura
st.pyplot(fig)
st.markdown('***')

# GRAFICO DOCENTES POR TIPO DE FORMACIÓN

# Tomo los valores de las formaciones excluyendo el nombre de la columna
formacion = formacion_tipo.iloc[1:, 0]

# Conteo de institutos para crear el gráfico
conteo_formacion = formacion.value_counts()
conteo_formacion= conteo_formacion.astype(int)

# Crea la figura y el eje
fig, ax = plt.subplots(figsize=(10, 10))

# Crea el gráfico circular
ax.pie(conteo_formacion, labels=conteo_formacion.index, autopct='%0.1f%%', 
       wedgeprops=dict(width=0.5, edgecolor='black'))

# Agrega título y etiquetas
plt.title('Docentes por Tipo de Formación', fontsize = 12, fontweight='bold')
plt.legend(loc='best')

# Muestra el gráfico en Streamlit
st.pyplot(fig)
st.markdown('***')

# GRÁFICO DOCENTES POR AREA DE CONOCIMIENTO

# Tomo los valores de las áreas excluyendo el nombre de la columna
area = area_conoc.iloc[1:, 0]

# Conteo de áreas para crear el gráfico
conteo_formacion = area.value_counts()
conteo_formacion = conteo_formacion.astype(int)

# Crea la figura y el eje
fig, ax = plt.subplots(figsize=(10, 10))

# Crea el gráfico circular
ax.pie(conteo_formacion, labels=conteo_formacion.index, autopct='%0.1f%%',
       wedgeprops=dict(width=0.5, edgecolor='black'),
       textprops={'fontsize': 14, 'fontweight': 'bold'},  # Etiquetas en negrita
       labeldistance=1.1)  # Mueve las etiquetas un poco a la derecha

# Agrega título y etiquetas
plt.title('Docentes por Área de Conocimiento', fontsize=14, fontweight='bold')
# Mueve la leyenda hacia la derecha
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# Muestra el gráfico en Streamlit
st.pyplot(fig)
st.markdown('***')

# GRÁFICO DE COMPETENCIAS POR NIVELES

# Suma la cantidad de docentes en el nivel 1, 2 y 3 para cada competencia
docentes_por_nivel = competencias.apply(pd.Series.value_counts).fillna(0)
#st.write(docentes_por_nivel)

# Transponer el DataFrame para que los índices sean los niveles y las columnas sean las competencias
docentes_por_nivel = docentes_por_nivel.T
#st.write(docentes_por_nivel)

# Configurar la interfaz de usuario con Streamlit
st.markdown('### Gráfico comparativo de niveles por competencia')

# Define colores para cada competencia
paleta_colores = {
    'CT': ['#FBC315', '#EDBC17', '#FC791E'],  # Naranja
    'CP': ['#00FF00', '#32CD32', '#006400'],  # Verde oscuro
    'CC': ['#00FFFF', '#40E0D0',  '#20B2AA'],  # Turquesa
    'CG': ['#AACC83', '#556832','#424632'],  # Oliva
    'CI': ['#D4B9D7', '#B378A3', '#8673A1']   # Violeta
}

# Definir los nombres de las competencias (asegúrate de que coincidan con tus datos)
column_names = ['CT', 'CP', 'CC', 'CG', 'CI']

# Crear figura de Plotly
fig = go.Figure()

# Ajustar el gráfico para solo tres niveles
posiciones = list(range(1, len(column_names)*3+1, 3))  # Posiciones de las barras
ancho_barra = 0.5  # Ancho de las barras

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
    title=f'Distribución de docentes por nivel de competencias',
    xaxis=dict(title='Competencias', tickvals=[pos + 1 for pos in posiciones], ticktext=column_names),
    yaxis=dict(title='Cantidad de Docentes'),
    barmode='group',
    showlegend=True
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig)

st.write('💡 Desplace el puntero sobre el gráfico para más detalles')
st.write('********')
