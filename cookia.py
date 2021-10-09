import numpy as np
import pandas as pd
import pyrebase
import streamlit as st
import random
import time

# Funciones
def main_cookia():
    # Datos estáticos
    estilo = 'style=\"color:grey;font-size:13px\"'
    etiquetas = ['','#Ácido','#Algrill','#Aliño','#Alvapor','#AlvaporconVaroma','#Andalucía','#Aperitivo','#Arroz','#Aves','#Bajoengrasas','#Barbacoa','#Buffet','#Caliente','#Carne','#CasaRural','#Cerdo','#Cereales','#Cocciónlenta','#Cocinaenniveles','#Cocinarparamuchos(6+)','#Comidaexótica','#Comidainfantil','#Comidaparallevar','#Conniñosenlacocina','#Contienealcohol','#Contienecrustáceos','#Contienegluten','#Contienelactosa','#Contienemoluscos','#Contienesoja','#Contienesésamo','#Cremasypurés','#Crujiente','#Cumpleaños','#Dulce','#DíadelPadre','#DíadelaMadre','#Díadelosabuelos','#En20minutos','#En30minutos','#Enfriar','#Ensaladas','#Entrante','#España','#Europa','#Fiesta','#Francia','#Freír','#Frutas','#Frutossecos','#Frío','#Guarnición','#Guisosyestofados','#Hazlotumismo','#Hornear','#Huevo','#India','#Inspirador','#Invierno','#Invitados','#Italia','#Japón','#Legumbres','#Ligeras','#Marisco','#Mediterráneo','#Menosde30minutos','#Navidad','#Nochevieja','#Oriental','#Otoño','#Para2','#Paradeportistas','#Paraestudiantes','#Parallevar','#Parapersonasmayores','#Pasta','#Patatas','#Pescado','#Picante','#Picnic','#Plancha','#Portugal','#Primavera','#Realfood','#Recetasen3pasos','#Sabroso','#Salado','#Salsas','#Saltear','#SemanaSanta','#Sinalcohol','#Sinazúcar','#Sinfrutossecos','#Singluten','#Sinhuevos','#Sinlactosa','#Snack','#Sopas','#Suave','#Templado','#Tendencia','#Ternera','#Umami','#Vacaciones','#Vegano','#Vegetales','#Vegetariana','#Verano','#Verduras']
    #etiquetas_top = ['#Carne','#Pescado','#Verduras','#Sinlactosa','#Sinhuevos','#Vegetariana','#Vegetales','#Singluten','#Legumbres','#Arroz','#Pasta','#Sopas','#Cereales','#Ensaladas','#Vegano','#Bajoengrasas','#Realfood']

    form_main = form_main_container.form("form_main")
    form_main.write('')
    form_main.subheader('¡Que no decidan por ti! Vamos a buscar 14 platos para chuparse los dedos:')
    form_main.write('')

    # Filtros
    list_kcal = list(range(0, 800, 50))
    list_kcal = [str(x) for x in list_kcal] + ['+750']
    form_main.select_slider('¿Cuántas calorías por plato?', options=list_kcal, value=['250', '500'], key='slider_kcal')

    cols_maquinas = form_main.columns(5)
    tm = cols_maquinas[1].radio('Modelo de la máquina', ['TM6', 'TM5', 'TM31'], key='tm')
    friend = cols_maquinas[3].checkbox('¿Tienes un Thermomix Friend?', key='friend')

    form_main.write('')
    form_main.write('')
    form_main.write('')
    form_main.info('Filtra entre más de 100 etiquetas... 👌🏻 Las 10 etiquetas más usadas son: #Otoño, #Invierno, #Cocinarparamuchos(6+), #Primavera, #Inspirador, #Rápido, #Verano, #Carne, #Pescado, #Verduras')
    
    label1 = form_main.selectbox('Etiqueta (opcional)', etiquetas, key='label1')
    #label2 = form_main.selectbox('Etiqueta 2 (opcional)', etiquetas, key='label2')

    form_main.write('')
    form_main.write('')
    form_main.write('')
    expander_sibarita = form_main.expander('Sólo para sibaritas de la planificación... (pulsa el símbolo \'+\') 👉🏻')
    if expander_sibarita:
        slider_val = expander_sibarita.slider('Valoración mínima', 0.0, 5.0, 3.5, 0.5)

        cols_sibarita1 = expander_sibarita.columns(3)
        slider_pop = cols_sibarita1[0].select_slider('Popularidad mínima', options=['Baja', 'Media', 'Alta', 'Muy alta'], value='Baja')
        slider_dif = cols_sibarita1[2].select_slider('Dificultad', options=['fácil', 'medio', 'avanzado'], value=['fácil', 'avanzado'], key='dif')

        cols_sibarita2 = expander_sibarita.columns(3)
        slider_minp = cols_sibarita2[0].select_slider('Minutos de preparación', options=['5', '10', '15', '20', '+20'], value=['5', '+20'], key='minp')
        slider_mint = cols_sibarita2[2].select_slider('Minutos en total', options=['5', '30', '45', '70', '+70'], value=['5', '+70'], key='mint')

    form_main.write('')
    form_main.write('')
    form_main.write('')
    if form_main.form_submit_button('🍽️ Quiero mi menú! 😋'):
        # Carga de datos
        df = pd.read_pickle('./data/df.pkl')
        #df_ingrs = pd.read_pickle('./data/df_ingrs.pkl')
        #df_ingrs_relevance = pd.read_pickle('./data/df_ingrs_relevance.pkl')
        #similarity = np.load('./data/similarity.dat', allow_pickle=True)
        #topN_matrix = pd.read_pickle('./data/topN_matrix.dat')

        # Preparación de filtros
        slider_kcal_int = [float(x) for x in st.session_state.slider_kcal]
        slider_kcal_int[0] = 750.01 if st.session_state.slider_kcal[0] == '+750' else float(st.session_state.slider_kcal[0])
        slider_kcal_int[1] = df.kcal.max() if st.session_state.slider_kcal[1] == '+750' else float(st.session_state.slider_kcal[1])

        label1 = [''] if label1 == [] else label1
        #label2 = [''] if label2 == [] else label2

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

        #slider_val = '3.5'
        #slider_pop_list = ['Muy alta', 'Alta', 'Media', 'Baja']
        #slider_dif_list = ['fácil', 'medio', 'avanzado']
        #slider_minp_int = [5, df.TiempoPreparación.max()]
        #slider_mint_int = [5, df.TiempoTotal.max()]
        #friend_val = [0]
        
        # Filtrado de recetas válidas
        indexes = list(df[(df.kcal.between(slider_kcal_int[0], slider_kcal_int[1])) &
        (df[tm] == 1) &
        (df.Etiquetas.str.contains(label1)) &
        #(df.Etiquetas.str.contains(label2)) &
        (df.Valoración.between(float(slider_val), 5)) &
        (df.CategoríaPopularidad.isin(slider_pop_list)) &
        (df.Dificultad.isin(slider_dif_list)) &
        (df.TiempoPreparación.between(slider_minp_int[0], slider_minp_int[1])) &
        (df.TiempoTotal.between(slider_mint_int[0], slider_mint_int[1])) &
        (df.ThermomixFriend.isin(friend_val))].index)
        
        # Resultado de la planificación
        if len(indexes) >= 14:

            if len(indexes) >= 98:
                form_main.success('Perfecto! :sunglasses: En la variedad está el gusto: ' + str(len(indexes)) + ' recetas encajan!')
            else:
                form_main.warning('Uy! Sólo ' + str(len(indexes)) + ' recetas encajan. ' +
                'Para la semana que viene relaja tus preferencias o repetirás platos...')
            
            with st.spinner('Sirviendo menú semanal...'):
                time.sleep(2)
                planner = pd.DataFrame(columns=['Comida','Cena'], index=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])
                random.shuffle(indexes)
                planificacion = indexes[:14]
                buildPlanner(planner, df, planificacion)
                lista_de_la_compra = buildBuyList(df, planificacion)
            
            form_main.success('Vualaaá!')
            form_main.write(planner.to_html(escape=False), unsafe_allow_html=True)
            form_main.balloons()

            cols_botones = st.columns(3)
            fichero_descarga = '<h1>Resultado del planificador semanal:</h1><br>' + planner.to_html(escape=False) + lista_de_la_compra
            cols_botones[1].download_button(label="Descarga esta planificación y la lista de la compra", data=fichero_descarga, file_name='cookia_planificación.html')
        else:
            form_main.error('Me temo que has sido muy estricto conmigo... No puedo ofrecerte ningún menú semanal. ' +
            'Por favor, vuelve a ajustar tus preferencias y lo intento de nuevo')
            st.stop()

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

def buildBuyList(df, indexes_list):
    all_ingrs = set()
    buy_list = '<h1>Lista de la compra resumida:</h1><br>'
    ingrs_list = ['Ingr0','Ingr1','Ingr2','Ingr3','Ingr4','Ingr5','Ingr6','Ingr7','Ingr8','Ingr9','Ingr10','Ingr11','Ingr12','Ingr13','Ingr14','Ingr15']
    
    for i in indexes_list:
        for j in ingrs_list:
            if pd.notna(df.at[i, j]):
                all_ingrs.add(df.at[i, j])
    all_ingrs = sorted(all_ingrs, key=str.lower)
    for ingr in all_ingrs:
        buy_list += ingr + '<br>'
    
    buy_list += '<br><h1>Lista de la compra detallada:</h1><br>'
    ingredients_list = ['Ingrediente0','Ingrediente1','Ingrediente2','Ingrediente3','Ingrediente4','Ingrediente5','Ingrediente6','Ingrediente7',
            'Ingrediente8','Ingrediente9','Ingrediente10','Ingrediente11','Ingrediente12','Ingrediente13','Ingrediente14','Ingrediente15']
    
    contador = 1
    for i in indexes_list:
        buy_list += '<h3>Plato ' + str(contador) + ':</h3><br>'
        for j in ingredients_list:
            if pd.notna(df.at[i, j]):
                buy_list += df.at[i, j] + '<br>'
        contador += 1
    
    return buy_list

def sidebar_options():
    if choice == 'Iniciar sesión':
        form_login = form_login_container.form("form_login_key", clear_on_submit=True)
        email = form_login.text_input('Correo electrónico')
        password = form_login.text_input('Contraseña',type = 'password')
        if form_login.form_submit_button('Inicia sesión'):
            try:
                st.session_state.user = st.session_state.auth.sign_in_with_email_and_password(email, password)
                username = st.session_state.db.child(st.session_state.user['localId']).child("username").get().val()
                st.session_state.user_info = st.session_state.auth.get_account_info(st.session_state.user['idToken'])
                if not st.session_state.user_info['users'][0]['emailVerified']:
                    #user = auth.refresh(user['refreshToken'])
                    st.session_state.auth.send_email_verification(st.session_state.user['idToken'])
                    st.sidebar.success('Hola de nuevo, ' + username +
                                        '! Te hemos reenviado el correo para que puedas verificar tu cuenta ' + 
                                        '(recuerda revisar tu bandeja de spam o correo no deseado)')
                else:
                    st.sidebar.info('Bienvenido/a, ' + username + ', a la familia!')
            except:
                st.sidebar.error('Ups! Ha habido un problema al iniciar sesión')
    elif choice == 'Registrarse':
        form_signup = form_signup_container.form("form_signup_key", clear_on_submit=True)
        email = form_signup.text_input('Correo electrónico')
        password = form_signup.text_input('Contraseña', type = 'password')
        password2 = form_signup.text_input(' Repetir contraseña', type = 'password')
        username = form_signup.text_input('Hola, soy cookia, ¿cuál es tu nombre?')
        if form_signup.form_submit_button('Registrarse'):
            import re
            #if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                st.sidebar.error('La dirección de correo electrónico no es válida. Por favor, corrígela')
            elif username == '':
                st.sidebar.error('Has dejado vacío el nombre de usuario. Adelante, no seas tímid@!')
            elif password != password2:
                st.sidebar.error('Las contraseñas que has introducido no coinciden. Corrígelas, por favor')
            else:
                try:
                    st.session_state.user = st.session_state.auth.create_user_with_email_and_password(email, password)
                    if st.session_state.user:
                        st.session_state.auth.send_email_verification(st.session_state.user['idToken'])
                        st.session_state.db.child(st.session_state.user['localId']).child("username").set(username)
                        st.session_state.db.child(st.session_state.user['localId']).child("ID").set(st.session_state.user['localId'])
                        st.sidebar.success('Estupendo, ' + username + '! Te hemos enviado un correo para que puedas completar tu registro ' + 
                                                                        '(recuerda revisar tu bandeja de spam o correo no deseado)')
                        st.sidebar.balloons()
                except:
                    st.sidebar.error('Ups! Ha habido un problema al registrar tu cuenta')
    elif choice == 'Olvidé mi contraseña':
        form_restore = form_restore_container.form("form_restore_key", clear_on_submit=True)
        email = form_restore.text_input('Correo electrónico')
        if form_restore.form_submit_button('Envíame un email'):
            try:
                if st.session_state.auth.send_password_reset_email(email):
                    st.sidebar.info('Listo! Te hemos enviado un correo para restaurar tu contraseña')
            except:
                st.sidebar.error('Ups! Ha habido un problema al restaurar la contraseña. Por favor, inténtalo de nuevo')

# Configuration Key
st.session_state.firebaseConfig = {
    'apiKey': st.secrets['apiKey'],
    'authDomain': st.secrets['authDomain'],
    'projectId': st.secrets['projectId'],
    'databaseURL': st.secrets['databaseURL'],
    'storageBucket': st.secrets['storageBucket'],
    'messagingSenderId': st.secrets['messagingSenderId'],
    'appId': st.secrets['appId'],
    'measurementId': st.secrets['measurementId']
}

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Mi web: https://buymeacoffee.com/cookia
st.session_state.coffee = '<a href="https://www.buymeacoffee.com/cookia" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Invítanos a una tapa&emoji=🍤&slug=cookia&button_colour=1e90ff&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00"></a>'

# Inicio de la página
cols_coffee = st.columns(3)
cols_coffee[2].markdown(st.session_state.coffee, unsafe_allow_html=True)
cols_logo = st.columns(3)
cols_logo[0].image('.streamlit/logo.png')

st.header('Tu Planificador Inteligente e Interactivo')
st.markdown('<i>cookia</i> nace con el deseo de aportar un enfoque innovador a la hora de planificar tu próximo plato entre miles de recetas <i>Thermomix</i>. ' + 
            'Encuentra de forma eficaz los menús más apropiados al rango de calorías que desees, añade alguna etiqueta entre más de un centenar, filtra por popularidad o tiempo de elaboración... ' + 
            '<br><br>Explora la variedad de recetas disponibles e invítanos a una tapa en el botón de arriba 👆🏻 para poder comentarnos qué nuevas funcionalidades te gustaría que añadamos próximamente!', unsafe_allow_html=True)
st.markdown('👈🏻 <i>Pulsa la flecha arriba a la izquierda y se desplegará el panel para registrarte/iniciar sesión.</i>', unsafe_allow_html=True)

choice_container = st.sidebar.empty()
form_login_container = st.sidebar.empty()
form_signup_container = st.sidebar.empty()
form_restore_container = st.sidebar.empty()
form_logout_container = st.sidebar.empty()
form_main_container = st.empty()

# Firebase Authentication and database instance
if 'firebase' not in st.session_state:
    st.session_state.firebase = pyrebase.initialize_app(st.session_state.firebaseConfig)
    st.session_state.auth = st.session_state.firebase.auth()
    st.session_state.db = st.session_state.firebase.database()

#if st.session_state.auth.current_user is None:
choice = choice_container.radio('Elige una de las siguientes opciones:', ['', 'Iniciar sesión', 'Registrarse', 'Olvidé mi contraseña'], key='choices')
sidebar_options()

if st.session_state.auth.current_user is not None:
    choice_container.empty()
    form_login_container.empty()
    main_cookia()
    form_logout = form_logout_container.form("form_logout_key", clear_on_submit=True)
    if form_logout.form_submit_button('Cerrar sesión'):
        st.session_state.auth.current_user = None
        form_main_container.empty()
        choice = choice_container.radio('Elige una de las siguientes opciones:', ['', 'Iniciar sesión', 'Registrarse', 'Olvidé mi contraseña'], key='choices2')
        #from streamlit import caching
        #caching.clear_cache()
        st.sidebar.success('Has cerrado sesión correctamente. Esperamos verte pronto, hasta la próxima!')
        form_logout_container.empty()