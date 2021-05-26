import numpy as np
import pandas as pd
import streamlit as st
import random
import time

# Funciones
def buildCell(url, img, tit):
    prefix_url, suffix_url = '<a href=\"', '\" target=\"_blank\">'
    prefix_img, suffix_img = '<img src=\"', '\" style=\"width:100%;\">'
    prefix_tit, suffix_tit = '<div>', '</div></a>'
    #tit = tit[:33] + '...'
    return prefix_url + url + suffix_url + prefix_img + img + suffix_img + prefix_tit + tit + suffix_tit

def buildPlanner(planner, df, indexes_list):
    htmls = []
    for i in indexes_list:
        htmls.append(buildCell(df.at[i, 'URL'], df.at[i, 'Imagen'], df.at[i, 'Título']))
    
    i = 0
    for index in planner.index:
        for column in planner.columns:
            planner.at[index, column] = htmls[i]
            i += 1

# Datos estáticos
estilo = 'style=\"color:grey;font-size:13px\"'
etiquetas = ['','#Ácido','#Algrill','#Aliño','#Alvapor','#AlvaporconVaroma','#Andalucía','#Aperitivo','#Arroz','#Aves','#Bajoengrasas','#Barbacoa','#Buffet','#Caliente','#Carne','#CasaRural','#Cerdo','#Cereales','#Cocciónlenta','#Cocinaenniveles','#Cocinarparamuchos(6+)','#Comidaexótica','#Comidainfantil','#Comidaparallevar','#Conniñosenlacocina','#Contienealcohol','#Contienecrustáceos','#Contienegluten','#Contienelactosa','#Contienemoluscos','#Contienesoja','#Contienesésamo','#Cremasypurés','#Crujiente','#Cumpleaños','#Dulce','#DíadelPadre','#DíadelaMadre','#Díadelosabuelos','#En20minutos','#En30minutos','#Enfriar','#Ensaladas','#Entrante','#España','#Europa','#Fiesta','#Francia','#Freír','#Frutas','#Frutossecos','#Frío','#Guarnición','#Guisosyestofados','#Hazlotumismo','#Hornear','#Huevo','#India','#Inspirador','#Invierno','#Invitados','#Italia','#Japón','#Legumbres','#Ligeras','#Marisco','#Mediterráneo','#Menosde30minutos','#Navidad','#Nochevieja','#Oriental','#Otoño','#Para2','#Paradeportistas','#Paraestudiantes','#Parallevar','#Parapersonasmayores','#Pasta','#Patatas','#Pescado','#Picante','#Picnic','#Plancha','#Portugal','#Primavera','#Realfood','#Recetasen3pasos','#Sabroso','#Salado','#Salsas','#Saltear','#SemanaSanta','#Sinalcohol','#Sinazúcar','#Sinfrutossecos','#Singluten','#Sinhuevos','#Sinlactosa','#Snack','#Sopas','#Suave','#Templado','#Tendencia','#Ternera','#Umami','#Vacaciones','#Vegano','#Vegetales','#Vegetariana','#Verano','#Verduras']
#etiquetas_top = ['#Carne','#Pescado','#Verduras','#Sinlactosa','#Sinhuevos','#Vegetariana','#Vegetales','#Singluten','#Legumbres','#Arroz','#Pasta','#Sopas','#Cereales','#Ensaladas','#Vegano','#Bajoengrasas','#Realfood']

# Inicio de la página
st.markdown('<h1><font color=\"green\">cook.IA</font></h1>', unsafe_allow_html=True)
st.markdown('<h2><font color=\"green\">Tu Planificador <i>Inteligente</i> e <i>Interactivo</i></font></h2>', unsafe_allow_html=True)
st.write('')
st.subheader('¡Que no decidan por ti! Vamos a buscar 14 platos para chuparse los dedos:')
st.write('')

# Filtros
list_kcal = list(range(0, 800, 50))
list_kcal = [str(x) for x in list_kcal] + ['+750']
slider_kcal = st.select_slider('¿Cuántas calorías por plato?', options=list_kcal, value=['250', '500'])
tm = st.radio('Modelo de la máquina', ['TM6', 'TM5', 'TM31'])

st.write('')
st.write('')
st.write('')
st.info('Filtra entre más de 100 etiquetas... 👌🏻')

label1 = st.selectbox('Etiqueta 1 (opcional)', etiquetas)
label2 = st.selectbox('Etiqueta 2 (opcional)', etiquetas)

st.write('')
st.write('')
st.write('')
st.info('Marca la casilla de abajo si no quieres dejar el más mínimo detalle al azar... 👇🏻')
sibarita = st.checkbox('Sólo para sibaritas de la planificación')
if sibarita:
    slider_val, empty1, slider_pop = st.beta_columns(3)
    with slider_val:
        slider_val = st.slider('Valoración mínima', 0.0, 5.0, 3.5, 0.5)
    with empty1:
        empty1 = st.empty()
    with slider_pop:
        slider_pop = st.select_slider('Popularidad mínima', options=['Baja', 'Media', 'Alta', 'Muy alta'], value='Baja')
    
    slider_dif, empty2, slider_minp, empty3, slider_mint = st.beta_columns(5)
    with slider_dif:
        slider_dif = st.select_slider('Dificultad', options=['fácil', 'medio', 'avanzado'], value=['fácil', 'avanzado'])
    with empty2:
        empty2 = st.empty()
    with slider_minp:
        slider_minp = st.select_slider('Minutos de preparación', options=['5', '10', '15', '20', '+20'], value=['5', '+20'])
    with empty3:
        empty3 = st.empty()
    with slider_mint:
        slider_mint = st.select_slider('Minutos en total', options=['5', '30', '45', '70', '+70'], value=['5', '+70'])
    
    friend = st.checkbox('Thermomix Friend')

st.write('')
st.write('')
st.write('')
if st.button('🍽️ Quiero mi menú! 😋'):
    # Carga de datos
    df = pd.read_pickle('./data/df.pkl')
    #df_ingrs = pd.read_pickle('./data/df_ingrs.pkl')
    #df_ingrs_relevance = pd.read_pickle('./data/df_ingrs_relevance.pkl')
    #similarity = np.load('./data/similarity.dat', allow_pickle=True)
    #topN_matrix = pd.read_pickle('./data/topN_matrix.dat')

    # Preparación de filtros
    slider_kcal_int = [float(x) for x in slider_kcal]
    slider_kcal_int[0] = 750.01 if slider_kcal[0] == '+750' else slider_kcal_int[0]
    slider_kcal_int[1] = df.kcal.max() if slider_kcal[1] == '+750' else slider_kcal_int[1]

    label1 = [''] if label1 == [] else label1
    label2 = [''] if label2 == [] else label2

    if sibarita:
        if slider_pop == 'Baja':
            slider_pop_list = ['Muy alta', 'Alta', 'Media', 'Baja']
        elif slider_pop == 'Media':
            slider_pop_list = ['Muy alta', 'Alta', 'Media']
        elif slider_pop == 'Alta':
            slider_pop_list = ['Muy alta', 'Alta']
        else:
            slider_pop_list = ['Muy alta']
        
        if slider_dif == ('fácil', 'avanzado'):
            slider_dif_list = ['fácil', 'medio', 'avanzado']
        else:
            slider_dif_list = slider_dif
        
        slider_minp_int = [int(x) for x in slider_minp]
        slider_minp_int[0] = 21 if slider_minp[0] == '+20' else slider_minp_int[0]
        slider_minp_int[1] = df.TiempoPreparación.max() if slider_minp[1] == '+20' else slider_minp_int[1]

        slider_mint_int = [int(x) for x in slider_mint]
        slider_mint_int[0] = 71 if slider_mint[0] == '+70' else slider_mint_int[0]
        slider_mint_int[1] = df.TiempoTotal.max() if slider_mint[1] == '+70' else slider_mint_int[1]

        friend_val = [0, 1] if friend else [0]
    else:
        slider_val = '3.5'
        slider_pop_list = ['Muy alta', 'Alta', 'Media', 'Baja']
        slider_dif_list = ['fácil', 'medio', 'avanzado']
        slider_minp_int = [5, df.TiempoPreparación.max()]
        slider_mint_int = [5, df.TiempoTotal.max()]
        friend_val = [0]
    
    # Filtrado de recetas válidas
    indexes = list(df[(df.kcal.between(slider_kcal_int[0], slider_kcal_int[1])) &
    (df[tm] == 1) &
    (df.Etiquetas.str.contains(label1)) &
    (df.Etiquetas.str.contains(label2)) &
    (df.Valoración.between(float(slider_val), 5)) &
    (df.CategoríaPopularidad.isin(slider_pop_list)) &
    (df.Dificultad.isin(slider_dif_list)) &
    (df.TiempoPreparación.between(slider_minp_int[0], slider_minp_int[1])) &
    (df.TiempoTotal.between(slider_mint_int[0], slider_mint_int[1])) &
    (df.ThermomixFriend.isin(friend_val))].index)
    
    # Resultado de la planificación
    if len(indexes) >= 14:

        if len(indexes) >= 98:
            st.success('Perfecto! :sunglasses: En la variedad está el gusto: ' + str(len(indexes)) + ' recetas encajan!')
        else:
            st.warning('Uy! Sólo ' + str(len(indexes)) + ' recetas encajan. ' +
            'Para la semana que viene relaja tus preferencias o repetirás platos...')
        
        with st.spinner('Sirviendo menú semanal...'):
            time.sleep(2)
            planner = pd.DataFrame(columns=['Comida','Cena'], index=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])
            random.shuffle(indexes)
            planificacion = indexes[:14]
            buildPlanner(planner, df, planificacion)
        
        st.success('Vualaaá!')
        st.write(planner.to_html(escape=False), unsafe_allow_html=True)
        #st.balloons()
    else:
        st.error('Me temo que has sido muy estricto conmigo... No puedo ofrecerte ningún menú semanal. ' +
        'Por favor, vuelve a ajustar tus preferencias y lo intento de nuevo')
        st.stop()
