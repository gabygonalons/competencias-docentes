import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np

# Autenticación para acceder a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
gc = gspread.authorize(credentials)

# Apertura de una hoja de cálculo específica
spreadsheet_key = "18Z1d9Ir_KyQyOgyaKZKk0Us07xgsP0xp6jMkWOGQ2Sg"
worksheet = gc.open_by_key(spreadsheet_key).sheet1

# Leer todas las columnas necesarias de una sola vez
data = worksheet.get_all_values()

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Eliminar la primera fila que contiene los nombres de las columnas
data = data[1:]
#st.write(data)

# Seleccionar las columnas necesarias y convertirlas a DataFrames
sexo_doc = pd.DataFrame(df.iloc[:, 1])  # Índice 1 corresponde a la columna de sexo
edades_doc = pd.DataFrame(df.iloc[:, 2])  # Índice 2 corresponde a la columna de edades
instituto_doc = pd.DataFrame(df.iloc[:, 3])  # Índice 3 corresponde a la columna de instituto
formacion_tipo = pd.DataFrame(df.iloc[:, 4])  # Índice 4 corresponde a la columna de tipo de formación
area_conoc = pd.DataFrame(df.iloc[:, 5])  # Índice 5 corresponde a la columna de área de conocimiento
sexo_doc = sexo_doc.iloc[1:, :]
#st.write(sexo_doc)
edades_doc = edades_doc.iloc[1:, :]
#st.write(edades_doc)
instituto_doc = instituto_doc.iloc[1:, :]
#st.write(instituto_doc)
formacion_tipo = formacion_tipo.iloc[1:, :]
#st.write(formacion_tipo)
area_conoc = area_conoc.iloc[1:, :]
#st.write(area_conoc)

# Seleccionar las columnas relevantes para las competencias]
competencias = df.iloc[:, 31:36]  # Las columnas de la 31 a la 35 (índice 31 a 35)
competencias = competencias.iloc[1:, :]
#st.write(competencias)




st.markdown("#### ANÁLISIS DE LOS DATOS RECOPILADOS")
st.markdown("### Gráficos")
st.markdown("ℹ️ Información General")
st.markdown('***')

# GRÁFICOS ADICIONALES

# Asegurarse de que las columnas sean de tipo float
competencias = competencias.astype(float)

# Renombrar las columnas de competencias
competencias.columns = ['CT', 'CP', 'CC', 'CG', 'CI']

# Convertir las competencias a valores numéricos
competencias = competencias.apply(pd.to_numeric, errors='coerce')
#st.write(competencias)

# GRÁFICO DE CAJA

st.markdown("### Gráfico de Caja y Bigotes o BoxPlot")

# Generar el gráfico de caja
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=competencias, ax=ax)
ax.set_title('Distribución de Competencias')
ax.set_xlabel('Competencias')
ax.set_ylabel('Valores')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

texto = """
#### Interpretación del gráfico de Caja:
- **Competencia Tecnológica:** La mediana está en el valor más bajo (alrededor de 1). No hay variabilidad (la caja es un solo valor), y hay un valor atípico a 2.
- **Competencia Pedagógica:** La mediana está alrededor de 1.75. El IQR (rango entre el Q1 y Q3) va desde aproximadamente 1.5 hasta 2. Hay un valor atípico a 3.
- **Competencia Comunicativa:** Similar a la Competencia Tecnológica, con la mediana en el valor más bajo (alrededor de 1). Hay un valor atípico a 2.
- **Competencia de Gestión:** La mediana está alrededor de 1.75. El IQR va desde aproximadamente 1.5 hasta 2. Hay un valor atípico a 3.
- **Competencia Investigativa:** La mediana está alrededor de 1.75. El IQR va desde aproximadamente 1.5 hasta 2. Hay un valor atípico a 3.

#### Conclusiones:
- **Competencia Tecnológica:** La mayoría de los valores se encuentran en el rango bajo (alrededor de 1), con poca variabilidad y un valor atípico más alto.
- **Competencia Pedagógica, Competencia de Gestión, y Competencia Investigativa:** Estas competencias muestran más variabilidad dentro del rango intercuartil (entre 1.5 y 2), pero también tienen valores atípicos altos (a 3).
- **Competencia Comunicativa:** Similar a CT, con la mayoría de los valores en el nivel más bajo (1) y algunos valores atípicos.

El gráfico proporciona una visión general de cómo están distribuidas las competencias entre los docentes:
Las competencias tecnológicas y comunicativas tienen una baja variabilidad con la mayoría de los valores en el rango más bajo.
Las competencias pedagógicas, de gestión e investigativa muestran más variabilidad, pero aún tienden a estar en el rango bajo a medio, con algunos valores atípicos más altos.
Esto puede indicar que, en general, las competencias tecnológicas y comunicativas son percibidas como más bajas entre los docentes, mientras que las otras competencias muestran más diversidad en las respuestas, con algunos docentes destacándose en niveles más altos.
"""
st.markdown(texto)

st.markdown('***')
# Comparación por grupo: Gráficos de violín
st.markdown("#### Gráfico de Violín o Violín Plot")

# Asignar nombres a las columnas de competencias
competencias.columns = [
    'Competencia Tecnológica', 
    'Competencia Pedagógica', 
    'Competencia Comunicativa', 
    'Competencia de Gestión', 
    'Competencia Investigativa'
]

# Combinar los DataFrames en uno solo
df_combined = pd.concat([sexo_doc.reset_index(drop=True),
                         edades_doc.reset_index(drop=True),
                         formacion_tipo.reset_index(drop=True),
                         area_conoc.reset_index(drop=True),
                         competencias.reset_index(drop=True)], axis=1)

# Renombrar las columnas del DataFrame combinado
df_combined.columns = [
    'Sexo', 'Edad', 'Tipo_Formacion', 'Area_Conocimiento', 
    'Competencia Tecnológica', 'Competencia Pedagógica', 
    'Competencia Comunicativa', 'Competencia de Gestión', 
    'Competencia Investigativa'
]

# Seleccionar el grupo y la competencia para comparar
grupo = st.selectbox('Selecciona un grupo:', ['Sexo', 'Edad', 'Tipo_Formacion', 'Area_Conocimiento'])
competencia = st.selectbox('Selecciona una competencia:', [
    'Competencia Tecnológica', 'Competencia Pedagógica', 'Competencia Comunicativa', 'Competencia de Gestión', 'Competencia Investigativa'
])

# Generar el gráfico de violín con puntos y mostrar todos los datos
fig = px.violin(df_combined, y=competencia, x=grupo, box=True, points='all')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# Diccionario de interpretaciones
interpretaciones = {
    ('Sexo', 'Competencia Tecnológica'): """
    **Interpretación de Competencia Tecnológica por Sexo:**
    - Para el sexo Femenino, la mediana de la Competencia Tecnológica parece estar alrededor de 1.5, con algunos valores atípicos que llegan hasta 3.5.
    - Para el sexo Masculino, la mayoría de los datos se encuentran agrupados alrededor de 1, con menos dispersión comparado con el grupo Femenino.
    - El grupo Femenino presenta una mayor variabilidad en la Competencia Tecnológica, mientras que el grupo Masculino muestra una distribución más compacta y concentrada.

    **Conclusión General:**
    En general, las mujeres tienden a mostrar mayor variabilidad en las competencias tecnológicas comparadas con los hombres, que presentan distribuciones más concentradas.
    """,
    ('Sexo', 'Competencia Pedagógica'): """
    **Interpretación de Competencia Pedagógica por Sexo:**
    - Para el sexo Femenino, la mediana de la Competencia Pedagógica está cerca de 1.5, con algunos valores atípicos que alcanzan hasta 3.5.
    - Para el sexo Masculino, la mediana está alrededor de 1.5, con valores atípicos que llegan hasta 3.5.
    - Ambos sexos muestran una distribución similar en la Competencia Pedagógica, con una ligera mayor dispersión en el grupo Femenino.

    **Conclusión General:**
    Tanto hombres como mujeres muestran una distribución similar en competencias pedagógicas.
    """,
    ('Sexo', 'Competencia Comunicativa'): """
    **Interpretación de Competencia Comunicativa por Sexo:**
    - Para el sexo Femenino, la mediana de la Competencia Comunicativa parece estar alrededor de 1.5, con algunos valores atípicos que llegan hasta 3.5.
    - Para el sexo Masculino, la mayoría de los datos se encuentran alrededor de 1, con una dispersión menor comparada con el grupo Femenino.
    - El grupo Femenino presenta una mayor variabilidad en la Competencia Comunicativa, mientras que el grupo Masculino muestra una distribución más compacta y concentrada.

    **Conclusión General:**
    En general, las mujeres tienden a mostrar mayor variabilidad en las competencias comunicativas comparadas con los hombres, que presentan distribuciones más concentradas.
    """,
    ('Sexo', 'Competencia de Gestión'): """
    **Interpretación de Competencia de Gestión por Sexo:**
    - Para el sexo Femenino, la mediana de la Competencia de Gestión está cerca de 1.5, con algunos valores atípicos que alcanzan hasta 3.
    - Para el sexo Masculino, la mediana también está alrededor de 1.5, con valores atípicos que llegan hasta 3.
    - Ambos sexos muestran una distribución similar en la Competencia de Gestión, aunque el grupo Masculino presenta una mayor dispersión.

    **Conclusión General:**
    Tanto hombres como mujeres muestran una distribución similar en competencias de gestión, aunque los hombres presentan mayor dispersión.
    """,
    ('Sexo', 'Competencia Investigativa'): """
    **Interpretación de Competencia Investigativa por Sexo:**
    - Para el sexo Femenino, la mediana de la Competencia Investigativa parece estar alrededor de 1.5, con algunos valores atípicos que llegan hasta 3.5.
    - Para el sexo Masculino, la mayoría de los datos se encuentran alrededor de 1, con una mayor dispersión comparada con el grupo Femenino.
    - El grupo Femenino presenta una mayor variabilidad en la Competencia Investigativa, mientras que el grupo Masculino muestra una distribución más compacta y concentrada.

    **Conclusión General:**
    En general, las mujeres tienden a mostrar mayor variabilidad en las competencias investigativas comparadas con los hombres, que presentan distribuciones más concentradas.
    """,
    ('Edad', 'Competencia Tecnológica'): """
    **Interpretación de Competencia Tecnológica por Edad:**
    - Los grupos de edad de 30 a 39 años y de 50 a 59 años presentan una mayor dispersión en la Competencia Tecnológica.
    - Los grupos de 20 a 29 años y más de 60 años muestran menos variabilidad en sus puntuaciones.
    - Los grupos intermedios (30 a 59 años) tienden a tener puntuaciones más variadas y, en algunos casos, valores más altos en Competencia Tecnológica.

    **Conclusión General:**
    Los grupos de edad más jóvenes (20-29 años) suelen tener una menor dispersión y estar más concentrados alrededor de un valor central en casi todas las competencias.
    Los mayores de 60 años muestran menor variabilidad en todas las competencias, con concentraciones cercanas a valores centrales.
    """,
    ('Edad', 'Competencia Pedagógica'): """
    **Interpretación de Competencia Pedagógica por Edad:**
    - Los grupos de 30 a 39 años, 40 a 49 años, 50 a 59 años y 20 a 29 años tienen una dispersión similar con valores atípicos.
    - El grupo de más de 60 años muestra una menor variabilidad en la Competencia Pedagógica.

    **Conclusión General:**
    Los mayores de 60 años muestran menor variabilidad en todas las competencias, con concentraciones cercanas a valores centrales.
    """,
    ('Edad', 'Competencia Comunicativa'): """
    **Interpretación de Competencia Comunicativa por Edad:**
    - Los grupos de 30 a 39 años, 40 a 49 años y 50 a 59 años tienen una mayor dispersión y presencia de valores atípicos.
    - El grupo de 20 a 29 años muestra una distribución más compacta, con valores concentrados alrededor del rango intercuartil.
    - El grupo de más de 60 años presenta una menor dispersión y muestra una concentración cercana al valor central, con algunos valores atípicos presentes.

    **Conclusión General:**
    Los grupos de edad más jóvenes (20-29 años) suelen tener una menor dispersión y estar más concentrados alrededor de un valor central en casi todas las competencias.
    Los mayores de 60 años muestran menor variabilidad en todas las competencias, con concentraciones cercanas a valores centrales.
    """,
    ('Edad', 'Competencia de Gestión'): """
    **Interpretación de Competencia de Gestión por Edad:**
    - Los grupos de 30 a 39 años, 40 a 49 años y 50 a 59 años presentan valores atípicos y variabilidad.
    - El grupo de 20 a 29 años tiene una menor dispersión y parece estar más concentrado alrededor de un valor central.
    - El grupo de más de 60 años muestra una menor variabilidad en la Competencia de Gestión.

    **Conclusión General:**
    Los grupos de edad más jóvenes (20-29 años) suelen tener una menor dispersión y estar más concentrados alrededor de un valor central en casi todas las competencias.
    Los mayores de 60 años muestran menor variabilidad en todas las competencias, con concentraciones cercanas a valores centrales.
    """,
    ('Edad', 'Competencia Investigativa'): """
    **Interpretación de Competencia Investigativa por Edad:**
    - Los grupos de 30 a 39 años, 40 a 49 años y 50 a 59 años presentan una mayor dispersión y presencia de valores atípicos.
    - El grupo de 20 a 29 años tiene una menor dispersión y parece estar más concentrado alrededor de un valor central.
    - El grupo de más de 60 años muestra una menor variabilidad en la Competencia Investigativa.

    **Conclusión General:**
    Los grupos de edad más jóvenes (20-29 años) suelen tener una menor dispersión y estar más concentrados alrededor de un valor central en casi todas las competencias.
    Los mayores de 60 años muestran menor variabilidad en todas las competencias, con concentraciones cercanas a valores centrales.
    """,
    ('Tipo_Formacion', 'Competencia Tecnológica'): """
    **Interpretación de Competencia Tecnológica por Tipo de Formación:**
    - Formación Docente: La mediana de la Competencia Tecnológica es alrededor de 1.5. Mayor dispersión con algunos valores que alcanzan 3.5.
    - Ambas Formaciones: Mediana similar alrededor de 1.5. Menor dispersión comparada con la Formación Docente.
    - Formación Técnica: Mediana cercana a 2. Dispersión considerable con algunos valores atípicos hasta 3.5.

    **Conclusión General:**
    La formación docente muestra mayor variabilidad en la mayoría de las competencias.
    """,
    ('Tipo_Formacion', 'Competencia Pedagógica'): """
    **Interpretación de Competencia Pedagógica por Tipo de Formación:**
    - Formación Docente: Muestra una mayor dispersión en los valores de la Competencia Pedagógica.
    - Ambas Formaciones: Mediana alrededor de 1.5. Menor dispersión comparada con la Formación Docente.
    - Formación Técnica: Mediana cercana a 2. Distribución amplia con algunos valores atípicos.

    **Conclusión General:**
    La formación docente muestra mayor variabilidad en la mayoría de las competencias.
    """,
    ('Tipo_Formacion', 'Competencia Comunicativa'): """
    **Interpretación de Competencia Comunicativa por Tipo de Formación:**
    - Formación Docente: Muestra una mayor dispersión en los valores de la Competencia Comunicativa.
    - Ambas Formaciones: Distribución más concentrada alrededor de los valores medianos.
    - Formación Técnica: Mediana cercana a 2. Distribución amplia con algunos valores atípicos.

    **Conclusión General:**
    La formación docente muestra mayor variabilidad en la mayoría de las competencias.
    """,
   ('Tipo_Formacion', 'Competencia de Gestión'): """
    **Interpretación de Competencia de Gestión por Tipo de Formación:**
    - Formación Docente: muestra una mediana cercana a 1.0 con una dispersión considerable y valores atípicos.
    - Ambas Formaciones: la mediana es similar a 1.0, pero con una mayor dispersión y valores atípicos.
    - Formación Técnica: presenta una mediana alrededor de 1.0 con menos dispersión y algunos valores atípicos.

    **Conclusión General:**
    La formación docente muestra mayor variabilidad en la mayoría de las competencias.
    """,

    ('Tipo_Formacion', 'Competencia Investigativa'): """
    **Interpretación de Competencia Investigativa por Tipo de Formación:**
    - Formación Docente: la mediana está cerca de 1.5, con una amplia dispersión de datos y valores atípicos.
    - Ambas Formaciones: la mediana es de 1.0 con una dispersión considerable y varios valores atípicos.
    - Formación Técnica: muestra una mediana alrededor de 1.0 con menos dispersión y algunos valores atípicos.

    **Conclusión General:**
    La formación docente muestra mayor variabilidad en la mayoría de las competencias.
    """,
     ('Area_Conocimiento', 'Competencia Tecnológica'): """
    **Interpretación de Competencia Tecnológica por Área de Conocimiento:**
    - Ciencias Exactas y Naturales presenta una mayor variabilidad en la Competencia Tecnológica, con una mediana alrededor de 2 y algunos valores atípicos hasta 3.5.
    - Ciencias Sociales y Humanidades muestra una menor variabilidad con la mayoría de los datos alrededor de 1.5.
    - Ciencias Biológicas y de la Salud tienen una distribución similar a Ciencias Exactas y Naturales, pero con menos dispersión.
    - Ciencias Agrarias, de Ingeniería y de Materiales presentan una distribución más concentrada con valores bajos de competencia.

    **Conclusión General:**
    Las áreas de Ciencias Exactas y Naturales tienden a mostrar mayor variabilidad en las competencias tecnológicas, mientras que Ciencias Sociales y Humanidades presentan menor variabilidad.
    """,
    ('Area_Conocimiento', 'Competencia Pedagógica'): """
    **Interpretación de Competencia Pedagógica por Área de Conocimiento:**
    - Ciencias Exactas y Naturales presenta una mediana cercana a 2, con una amplia dispersión y algunos valores atípicos hasta 3.5.
    - Ciencias Sociales y Humanidades muestran una distribución similar con una mediana alrededor de 2, pero con menos dispersión.
    - Ciencias Biológicas y de la Salud destacan con una mayor variabilidad y algunos valores atípicos hasta 4.
    - Ciencias Agrarias, de Ingeniería y de Materiales tienen una distribución más concentrada en valores bajos de competencia.

    **Conclusión General:**
    Las áreas de Ciencias Exactas y Naturales tienden a mostrar mayor variabilidad en las competencias pedagógicas, mientras que Ciencias Sociales y Humanidades presentan menor variabilidad.
    """,
    ('Area_Conocimiento', 'Competencia Comunicativa'): """
    **Interpretación de Competencia Comunicativa por Área de Conocimiento:**
    - Ciencias Exactas y Naturales tiene una mediana alrededor de 1.5, con algunos valores atípicos hasta 3.
    - Ciencias Sociales y Humanidades presentan una mayor variabilidad con una mediana cercana a 2.
    - Ciencias Biológicas y de la Salud tienen una mediana alrededor de 2, con menos dispersión comparado con Ciencias Sociales y Humanidades.
    - Ciencias Agrarias, de Ingeniería y de Materiales muestran una distribución más concentrada en valores bajos de competencia.

    **Conclusión General:**
    Las áreas de Ciencias Exactas y Naturales tienden a mostrar mayor variabilidad en las competencias comunicativas, mientras que Ciencias Sociales y Humanidades presentan menor variabilidad.
    """,
      ('Area_Conocimiento', 'Competencia de Gestión'): """
    **Interpretación de Competencia de Gestión por Área de Conocimiento:**
    - Ciencias Exactas y Naturales tienen una mayor dispersión con valores atípicos hasta 3.
    - Ciencias Sociales y Humanidades muestran una mediana alrededor de 1.5 con menos dispersión.
    - Ciencias Biológicas y de la Salud presentan una mayor variabilidad y una mediana de alrededor de 2.5.
    - Ciencias Agrarias, de Ingeniería y de Materiales muestran una menor dispersión con la mayoría de los datos alrededor de 1.

    **Conclusión General:**
    Las áreas de Ciencias Exactas y Naturales tienden a mostrar mayor variabilidad en las competencias de gestión, mientras que Ciencias Sociales y Humanidades presentan menor variabilidad.
    """,
    ('Area_Conocimiento', 'Competencia Investigativa'): """
    **Interpretación de Competencia Investigativa por Área de Conocimiento:**
    - Ciencias Exactas y Naturales presentan una mayor variabilidad con una mediana alrededor de 2.
    - Ciencias Sociales y Humanidades tienen una mediana alrededor de 2 con menos dispersión.
    - Ciencias Biológicas y de la Salud muestran una mayor dispersión con valores atípicos hasta 3.5.
    - Ciencias Agrarias, de Ingeniería y de Materiales tienen una menor variabilidad con la mayoría de los datos alrededor de 1.5.

    **Conclusión General:**
    Las áreas de Ciencias Exactas y Naturales tienden a mostrar mayor variabilidad en las competencias investigativas, mientras que Ciencias Sociales y Humanidades presentan menor variabilidad.
    """
}

# Mostrar la interpretación específica si existe
interpretacion = interpretaciones.get((grupo, competencia), """
**Interpretación general:**
- Analiza cómo se distribuye la competencia {competencia} en función del grupo {grupo}.
- Observa las diferencias en la mediana, los cuartiles y los outliers.
- Utiliza el gráfico de violín para entender la densidad de los datos y la distribución general.
""")

st.write(interpretacion.format(competencia=competencia, grupo=grupo))
st.markdown('***')


# Correlación: mapa de calor
st.markdown("### Correlación entre competencias")
corr = competencias.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Mapa de Calor de Correlación entre Competencias')
st.pyplot(fig)

texto = """
#### Interpretación de los valores de correlación
Los valores de correlación se representan con colores, donde el rojo indica una correlación positiva fuerte, el azul indica una correlación negativa fuerte y el verde indica una correlación débil o inexistente.
En el gráfico, se observan las siguientes correlaciones:
* **CT y CP:** Correlación positiva moderada (0.52). Esto significa que hay una tendencia a que las dos competencias aumenten o disminuyan juntas.
* **CT y CG:** Correlación positiva moderada (0.46). Similar a la relación entre CT y CP, estas dos competencias tienden a aumentar o disminuir juntas.
* **CT y CI:** Correlación positiva moderada (0.55). Similar a las relaciones anteriores, estas dos competencias tienden a aumentar o disminuir juntas.
* **CP y CG:** Correlación positiva muy fuerte (0.9). Esto significa que hay una fuerte tendencia a que las dos competencias aumenten o disminuyan juntas.
* **CP y CI:** Correlación positiva muy fuerte (0.8). Similar a la relación entre CP y CG, estas dos competencias tienden a aumentar o disminuir juntas.
* **CG y CI:** Correlación negativa fuerte (-0.7). Esto significa que hay una fuerte tendencia a que las dos competencias aumenten o disminuyan en direcciones opuestas.

"""
st.markdown(texto)
st.markdown('***')

#---------------------------------------------------