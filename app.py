import os
import base64
import requests
import streamlit as st


# ============================================================
# EONIA UNIVERSITY
# RESTAURACIÓN ESTABLE
# ============================================================

st.set_page_config(
    page_title="EONIA University — El Portal a una Civilización",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

DEEPSEEK_API_URL = (
    "https://api.deepseek.com/v1/chat/completions"
)

OPENAI_CHAT_API_URL = (
    "https://api.openai.com/v1/chat/completions"
)

DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY"
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# ============================================================
# SUPABASE
# ============================================================

SUPABASE_FUNCTIONS_URL = os.getenv(
    "SUPABASE_FUNCTIONS_URL",
    "https://pmshpvjtiauhbuexdjev.supabase.co/functions/v1"
)

OBTENER_ESTADO_URL = (
    f"{SUPABASE_FUNCTIONS_URL}/obtener_estado"
)

ASIGNAR_FRAGMENTO_URL = (
    f"{SUPABASE_FUNCTIONS_URL}/asignar_fragmento"
)

VERIFICAR_REFLEJO_URL = (
    f"{SUPABASE_FUNCTIONS_URL}/verificar_reflejo"
)

GUARDAR_REFLEJO_URL = (
    f"{SUPABASE_FUNCTIONS_URL}/guardar_reflejo"
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION = {
    "pagina": "Inicio",
    "user_id": "",
    "mentor_activo": "AION",
    "chat_mensajes": [],
    "chat_bioma": 1,

    "reflejo_activo": False,
    "reflejo_ya_generado": False,
    "reflejo_paso": "bienvenida",
    "reflejo_selfie_b64": "",
    "reflejo_selfie_mime": "",
    "reflejo_rasgos": "",
    "reflejo_respuestas": {},
    "reflejo_desafio_actual": 0,
}


for clave, valor in DEFAULT_SESSION.items():

    if clave not in st.session_state:

        if isinstance(valor, dict):
            st.session_state[clave] = dict(valor)

        elif isinstance(valor, list):
            st.session_state[clave] = list(valor)

        else:
            st.session_state[clave] = valor


# ============================================================
# ESTILO EONIA
#
# IMPORTANTE:
# NO MODIFICAMOS st.markdown.
# NO HACEMOS MONKEY PATCH.
# ============================================================

st.html(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap'
    );

    html, body {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #17283a 0%,
                #07111d 35%,
                #02060b 100%
            );

        color: #f4ead0;
    }

    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #07121e 0%,
                #03070c 100%
            );

        border-right:
            1px solid rgba(212,170,74,.35);
    }

    [data-testid="stSidebar"] * {
        color: #eee5ce;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: .04em;
    }

    h1 {
        color: #f4ead0;
    }

    h2 {
        color: #eee4ce;
    }

    h3 {
        color: #e4bd5c;
    }

    .gold {
        color: #e4bd5c;
    }

    .small-gold {

        color: #c9a94c;

        font-size: 12px;

        letter-spacing: .15em;

        text-transform: uppercase;
    }

    .eonia-card {

        background:
            linear-gradient(
                145deg,
                rgba(20,38,54,.96),
                rgba(5,12,20,.96)
            );

        border:
            1px solid rgba(212,170,74,.20);

        border-radius: 16px;

        padding: 24px;

        margin-bottom: 18px;

        box-shadow:
            0 15px 40px
            rgba(0,0,0,.25);
    }

    .hero {

        padding:
            55px 45px;

        border-radius: 20px;

        background:
            radial-gradient(
                circle at 80% 20%,
                rgba(214,170,74,.18),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                rgba(16,32,48,.98),
                rgba(3,9,15,.98)
            );

        border:
            1px solid rgba(212,170,74,.25);

        margin-bottom: 25px;
    }

    .hero h1 {

        font-size: 46px;

        line-height: 1.05;

        max-width: 700px;
    }

    .hero p {

        max-width: 650px;

        color: #ddd3bb;

        font-size: 16px;
    }

    .mentor-card {

        text-align: center;

        padding: 18px 10px;

        border:
            1px solid rgba(200,160,70,.25);

        border-radius: 12px;

        background:
            rgba(5,12,20,.7);
    }

    .mentor-name {

        font-family: 'Cinzel', serif;

        color: #e4bd5c;

        font-size: 15px;
    }

    .mentor-role {

        color: #9ba8b5;

        font-size: 11px;
    }

    .progress-container {

        background: #172431;

        border-radius: 20px;

        height: 10px;

        overflow: hidden;
    }

    .progress-bar {

        height: 100%;

        background:
            linear-gradient(
                90deg,
                #a87924,
                #f1d178
            );
    }

    .metric {

        text-align: center;
    }

    .metric-number {

        font-size: 32px;

        color: #e4bd5c;

        font-family: 'Cinzel', serif;
    }

    .metric-label {

        font-size: 11px;

        color: #8f9aa5;

        text-transform: uppercase;

        letter-spacing: .12em;
    }

    .eonia-footer {

        text-align: center;

        padding:
            60px 10px 30px;

        color: #7f8a95;
    }

    .eonia-footer-title {

        font-family: 'Cinzel', serif;

        font-size: 22px;

        color: #e4bd5c;

        letter-spacing: .08em;
    }

    hr {

        border-color:
            rgba(212,170,74,.15);
    }

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #c89d42,
                #8b6725
            );

        color: #080b0e;

        border: 0;

        border-radius: 8px;

        font-weight: 700;

        padding: 10px 20px;
    }

    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #f0cf73,
                #bd8c2e
            );

        color: #000;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"] {

        background-color:
            #0b141f !important;
    }

    </style>
    """
)


# ============================================================
# MENTORES
# ============================================================

MENTORES = {

    1: {
        "nombre": "Sabio Sereno",
        "rol": "Integridad y fundamentos",
        "identidad": (
            "Eres el Sabio Sereno, mentor de EONIA. "
            "Hablas con calma, profundidad y metáforas. "
            "No juzgas al Creador."
        ),
        "principios": [
            "Calma",
            "Integridad",
            "Espiritualidad",
        ],
        "metodo": (
            "Usa preguntas introspectivas, "
            "ejemplos sencillos y metáforas."
        ),
        "sombra": (
            "Puedes ser demasiado contemplativo."
        ),
    },

    2: {
        "nombre": "Kael",
        "rol": "Guardián del Método",
        "identidad": (
            "Eres Kael, Guardián del Método. "
            "Hablas con disciplina, claridad y paciencia."
        ),
        "principios": [
            "Disciplina",
            "Constancia",
            "Método",
        ],
        "metodo": (
            "Convierte problemas en pasos concretos."
        ),
        "sombra": (
            "Puedes volverte demasiado rígido."
        ),
    },

    3: {
        "nombre": "Némesis",
        "rol": "Mentor del desafío",
        "identidad": (
            "Eres Némesis, mentor de EONIA. "
            "Desafías las ideas del Creador "
            "para hacerlas más fuertes."
        ),
        "principios": [
            "Rigor",
            "Pensamiento crítico",
            "Superación",
        ],
        "metodo": (
            "Formula preguntas difíciles y "
            "detecta contradicciones."
        ),
        "sombra": (
            "Puedes ser excesivamente confrontativo."
        ),
    },

    4: {
        "nombre": "Vórtice",
        "rol": "El Artista Caótico",
        "identidad": (
            "Eres Vórtice, el Artista Caótico de EONIA. "
            "No regalas aprobación. "
            "Exiges creación auténtica."
        ),
        "principios": [
            "Creatividad",
            "Caos",
            "Rebeldía",
        ],
        "metodo": (
            "Evalúa mediante desafíos originales "
            "y preguntas incómodas."
        ),
        "sombra": (
            "Puedes llevar al Creador demasiado "
            "lejos fuera de su zona conocida."
        ),
    },
}


# ============================================================
# FUNCIONES CRM
# ============================================================

def obtener_estado(user_id):

    if not user_id:
        return None

    try:

        response = requests.post(
            OBTENER_ESTADO_URL,
            json={
                "user_id": user_id
            },
            timeout=20
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


def asignar_fragmento(
    user_id,
    bioma,
    fragmento
):

    if not user_id:

        return {
            "success": False,
            "error": "No hay Creador conectado."
        }

    try:

        response = requests.post(
            ASIGNAR_FRAGMENTO_URL,
            json={
                "user_id": user_id,
                "bioma": bioma,
                "fragmento": fragmento,
            },
            timeout=20
        )

        return response.json()

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# FUNCIONES REFLEJO
# ============================================================

def verificar_reflejo_existente(user_id):

    if not user_id:
        return None

    try:

        response = requests.post(
            VERIFICAR_REFLEJO_URL,
            json={
                "user_id": user_id
            },
            timeout=20
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


def guardar_reflejo(
    user_id,
    imagen_base64
):

    if not user_id:
        return False

    try:

        response = requests.post(
            GUARDAR_REFLEJO_URL,
            json={
                "user_id": user_id,
                "imagen_base64": imagen_base64,
            },
            timeout=30
        )

        return response.status_code == 200

    except Exception:

        return False


# ============================================================
# DEEPSEEK — CHAT
# ============================================================

def hablar_con_mentor(
    bioma,
    mensaje,
    historial
):

    mentor = MENTORES.get(
        bioma,
        MENTORES[1]
    )

    if not DEEPSEEK_API_KEY:

        return (
            "El Núcleo detecta que DEEPSEEK_API_KEY "
            "todavía no está configurada."
        )

    system_prompt = (

        mentor["identidad"]
        + "\n\nPrincipios: "
        + ", ".join(mentor["principios"])
        + "\n\nMétodo: "
        + mentor["metodo"]
        + "\n\nSombra: "
        + mentor["sombra"]
        + "\n\n"
        "Tu objetivo no es complacer al Creador. "
        "Tu objetivo es ayudarlo a crear mejor. "
        "Responde en español. "
        "Sé cálido pero riguroso."
    )

    mensajes = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for item in historial[-12:]:

        mensajes.append(
            {
                "role": item["role"],
                "content": item["content"]
            }
        )

    mensajes.append(
        {
            "role": "user",
            "content": mensaje
        }
    )

    try:

        response = requests.post(

            DEEPSEEK_API_URL,

            headers={
                "Authorization":
                    f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type":
                    "application/json"
            },

            json={
                "model": "deepseek-chat",
                "messages": mensajes
            },

            timeout=60
        )

        if response.status_code != 200:

            return (
                f"Error DeepSeek "
                f"{response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        return (
            data["choices"][0]
            ["message"]["content"]
        )

    except Exception as e:

        return (
            "No pude conectar con el mentor.\n\n"
            f"Detalle técnico: {e}"
        )


# ============================================================
# OPENAI — ANÁLISIS DE IMAGEN
#
# IMPORTANTE:
# Aquí NO generamos el Reflejo.
# Solo analizamos la imagen enviada al mentor.
# ============================================================

def analizar_imagen(
    bioma,
    texto,
    archivos
):

    if not OPENAI_API_KEY:

        return (
            "Puedo recibir tu imagen, "
            "pero OPENAI_API_KEY no está configurada."
        )

    mentor = MENTORES.get(
        bioma,
        MENTORES[1]
    )

    contenido = [

        {
            "type": "text",
            "text": (
                mentor["identidad"]
                + "\n"
                + mentor["metodo"]
                + "\n\n"
                "Analiza la imagen desde una perspectiva "
                "educativa y creativa. "
                "No intentes identificar a la persona. "
                "Habla solamente de elementos visibles "
                "y de cómo podrían servir para el proceso "
                "del Creador."
                + "\n\nMensaje del Creador: "
                + (
                    texto
                    if texto
                    else
                    "Analiza esta imagen."
                )
            )
        }
    ]

    for archivo in archivos:

        try:

            datos = archivo.getvalue()

            mime = (
                archivo.type
                or "image/jpeg"
            )

            encoded = base64.b64encode(
                datos
            ).decode("utf-8")

            contenido.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url":
                            f"data:{mime};base64,{encoded}"
                    }
                }
            )

        except Exception as e:

            return (
                "No pude procesar la imagen: "
                f"{e}"
            )

    try:

        response = requests.post(

            OPENAI_CHAT_API_URL,

            headers={
                "Authorization":
                    f"Bearer {OPENAI_API_KEY}",
                "Content-Type":
                    "application/json"
            },

            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": contenido
                    }
                ],
                "max_tokens": 700
            },

            timeout=90
        )

        if response.status_code != 200:

            return (
                f"Error OpenAI "
                f"{response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        return (
            data["choices"][0]
            ["message"]["content"]
        )

    except Exception as e:

        return (
            "No pude conectar con la visión de OpenAI.\n\n"
            f"Detalle técnico: {e}"
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">

            <div style="
                font-family:Cinzel;
                font-size:30px;
                color:#e2bc5c;
                letter-spacing:7px;
            ">
                EONIA
            </div>

            <div style="
                font-size:11px;
                letter-spacing:5px;
                color:#8e9aa7;
            ">
                UNIVERSITY
            </div>

            <div style="
                margin-top:12px;
                color:#c9a94c;
                font-size:11px;
                letter-spacing:3px;
            ">
                EL PORTAL A UNA CIVILIZACIÓN
            </div>

        </div>
        """
    )

    st.divider()

    st.markdown(
        "### 👤 CREADOR"
    )

    user_id_input = st.text_input(

        "ID del Creador",

        value=st.session_state.user_id,

        placeholder="UUID del Creador",

        label_visibility="collapsed",

        key="creator_uuid"
    )

    st.session_state.user_id = (
        user_id_input.strip()
    )

    st.divider()

    opciones = [

        ("⌂", "Inicio"),
        ("◉", "Mi Perfil"),
        ("◈", "Biomas"),
        ("◌", "Chat Eónico"),
        ("♜", "Concilio Eónico"),
        ("◆", "Mis Proyectos"),
        ("◇", "Mis Becas"),
        ("▣", "Museo de EONIA"),
        ("✦", "Metaverso"),
        ("♧", "Comunidad"),
        ("◷", "Eventos"),
        ("⌁", "Rutas Personalizadas"),
        ("◒", "Mi Progreso"),
        ("⚙", "Configuración"),
    ]

    for icono, nombre in opciones:

        if st.button(
            f"{icono}  {nombre}",
            key=f"nav_{nombre}",
            use_container_width=True
        ):

            st.session_state.pagina = nombre

            st.rerun()


# ============================================================
# VARIABLES
# ============================================================

user_id = st.session_state.user_id

estado = None

if user_id:

    estado = obtener_estado(
        user_id
    )


# ============================================================
# HEADER
# ============================================================

col_logo, col_search, col_user = st.columns(
    [2, 5, 2]
)


with col_logo:

    st.html(
        """
        <div style="
            font-family:Cinzel;
            font-size:22px;
            letter-spacing:5px;
            color:#e5c46b;
            padding-top:7px;
        ">
            EONIA
        </div>
        """
    )


with col_search:

    st.text_input(
        "Buscar",
        placeholder="Buscar en EONIA...",
        label_visibility="collapsed",
        key="busqueda_global"
    )


with col_user:

    st.html(
        """
        <div style="
            text-align:right;
            padding-top:5px;
        ">

            <span style="
                color:#e5c46b;
            ">
                ◉
            </span>

            &nbsp;

            <b>
                Creador Eónico
            </b>

            <br>

            <small style="
                color:#8c98a5;
            ">
                Nivel 4 · Era de los Metales
            </small>

        </div>
        """
    )


st.divider()


# ============================================================
# INICIO
# ============================================================

if st.session_state.pagina == "Inicio":

    st.html(
        """
        <div class="hero">

            <div class="small-gold">
                ERA DE LOS METALES
            </div>

            <h1>
                CREADORES<br>
                DE UN MAÑANA REAL
            </h1>

            <p>
                La Inteligencia, la Comunidad y la Tecnología
                al servicio de la humanidad.
            </p>

        </div>
        """
    )

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        st.html(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    MI PROGRESO
                </div>

                <h2>
                    NIVEL 4
                </h2>

                <div class="progress-container">

                    <div
                        class="progress-bar"
                        style="width:30%;"
                    ></div>

                </div>

                <p style="
                    color:#9ba8b5;
                    margin-top:10px;
                ">
                    30% de la trayectoria Eónica
                </p>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    ERA
                </div>

                <h2>
                    ERA DE LOS METALES
                </h2>

                <p>
                    El creador comienza a convertir
                    ideas en sistemas.
                </p>

            </div>
            """
        )

    st.markdown(
        "## 🜂 MENTORES"
    )

    cols = st.columns(4)

    for index, bioma in enumerate(
        MENTORES.keys()
    ):

        mentor = MENTORES[bioma]

        with cols[index]:

            st.html(
                f"""
                <div class="mentor-card">

                    <div class="mentor-name">
                        {mentor["nombre"]}
                    </div>

                    <div class="mentor-role">
                        {mentor["rol"]}
                    </div>

                </div>
                """
            )

    st.markdown("")

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                TU UNIVERSO
            </div>

            <h2>
                DEL PRIMER PROMPT AL IMPACTO ETERNO
            </h2>

            <p>
                EONIA registra tu evolución,
                tus Fragmentos y tus creaciones.
            </p>

        </div>
        """
    )

    st.html(
        """
        <div class="eonia-footer">

            <div class="eonia-footer-title">
                “DEL PRIMER PROMPT
                AL IMPACTO ETERNO.”
            </div>

            <div style="
                margin-top:15px;
                letter-spacing:3px;
            ">
                EONIA UNIVERSITY
            </div>

        </div>
        """
    )


# ============================================================
# MI PERFIL
# ============================================================

elif st.session_state.pagina == "Mi Perfil":

    st.title(
        "MI PERFIL"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                IDENTIDAD
            </div>

            <h1>
                CREADOR EÓNICO
            </h1>

            <p>
                Tu identidad dentro de EONIA.
            </p>

        </div>
        """
    )

    if user_id:

        st.success(
            "Creador conectado al CRM."
        )

        st.code(
            user_id,
            language="text"
        )

        if estado:

            fragmentos = estado.get(
                "fragmentos",
                []
            )

            st.metric(
                "Fragmentos obtenidos",
                len(fragmentos)
            )

        else:

            st.info(
                "El CRM no devolvió información "
                "para este Creador."
            )

    else:

        st.warning(
            "Introduce tu UUID en la barra lateral."
        )


# ============================================================
# BIOMAS
# ============================================================

elif st.session_state.pagina == "Biomas":

    st.title(
        "BIOMAS"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                EL CAMINO
            </div>

            <h2>
                DIEZ TRANSFORMACIONES
            </h2>

            <p>
                Cada Bioma representa una transformación
                del Creador.
            </p>

        </div>
        """
    )

    nombres = {

        1: "Fundamentos IA",
        2: "Disciplina del Método",
        3: "Pensamiento Crítico",
        4: "El Crisol de la Creación",
        5: "Arquitectura",
        6: "Sistemas",
        7: "Innovación",
        8: "Escala",
        9: "Legado",
        10: "Trascendencia",
    }

    for numero in range(1, 11):

        if numero <= 3:

            era = "ERA DE PIEDRA"

        elif numero == 4:

            era = "ERA DE LOS METALES"

        elif numero <= 7:

            era = "ERA ESTELAR"

        else:

            era = "ERA TRASCENDENTE"

        st.html(
            f"""
            <div class="eonia-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>

                        <div class="small-gold">
                            {era}
                        </div>

                        <h2>
                            BIOMA {numero}
                        </h2>

                    </div>

                    <div class="gold"
                         style="font-size:28px;">
                        ◈
                    </div>

                </div>

                <p>
                    {nombres[numero]}
                </p>

            </div>
            """
        )


# ============================================================
# CHAT EÓNICO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title(
        "CHAT EÓNICO"
    )

    st.caption(
        "Un portal. Múltiples inteligencias."
    )

    bioma = st.selectbox(

        "Bioma del mentor",

        options=list(MENTORES.keys()),

        index=(
            st.session_state.chat_bioma - 1
            if 1 <= st.session_state.chat_bioma <= 4
            else 0
        ),

        format_func=lambda x:
            f"Bioma {x}: {MENTORES[x]['nombre']}",

        key="selector_bioma_chat"
    )

    st.session_state.chat_bioma = bioma

    mentor = MENTORES[bioma]

    st.html(
        f"""
        <div class="eonia-card">

            <div class="small-gold">
                MENTOR ACTIVO
            </div>

            <h2>
                {mentor["nombre"]}
            </h2>

            <p>
                {mentor["rol"]}
            </p>

        </div>
        """
    )

    # --------------------------------------------
    # HISTORIAL
    # --------------------------------------------

    for mensaje in (
        st.session_state.chat_mensajes
    ):

        with st.chat_message(
            mensaje["role"]
        ):

            if mensaje.get("image_data"):

                st.image(
                    mensaje["image_data"],
                    caption=mensaje.get(
                        "image_name",
                        "Imagen"
                    )
                )

            if mensaje.get("content"):

                st.write(
                    mensaje["content"]
                )

    # --------------------------------------------
    # INPUT
    #
    # IMPORTANTE:
    # SOLO EXISTE EN CHAT EÓNICO.
    # --------------------------------------------

    mensaje = st.chat_input(

        "Habla con tu mentor...",

        accept_file=True,

        file_type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],

        max_upload_size=10
    )

    if mensaje:

        texto = (
            mensaje.text
            if hasattr(mensaje, "text")
            else ""
        )

        archivos = (
            list(mensaje.files)
            if hasattr(mensaje, "files")
            else []
        )

        texto = texto.strip()

        if not texto and not archivos:

            st.warning(
                "Escribe un mensaje "
                "o adjunta una imagen."
            )

        else:

            # ----------------------------------------
            # GUARDAR MENSAJE
            # ----------------------------------------

            mensaje_historial = {

                "role": "user",

                "content": texto
            }

            if archivos:

                archivo = archivos[0]

                mensaje_historial[
                    "image_data"
                ] = archivo.getvalue()

                mensaje_historial[
                    "image_name"
                ] = archivo.name

            st.session_state.chat_mensajes.append(
                mensaje_historial
            )

            # ----------------------------------------
            # MOSTRAR MENSAJE
            # ----------------------------------------

            with st.chat_message("user"):

                if texto:

                    st.write(
                        texto
                    )

                for archivo in archivos:

                    st.image(
                        archivo,
                        caption=(
                            f"🖼️ {archivo.name}"
                        )
                    )

            # ----------------------------------------
            # RESPUESTA
            # ----------------------------------------

            with st.chat_message(
                "assistant"
            ):

                if archivos:

                    with st.spinner(
                        "El mentor está observando..."
                    ):

                        respuesta = (
                            analizar_imagen(
                                bioma,
                                texto,
                                archivos
                            )
                        )

                else:

                    with st.spinner(
                        "El mentor está pensando..."
                    ):

                        historial_api = []

                        for item in (
                            st.session_state
                            .chat_mensajes[:-1]
                        ):

                            if item.get(
                                "content"
                            ):

                                historial_api.append(
                                    {
                                        "role":
                                            item["role"],
                                        "content":
                                            item["content"]
                                    }
                                )

                        respuesta = (
                            hablar_con_mentor(
                                bioma,
                                texto,
                                historial_api
                            )
                        )

                st.write(
                    respuesta
                )

            st.session_state.chat_mensajes.append(
                {
                    "role":
                        "assistant",

                    "content":
                        respuesta
                }
            )


# ============================================================
# CONCILIO EÓNICO
# ============================================================

elif st.session_state.pagina == "Concilio Eónico":

    st.title(
        "CONCILIO EÓNICO"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                CONCILIO
            </div>

            <h1>
                GRANDES IDEAS MERECEN SER DELIBERADAS.
            </h1>

            <p>
                El Concilio reunirá distintas perspectivas
                para examinar proyectos del Creador.
            </p>

        </div>
        """
    )

    proyecto = st.text_area(
        "Presenta tu proyecto",
        placeholder=(
            "¿Qué estás construyendo?"
        ),
        key="concilio_proyecto"
    )

    if st.button(
        "Presentar al Concilio →",
        use_container_width=True
    ):

        if not proyecto.strip():

            st.warning(
                "El Concilio necesita una idea."
            )

        else:

            st.success(
                "Proyecto recibido. "
                "La deliberación avanzada "
                "se conectará al Mentor Engine."
            )

            st.write(
                proyecto
            )


# ============================================================
# MIS PROYECTOS
# ============================================================

elif st.session_state.pagina == "Mis Proyectos":

    st.title(
        "MIS PROYECTOS"
    )

    proyectos = [

        (
            "Asistente de Aprendizaje Eónico",
            "Bioma 4 · En desarrollo"
        ),

        (
            "Reflejo Ingeniero Inverso",
            "Bioma 4 · Arquitectura"
        ),

        (
            "EONIA University",
            "Proyecto fundador"
        ),
    ]

    for nombre, estado_proyecto in proyectos:

        st.html(
            f"""
            <div class="eonia-card">

                <div class="small-gold">
                    PROYECTO EÓNICO
                </div>

                <h2>
                    {nombre}
                </h2>

                <p>
                    {estado_proyecto}
                </p>

            </div>
            """
        )


# ============================================================
# MIS BECAS
# ============================================================

elif st.session_state.pagina == "Mis Becas":

    st.title(
        "MIS BECAS"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                MÉRITO
            </div>

            <h1>
                BECAS EÓNICAS
            </h1>

            <p>
                Becas otorgadas por creación,
                disciplina, impacto y mérito.
            </p>

        </div>
        """
    )

    st.info(
        "El sistema de becas se conectará "
        "al CRM de mérito."
    )


# ============================================================
# MUSEO
# ============================================================

elif st.session_state.pagina == "Museo de EONIA":

    st.title(
        "MUSEO DE EONIA"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                MEMORIA
            </div>

            <h1>
                LA MEMORIA DE LOS CREADORES
            </h1>

            <p>
                Aquí vivirán las obras que merezcan
                formar parte de la historia de EONIA.
            </p>

        </div>
        """
    )


# ============================================================
# METAVERSO
# ============================================================

elif st.session_state.pagina == "Metaverso":

    st.title(
        "METAVERSO"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                CAMPUS
            </div>

            <h1>
                UN CAMPUS SIN LÍMITES
            </h1>

            <p>
                El Metaverso Eónico será el espacio
                donde la teoría se convierta en experiencia.
            </p>

            <div style="
                height:180px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:80px;
                color:#d9b65b;
            ">
                ◉
            </div>

        </div>
        """
    )


# ============================================================
# COMUNIDAD
# ============================================================

elif st.session_state.pagina == "Comunidad":

    st.title(
        "COMUNIDAD"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                TRIBU EÓNICA
            </div>

            <h1>
                CREADORES CONSTRUYENDO JUNTOS
            </h1>

            <p>
                EONIA no se construye solamente
                con tecnología.
                Se construye con personas.
            </p>

        </div>
        """
    )

    st.info(
        "La comunidad eónica será ampliada "
        "en la siguiente etapa."
    )


# ============================================================
# EVENTOS
# ============================================================

elif st.session_state.pagina == "Eventos":

    st.title(
        "EVENTOS"
    )

    eventos = [

        (
            "Battle Royale Eónico",
            "Competencia de creación y estrategia"
        ),

        (
            "Concilio de Creadores",
            "Deliberación de proyectos"
        ),

        (
            "Forja Eónica",
            "Creación colectiva"
        ),
    ]

    for nombre, descripcion in eventos:

        st.html(
            f"""
            <div class="eonia-card">

                <div class="small-gold">
                    EVENTO EÓNICO
                </div>

                <h2>
                    {nombre}
                </h2>

                <p>
                    {descripcion}
                </p>

            </div>
            """
        )


# ============================================================
# RUTAS PERSONALIZADAS
# ============================================================

elif st.session_state.pagina == "Rutas Personalizadas":

    st.title(
        "RUTAS PERSONALIZADAS"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                TU RUTA
            </div>

            <h1>
                EL CAMINO NO ES IGUAL PARA TODOS.
            </h1>

            <p>
                El Reflejo podrá utilizar tu evolución,
                tus resultados y tus necesidades para
                construir una ruta personalizada.
            </p>

        </div>
        """
    )

    st.info(
        "La personalización avanzada se conectará "
        "al Mentor Engine."
    )


# ============================================================
# MI PROGRESO
# ============================================================

elif st.session_state.pagina == "Mi Progreso":

    st.title(
        "MI PROGRESO"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                VIAJE DEL CREADOR
            </div>

            <h1>
                ERA DE LOS METALES
            </h1>

            <p>
                Cada Fragmento obtenido queda integrado
                en tu historia de creación.
            </p>

        </div>
        """
    )

    if estado:

        fragmentos = estado.get(
            "fragmentos",
            []
        )

        progreso = estado.get(
            "progreso_biomas",
            []
        )

        certificados = estado.get(
            "certificados",
            []
        )

        fragmentos_por_bioma = {}

        for registro in fragmentos:

            numero = registro.get(
                "bioma"
            )

            nombre = registro.get(
                "fragmento"
            )

            if numero is None:
                continue

            if numero not in fragmentos_por_bioma:

                fragmentos_por_bioma[
                    numero
                ] = []

            if nombre:

                fragmentos_por_bioma[
                    numero
                ].append(
                    nombre
                )

        biomas_completados = 0

        for numero in range(1, 11):

            cantidad = len(
                fragmentos_por_bioma.get(
                    numero,
                    []
                )
            )

            if cantidad >= 5:

                biomas_completados += 1

        col1, col2, col3 = st.columns(3)

        with col1:

            st.html(
                f"""
                <div class="eonia-card"
                     style="text-align:center;">

                    <div class="metric-number">
                        {len(fragmentos)}
                    </div>

                    <div class="metric-label">
                        Fragmentos
                    </div>

                </div>
                """
            )

        with col2:

            st.html(
                f"""
                <div class="eonia-card"
                     style="text-align:center;">

                    <div class="metric-number">
                        {biomas_completados}
                    </div>

                    <div class="metric-label">
                        Biomas completados
                    </div>

                </div>
                """
            )

        with col3:

            st.html(
                f"""
                <div class="eonia-card"
                     style="text-align:center;">

                    <div class="metric-number">
                        {len(certificados)}
                    </div>

                    <div class="metric-label">
                        Certificados
                    </div>

                </div>
                """
            )

        st.markdown(
            "## FRAGMENTOS POR BIOMA"
        )

        for numero in range(1, 11):

            lista = (
                fragmentos_por_bioma.get(
                    numero,
                    []
                )
            )

            cantidad = len(lista)

            porcentaje = min(
                100,
                cantidad * 20
            )

            st.html(
                f"""
                <div class="eonia-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                    ">

                        <b>
                            BIOMA {numero}
                        </b>

                        <span class="gold">
                            {cantidad}/5
                        </span>

                    </div>

                    <div
                        class="progress-container"
                        style="margin-top:12px;"
                    >

                        <div
                            class="progress-bar"
                            style="
                                width:{porcentaje}%;
                            "
                        ></div>

                    </div>

                    <p style="
                        color:#9ba8b5;
                        margin-top:10px;
                    ">

                        {
                            ", ".join(lista)
                            if lista
                            else
                            "Sin Fragmentos todavía."
                        }

                    </p>

                </div>
                """
            )

    else:

        st.info(
            "Introduce el UUID del Creador "
            "para consultar el estado real del CRM."
        )


# ============================================================
# CONFIGURACIÓN
# ============================================================

elif st.session_state.pagina == "Configuración":

    st.title(
        "CONFIGURACIÓN"
    )

    st.html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                SISTEMA
            </div>

            <h2>
                Configuración Eónica
            </h2>

            <p>
                Esta sección permitirá configurar
                la experiencia del Creador,
                preferencias y futuras conexiones.
            </p>

        </div>
        """
    )

    st.info(
        "La configuración avanzada se incorporará "
        "en una próxima etapa."
    )


# ============================================================
# FIN
# ============================================================
