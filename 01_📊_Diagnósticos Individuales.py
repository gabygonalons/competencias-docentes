import streamlit as st
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter

# PARTE GENERAL

# Autenticación para acceder a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
gc = gspread.authorize(credentials)

# Acceso a la hoja de cálculo
spreadsheet_key = "18Z1d9Ir_KyQyOgyaKZKk0Us07xgsP0xp6jMkWOGQ2Sg"
worksheet = gc.open_by_key(spreadsheet_key).sheet1

st.title("Diagnósticos Individuales")
st.markdown('***')
st.markdown("##### Para conocer los resultados del Diagnóstico de Competencias, por favor ingrese el código generado al final de la encuesta y luego presione Enter.")

# Ingreso del código de usuario
codigo_usuario = st.text_input("Ingrese su código:", "")

# Verificación del código
if codigo_usuario:
    try:
        indice_fila = worksheet.col_values(31).index(codigo_usuario) + 1
    except ValueError:
        st.warning("Código no encontrado. Ingrese un código válido.")
        st.stop()
else:
    st.stop()

# Lectura y almacenamiento de la información en dataframes

# Obtener respuestas para la fila específica
respuestas_pp = worksheet.row_values(indice_fila)[7:15]
#st.write(respuestas_pp)
# Obtener respuestas para la fila específica
respuestas_sp = worksheet.row_values(indice_fila)[15:30]
#st.write(respuestas_sp)


# PRIMERA PARTE

# Información de orientación
texto = """
##### FORMAS DE UBICARSE EN EL PENTÁGONO DE COMPETENCIAS

#### 1 - Ubicación por momentos:

"A continuación se exponen las preguntas presentes en el cuestionario y los momentos que corresponden a las respuestas dadas:"

- 1 - "¿Puedo usar las TIC por mí mismo?", "SI": "Explorador"
- 2 - "¿Utilizo las TIC en mis labores educativas cotidianas?", "SI": "Explorador"
- 3 - "¿Entiendo las implicaciones éticas del uso educativo de las TIC e inculco su uso responsable en mi comunidad educativa?", "SI": "Explorador"
- 4 - "¿Integro las TIC al quehacer pedagógico, al PEI y a la gestión institucional de manera pertinente?", "SI": "Explorador"
- 5 - "¿Combino diversidad de lenguajes y herramientas tecnológicas para diseñar ambientes de aprendizaje que respondan a las necesidades particulares de mi entorno?", "SI": "Explorador"]
- 6 - "¿Soy de los primeros en adoptar nuevas ideas provenientes de diversidad de fuentes?", "SI": "Integrador"
- 7 - "¿Tengo criterios para argumentar la forma en la que la integración de las TIC facilita el aprendizaje y mejora la gestión escolar?", "SI": "Integrador"
- 8 - "¿Comparto las actividades que realizo, discuto mis estrategias y hago ajustes utilizando la realimentación que me dan mis compañeros?", "NO":"Integrador"; "SI":"Innovador"

##### Pentágono de Competencias Digitales por Momentos
Para saber el momento o nivel en el que se encuentra; de exploración, integración o innovación debe seguir las preguntas en sentido horario, los puntos verdes indican las respuestas afirmativas o "SI" y los rojos las negativas o "NO".
El gráfico expuesto a continuación le dará una idea general de su nivel, recuerde que las competencias se pueden desarrollar de maneras diversas. Gráficamente vamos avanzando desde afuera hacia el centro, del nivel explorador al innovador. 
"""
st.markdown(texto)

# Etiquetas
preguntas = ['Uso autónomo',
             'Uso educativo cotidiano',
             'Implicaciones éticas',
             'Integra las TIC',
             'Combina lenguajes y herramientas',
             'Adopta nuevas ideas',
             'Argumenta',
             'Comparte actividades/estrategias']

# Convertir respuestas a números (1 para 'Si', 0 para 'No')
respuestas_numeros = [1 if respuesta == 'Si' else 0 for respuesta in respuestas_pp]

# Niveles de competencia
niveles = ['Innovador', 'Integrador', 'Explorador']

# Convertir respuestas a niveles
niveles_respuestas = [niveles[numero] for numero in respuestas_numeros]

# Asignar niveles específicos para cada pregunta (a modo de ejemplo)
niveles_preguntas = ['Explorador', 'Explorador', 'Explorador', 'Explorador', 'Integrador', 'Integrador', 'Integrador', 'Innovador']

# Crear un gráfico de radar con forma de pentágono
fig = go.Figure()

# Marcar las respuestas por 'Si' o 'No' en el nivel correspondiente
for i, nivel_respuesta in enumerate(niveles_respuestas):
    nivel_pregunta = niveles_preguntas[i]
    pregunta_actual = preguntas[i]  # Utilizamos la pregunta correspondiente
    respuesta_actual = respuestas_pp[i].strip()  # Eliminar espacios en blanco

    # Definir color según la respuesta
    color = 'green' if respuesta_actual == 'Si' else 'red'
   
    # Calcular la posición angular de la etiqueta
    theta = (360 / len(preguntas)) * i  # Se ajusta para el orden correcto

    # Agregar cada respuesta como un punto en el gráfico
    fig.add_trace(go.Scatterpolar(
        r=[niveles.index(nivel_pregunta) + 1],
        theta=[theta],
        mode='markers',
        marker=dict(color=color, size=20),
        name=f'{respuesta_actual}',  # Utilizamos solo el valor de la respuesta en la leyenda
        text=[pregunta_actual],  # Agregamos el nombre de la pregunta como etiqueta
        hoverinfo='text',  # Solo mostrar información de texto en el hover
    ))

    # Agregar etiquetas con un pequeño desplazamiento angular
    fig.add_annotation(
        x=1.3 * (niveles.index(nivel_pregunta) + 1),  # Multiplicamos por 1.3 para alejar las etiquetas del centro
        y=theta,
        text=pregunta_actual,
        showarrow=False,
        xanchor='center',
        yanchor='middle',
        textangle=0,  # Dejamos el texto horizontal
        font=dict(size=20)  # Reducimos el tamaño del texto
    )

# Agregar cada nivel como una capa en el gráfico
for i, nivel in enumerate(niveles):
    fig.add_trace(go.Scatterpolar(
        r=[niveles.index(nivel) + 1] * len(preguntas),
        theta=[(360 / len(preguntas)) * j for j in range(len(preguntas))],  # Se ajusta para el orden correcto
        fill='toself',
        name=nivel,  # Usamos los niveles como leyendas
        fillcolor='rgba(85, 85, 85, 0.1)' if i == 0 else 'rgba(100, 100, 100, 0.1)',  # Rojo para el primer nivel, verde para los demás
        line=dict(color='rgba(0, 0, 0, 0)'),  # Sin línea
        connectgaps=False  # Sin conectar los puntos
    ))

# Ajustar el margen del gráfico
fig.update_layout(
    margin=dict(l=150, r=200, t=100, b=100)
)

# Configurar diseño del gráfico con ajustes en la fuente de las etiquetas
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=False,
            range=[0, len(niveles) + 1]
        ),
        angularaxis=dict(
            tickmode='array',  # Establece el modo de las marcas de las etiquetas
            tickvals=[(360 / len(preguntas)) * i for i in range(len(preguntas))],  # Establece las ubicaciones de las marcas de las etiquetas
            ticktext=preguntas,  # Establece las etiquetas
            rotation=90,  # Ajustar la rotación de las etiquetas
            direction='clockwise',  # Dirección de las agujas del reloj
            tickfont=dict(size=12)  # Ajustar el tamaño de la fuente de las etiquetas
        )
    ),
    showlegend=True,
)

# Mover la caja de leyenda (referencias)
fig.update_layout(
    legend=dict(
        x=2.00,  # Mover % hacia la izquierda
        y=0.80,  # Mover % hacia arriba
        bgcolor='rgba(255, 255, 255, 0.5)',  # Color de fondo semitransparente
        bordercolor='rgba(0, 0, 0, 0.5)',  # Color del borde semitransparente
        borderwidth=1  # Ancho del borde
    )
)

# Aumentar el tamaño del gráfico
fig.update_layout(
    width=800,  # Ajusta el ancho del gráfico
    height=500,  # Ajusta la altura del gráfico
)

# Mostrar el gráfico
st.plotly_chart(fig)


# Información de devolución para los momentos
texto_dm = """
 
Las competencias se desarrollan y expresan en diferentes ***niveles o grados de complejidad***.

- El **primer nivel o momento de exploración**, se caracteriza por permitir el ***acercamiento*** a 
un conjunto de conocimientos que se constituyen en la posibilidad para acceder a estados de mayor elaboración conceptual. 
- En el **segundo nivel o momento de integración**, se plantea el uso de los conocimientos ya ***apropiados*** para
la resolución de problemas en contextos diversos. 
- Finalmente, en el **tercer nivel o momento de innovación**, se da mayor énfasis a los ***ejercicios de creación***; lo que permite ir más allá del
conocimiento aprendido e imaginar nuevas posibilidades de acción o explicación.

#### 1. Exploración
El momento de exploración es la primera aproximación a un mundo desconocido en el que
es muy apropiado imaginar, o traer a la mente cosas que no están presentes para nuestros
sentidos. Lo más importante del momento de exploración es romper con los miedos y prejuicios,
abrir la mente a nuevas posibilidades, soñar con escenarios ideales y conocer la
amplia gama de oportunidades que se abren con el uso de TIC en educación.
Durante el momento de ***Exploración*** los docentes:
- Se familiarizan poco a poco con el espectro de posibilidades – desde las básicas hasta las
más avanzadas - que ofrecen las TIC en educación.
- Empiezan a introducir las TIC en algunas de sus labores y procesos de enseñanza y aprendizaje.
- Reflexionan sobre las opciones que las TIC les brindan para responder a sus necesidades y a las de su contexto.
#### 2. Integración
Es en este segundo momento, en donde se desarrollan las capacidades para usar las TIC de
forma autónoma, los docentes están listos para desarrollar ideas que tienen valor a través
de la profundización y la integración creativa de las TIC en los procesos educativos. Los docentes
llegan con saberes y experiencias previas; al explorar en el primer momento descubren
el potencial de las TIC y a medida que van ganando confianza con las nuevas habilidades
adquiridas comienzan a generar ideas e introducir nuevas tecnologías en la planeación,
la evaluación y las prácticas pedagógicas.
En el momento de ***Integración*** los docentes:
- Saben utilizar las TIC para aprender, de manera no presencial, lo que les permite aprovechar
recursos disponibles en línea, tomar cursos virtuales, aprender con tutores a distancia y participar
en redes y comunidades de práctica.
- Integran las TIC en el diseño curricular, el PEI y la gestión institucional de manera pertinente.
- Entienden las implicaciones sociales de la inclusión de las TIC en los procesos educativos.
#### 3. Innovación
El momento de innovación se caracteriza por poner nuevas ideas en práctica, usar las TIC
para crear, para expresar sus ideas, para construir colectivamente nuevos conocimientos y para
construir estrategias novedosas que le permitan reconfigurar su práctica educativa. Es un momento
en el que los docentes sienten confianza en sí mismos, están cómodos al cometer errores
mientras aprenden e inspiran en sus estudiantes el deseo de ir más allá de lo conocido.
En el momento de ***Innovación*** los docentes:
- Son capaces de adaptar y combinar una diversidad de lenguajes y de herramientas tecnológicas
para diseñar ambientes de aprendizaje o de gestión institucional que respondan a las necesidades particulares de su entorno.
- Están dispuestos a adoptar y adaptar nuevas ideas y modelos que reciben de diversidad de fuentes.
- Comparten las actividades que realizan con sus compañeros y discuten sus estrategias recibiendo realimentación que utilizan para hacer ajustes pertinentes a sus prácticas educativas.
- Tienen criterios para argumentar la forma en que la integración de las TIC cualifica los procesos de enseñanza y aprendizaje y mejora la gestión institucional.

Cada una de las competencias del pentágono es fundamental tanto para los docentes como para los directivos docentes. 
Sin embargo, la forma en que se expresan las competencias puede variar dependiendo del momento o nivel de desarrollo 
en el que los docentes se encuentren, su rol, la disciplina que enseñan, el nivel en el que se desempeñan, sus intereses
y sus talentos.
"""
st.markdown(texto_dm)

####################################################################################
####################################################################################

# Información de introducción a competencias
texto_comp = """
#### 2 - Ubicación por competencias:

##### NIVELES DE COMPETENCIA

A continuación, se muestran los Niveles de Competencia obtenidos en cada una de las mismas y su gráfico respectivo.
Además, se  brinda la caracterización de las competencias, indicando el descriptor de
nivel de competencia para cada uno de los momentos. 
"""
st.markdown(texto_comp)

# Define las competencias
nombre_competencia = {
    'CT': 'Tecnológica',
    'CP': 'Pedagógica',
    'CC': 'Comunicativa',
    'CG': 'De Gestión',
    'CI': 'Investigativa'
}

# Define las columnas relevantes para cada competencia
competencia_columns = {
    'CT': list(range(16, 19)),
    'CP': list(range(19, 22)),
    'CC': list(range(22, 25)),
    'CG': list(range(25, 28)),
    'CI': list(range(28, 31))
}

# Ajustar la definición de las competencias
competencia_indices = {
    'CT': [0, 1, 2],
    'CP': [3, 4, 5],
    'CC': [6, 7, 8],
    'CG': [9, 10, 11],
    'CI': [12, 13, 14]
}

definicion_competencia = {
    'CT': 'Capacidad para seleccionar y utilizar de forma pertinente, responsable y eficiente una variedad de herramientas tecnológicas entendiendo los principios que las rigen, la forma de combinarlas y las licencias que las amparan.',
    'CP': 'Capacidad de utilizar las TIC para fortalecer los procesos de enseñanza y aprendizaje, reconociendo alcances y limitaciones de la incorporación de estas tecnologías en la formación integral de los estudiantes y en su propio desarrollo profesional.',
    'CC': 'Capacidad para expresarse, establecer contacto y relacionarse en espacios virtuales y audiovisuales a través de diversos medios y con el manejo de múltiples lenguajes, de manera sincrónica y asincrónica.',
    'CG': 'Capacidad para utilizar las TIC en la planeación, organización, administración y evaluación de manera efectiva de los procesos educativos; tanto a nivel de prácticas pedagógicas como de desarrollo institucional.', 
    'CI': 'Capacidad de utilizar las TIC para la transformación del saber y la generación de nuevos conocimientos.'
}

# Diccionario para almacenar los niveles de competencia por cada competencia
niveles_competencia = {}

# Diccionario de devoluciones según la competencia y nivel
devoluciones = {
    1: {
        1: "Reconoce un amplio espectro de herramientas tecnológicas y algunas formas de integrarlas a la práctica educativa.",
        2: "Utiliza diversas herramientas tecnológicas en los procesos educativos, de acuerdo a su rol, área de formación, nivel y contexto en el que se desempeña.",
        3: "Aplica el conocimiento de una amplia variedad de tecnologías en el diseño de ambientes de aprendizaje innovadores y para plantear soluciones a problemas identificados en el contexto.",
     },
    2: {
        1: "Identifica nuevas estrategias y metodologías mediadas por las TIC, como herramienta para su desempeño profesional.",
        2: "Propone proyectos y estrategias de aprendizaje con el uso de TIC para potenciar el aprendizaje de los estudiantes.",
        3: "Lidera experiencias significativas que involucran ambientes de aprendizaje diferenciados de acuerdo a las necesidades e intereses propias y de los estudiantes.",
    },
    3: {
        1: "Emplea diversos canales y lenguajes propios de las TIC para comunicarse con la comunidad educativa.",
        2: "Desarrolla estrategias de trabajo colaborativo en el contexto escolar a partir de su participación en redes y comunidades con el uso de las TIC.",
        3: "Participa en comunidades y publica sus producciones textuales en diversos espacios virtuales y a través de múltiples medios digitales usando los lenguajes que posibilitan las TIC.",
    },
    4: {
        1: "Organiza actividades propias de su quehacer profesional con el uso de las TIC.",
        2: "Integra las TIC en procesos de dinamización de las gestiones directiva, académica, administrativa y comunitaria de su institución.",
        3: "Propone y lidera acciones para optimizar procesos integrados de la gestión escolar.",
    },
    5: {
        1: "Usa las TIC para hacer registro y seguimiento de lo que vive y observa en su práctica, su contexto y el de sus estudiantes.",
        2: "Lidera proyectos de investigación propia y con sus estudiantes.",
        3: "Construye estrategias educativas innovadoras que incluyen la generación colectiva de conocimientos.",
    }
}

# Diccionario de colores según la competencia
colores_competencia = {
    1: "darkgreen",
    2: "orange",
    3: "violet",
    4: "olive",
    5: "turquoise"
}

# Obtener la devolución basada en la competencia y nivel
def obtener_devolucion(competencia, nivel_competencia):
    try:
        devolucion = devoluciones[competencia][nivel_competencia]
    except KeyError:
        devolucion = "Nivel o competencia desconocida"
    return devolucion

# Calcular y almacenar los niveles directamente en las columnas correspondientes (32 a 37)
for competencia, indices in competencia_indices.items():
    valores_competencia = [int(respuestas_sp[indice][0]) for indice in indices]
    counter = Counter(valores_competencia)
    max_repeated_value, max_repeated_count = counter.most_common(1)[0]  # Obtiene el valor más repetido y su conteo
    
    # Si hay repeticiones, usa el valor más repetido, de lo contrario, usa 2
    nivel_competencia = max_repeated_value if max_repeated_count > 1 else 2
 
    columna_actual = 32 + list(competencia_indices.keys()).index(competencia)  # 32 para la primera competencia, 33 para la segunda, y así sucesivamente

    # Guardar el nivel de competencia en el diccionario
    niveles_competencia[competencia] = nivel_competencia

    # Actualizar la celda con el nivel de competencia calculado
    try:
        worksheet.update_cell(indice_fila, columna_actual, nivel_competencia)
        print(f"Actualizada celda en fila {indice_fila}, columna {columna_actual} con nivel {nivel_competencia}")
    except Exception as e:
        st.error(f"Error al actualizar la celda en la fila {indice_fila}, columna {columna_actual}: {e}")
        print(f"Error al actualizar celda: {e}")

    # Obtener la devolución y el color para la competencia actual
    devolucion = obtener_devolucion(list(competencia_columns.keys()).index(competencia)+1, nivel_competencia)
    color = colores_competencia.get(list(competencia_columns.keys()).index(competencia)+1, "black")
    definicion = definicion_competencia.get(competencia, "Definición no disponible.")

    # Mostrar la devolución con el color correspondiente y la definición
    st.markdown(f"<p style='color:{color};'><strong>Nivel de Competencia {nombre_competencia[competencia]} <p>{definicion}</p> ({competencia}):</strong> Nivel de Competencia obtenido - {nivel_competencia} - {devolucion}</p>", unsafe_allow_html=True)

# Almacenar los niveles de competencias en una lista
niveles_generales = list(niveles_competencia.values())

# Obtener los valores más repetidos
counter_general = Counter(niveles_generales)
max_repeated_count = max(counter_general.values(), default=0)

# Filtrar los valores que se repiten con mayor frecuencia
most_repeated_values = [value for value, count in counter_general.items() if count == max_repeated_count]

# Tomar el valor más alto entre los que se repiten más veces
nivel_general = max(most_repeated_values, default=3)

# Actualizar la celda con el nivel general de competencias calculado
try:
    columna_nivel_general = 37  # Ajusta este valor según la columna deseada
    worksheet.update_cell(indice_fila, columna_nivel_general, nivel_general)
except Exception as e:
    st.error(f"Error al actualizar la celda en la fila {indice_fila}, columna {columna_nivel_general}: {e}")

# Mostrar el nivel general de competencias
st.markdown('***')
st.text(f"Nivel de Competencias General (NCG): {nivel_general}")
st.markdown('***')

#Aclaración
st.text("Para obtener información más detallada del gráfico puede acercar el puntero del ratón")
  
##############################################################

# Competencias y niveles
competencias = ['CT', 'CP', 'CC', 'CG', 'CI']
niveles = niveles_generales

fig = go.Figure()

# Define colores para cada competencia
colores_competencias = {
    'CT': 'darkgreen',
    'CP': 'orange',
    'CC': 'violet',
    'CG': 'olive',
    'CI': 'turquoise'
}

# Aumentamos el tamaño de los puntos
tamaño_puntos = 20

# Define los nombres de los niveles y sus valores
nombres_niveles = ["Explorador", "Integrador", "Innovador"]
valores_niveles = [1, 2, 3]  # Suponiendo que los niveles van de 1 a 3

# Colores de los niveles con opacidad reducida
colores_niveles = ['rgba(0,0,0,0.05)', 'rgba(0,0,0,0.1)', 'rgba(0,0,0,0.2)']

# Agrega áreas radiales para los niveles
for nombre, valor, color in zip(nombres_niveles[::-1], valores_niveles[::-1], colores_niveles[::-1]):
    fig.add_trace(go.Scatterpolar(
        r=[valor] * len(competencias),
        theta=competencias + [competencias[0]],
        mode='lines',
        line=dict(color=color, width=2),
        name=nombre,
        connectgaps=True,
        fill='toself',  # Esto asegura que el área cubierta por las líneas esté llenada
        fillcolor=color,  # Color del área llenada
        subplot='polar'  # Asegura que las áreas estén en la misma capa que las líneas de colores
    ))


# Agrega las líneas que conectan los puntos de las respuestas
for i, competencia in enumerate(competencias):
    if i < len(competencias) - 1:
        siguiente_competencia = competencias[i + 1]
    else:
        siguiente_competencia = competencias[0] 
    fig.add_trace(go.Scatterpolar(
        r=[niveles[i], niveles[(i + 1) % len(competencias)]],  # Conecta con el siguiente nivel (o el primero si es el último)
        theta=[competencia, siguiente_competencia],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False  # Ocultar líneas en la leyenda
    ))


# Gira los puntos 180 grados y agrégalos
for competencia, color in colores_competencias.items():
    nivel = niveles_generales[competencias.index(competencia)]
    
    # Calcula la nueva posición angular (giro de 180 grados)
    index = competencias.index(competencia)
    nueva_posicion_angular = (index) % len(competencias)  # 2 posiciones adelante en una lista circular
    nueva_competencia = competencias[nueva_posicion_angular]

    fig.add_trace(go.Scatterpolar(
        r=[nivel],
        theta=[nueva_competencia],
        mode='markers',  # Mostrar solo los puntos
        marker=dict(color=color, size=tamaño_puntos, line=dict(color='white', width=2)),  # Configura el tamaño y el contorno del marcador
        name=f"Nivel de {competencia}"
    ))

# Configuración del diseño
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=False,
            range=[0, max(niveles) + 1]
        ),
        angularaxis=dict(
            direction='clockwise',
            rotation=90,
            tickmode='array'
        )
    ),
    showlegend=True
)

# Mostrar el gráfico
st.plotly_chart(fig)
