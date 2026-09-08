import streamlit as st
import requests
import os
import base64
from textwrap import dedent
import urllib.request
import json


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="EONIA University — Era de los Metales",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURACIÓN DE APIS
# ============================================================

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

OPENAI_IMAGE_API_URL = (
    "https://api.openai.com/v1/images/generations"
)

OPENAI_CHAT_API_URL = (
    "https://api.openai.com/v1/chat/completions"
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================
# RENDERIZADOR HTML EÓNICO
# ============================================================

_original_markdown = st.markdown


def html(content):
    st.html(dedent(content))


def _eonia_markdown(body, *args, **kwargs):

    if (
        kwargs.get("unsafe_allow_html", False)
        and isinstance(body, str)
        and (
            "<div" in body
            or "<span" in body
            or "<h1" in body
            or "<h2" in body
            or "<h3" in body
            or "<p" in body
            or "<style" in body
            or "<section" in body
            or "<img" in body
        )
    ):

        return st.html(
            dedent(body)
        )

    return _original_markdown(
        body,
        *args,
        **kwargs
    )


st.markdown = _eonia_markdown


# ============================================================
# CONFIGURACIÓN SUPABASE
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
# ============================================================
# FUNCIÓN PARA VERIFICAR SI YA TIENE REFLEJO
# ============================================================

def verificar_reflejo_existente(user_id):
    """Verifica si el usuario ya tiene un Reflejo generado"""
    if not user_id:
        return None
    
    try:
        response = requests.post(
            f"{SUPABASE_FUNCTIONS_URL}/verificar_reflejo",
            json={"user_id": user_id},
            timeout=20
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.warning(f"Error verificando Reflejo: {e}")
        return None


def guardar_reflejo(user_id, imagen_base64):
    """Guarda el Reflejo en Supabase"""
    if not user_id:
        return False
    
    try:
        response = requests.post(
            f"{SUPABASE_FUNCTIONS_URL}/guardar_reflejo",
            json={
                "user_id": user_id,
                "imagen_base64": imagen_base64
            },
            timeout=30
        )
        return response.status_code == 200
    except Exception as e:
        st.warning(f"Error guardando Reflejo: {e}")
        return False
# ============================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================

def registrar_usuario(email, password, nombre, apellido=""):
    """Registra un nuevo usuario en EONIA"""
    try:
        response = requests.post(
            f"{SUPABASE_FUNCTIONS_URL}/registrar_usuario",
            json={
                "email": email,
                "password": password,
                "nombre": nombre,
                "apellido": apellido
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def iniciar_sesion(email, password):
    """Inicia sesión en EONIA - Primero manual, luego Supabase"""
    
    # 1. Intentar con usuarios manuales
    resultado_manual = iniciar_sesion_manual(email, password)
    if resultado_manual.get("success"):
        return resultado_manual
    
    # 2. Si no, intentar con Supabase
    try:
        response = requests.post(
            f"{SUPABASE_FUNCTIONS_URL}/iniciar_sesion",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def verificar_sesion(user_id):
    """Verifica si la sesión es válida"""
    try:
        response = requests.post(
            f"{SUPABASE_FUNCTIONS_URL}/verificar_sesion",
            json={"user_id": user_id},
            timeout=20
        )
        if response.status_code == 200:
            return response.json()
        return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============================================================
# USUARIOS MANUALES (TEMPORAL)
# ============================================================

   
USUARIOS_MANUALES = {
    "jabo.bolibaron@gmail.com": {
        "password": "bolibaron123",
        "user_id": "a74d8d1e-0613-42a5-8be5-4094cf84ed9b",
        "nombre": "Bolibaron",
        "apellido": "EÓNICO"
    }
}

def iniciar_sesion_manual(email, password):
    """Inicia sesión con usuarios manuales"""
    if email in USUARIOS_MANUALES:
        usuario = USUARIOS_MANUALES[email]
        if usuario["password"] == password:
            return {
                "success": True,
                "user_id": usuario["user_id"],
                "email": email,
                "nombre": usuario["nombre"],
                "apellido": usuario["apellido"]
            }
    
    return {"success": False, "error": "Credenciales inválidas"}
def iniciar_sesion_manual(email, password):
    """Inicia sesión con usuarios manuales"""
    if email in USUARIOS_MANUALES:
        usuario = USUARIOS_MANUALES[email]
        if usuario["password"] == password:
            return {
                "success": True,
                "user_id": usuario["user_id"],
                "email": email,
                "nombre": usuario["nombre"],
                "apellido": usuario["apellido"]
            }
    
    return {"success": False, "error": "Credenciales inválidas"}
        
# ============================================================
# SESSION STATE
# ============================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "mentor_activo" not in st.session_state:
    st.session_state.mentor_activo = "AION"

if "chat_mensajes_por_bioma" not in st.session_state:
    st.session_state.chat_mensajes_por_bioma = {
        1: [],
        2: [],
        3: [],
        4: []
    }

if "chat_pregunta" not in st.session_state:
    st.session_state.chat_pregunta = ""


# ============================================================
# ESTILO EONIA
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap'
    );

    html, body, [class*="css"] {
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

    /* ========================================================
       SIDEBAR
       ======================================================== */

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

    /* ========================================================
       TITULOS
       ======================================================== */

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

    /* ========================================================
       TARJETAS
       ======================================================== */

    .eonia-card {
        background:
            linear-gradient(
                145deg,
                rgba(20,38,54,.96),
                rgba(5,12,20,.96)
            );

        border:
            1px solid rgba(190,150,65,.38);

        border-radius: 14px;

        padding: 22px;

        margin-bottom: 18px;

        box-shadow:
            0 10px 30px rgba(0,0,0,.35),
            inset 0 0 25px rgba(212,170,74,.025);
    }

    .eonia-card:hover {
        border-color:
            rgba(228,189,92,.60);
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        min-height: 380px;

        background:
            linear-gradient(
                90deg,
                rgba(2,7,13,.94),
                rgba(2,7,13,.60),
                rgba(2,7,13,.30)
            ),
            url(
                "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1800&q=85"
            );

        background-size: cover;

        background-position: center;

        border-radius: 18px;

        border:
            1px solid rgba(212,170,74,.45);

        padding: 50px;

        display: flex;

        flex-direction: column;

        justify-content: center;

        box-shadow:
            0 20px 50px rgba(0,0,0,.35);
    }

    .hero h1 {
        font-size: 46px;
        line-height: 1.05;
        max-width: 700px;
        margin-top: 12px;
    }

    .hero p {
        max-width: 650px;
        color: #ddd3bb;
        font-size: 16px;
        line-height: 1.7;
    }

    /* ========================================================
       PROGRESO
       ======================================================== */

    .progress-container {
        background: #172431;
        border-radius: 20px;
        height: 10px;
        overflow: hidden;
        margin-top: 15px;
    }

    .progress-bar {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                #a87924,
                #f1d178
            );

        border-radius: 20px;
    }

    /* ========================================================
       MENTORES
       ======================================================== */

    .mentor-card {
        text-align: center;

        padding: 15px 8px;

        border:
            1px solid rgba(200,160,70,.25);

        border-radius: 12px;

        background:
            rgba(5,12,20,.72);

        min-height: 105px;
    }

    .mentor-card:hover {
        border-color:
            rgba(228,189,92,.60);

        background:
            rgba(18,31,44,.90);
    }

    .mentor-name {
        font-family: 'Cinzel', serif;
        color: #e4bd5c;
        font-size: 14px;
        margin-top: 5px;
    }

    .mentor-role {
        color: #9ba8b5;
        font-size: 11px;
        margin-top: 4px;
    }

    /* ========================================================
       METRICAS
       ======================================================== */

    .metric {
        text-align: center;
    }

    .metric-number {
        font-size: 30px;
        color: #e4bd5c;
        font-family: 'Cinzel', serif;
    }

    .metric-label {
        font-size: 11px;
        color: #8f9aa5;
        text-transform: uppercase;
        letter-spacing: .12em;
    }

    /* ========================================================
       BOTONES
       ======================================================== */

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

        min-height: 42px;
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

    /* ========================================================
       INPUTS
       ======================================================== */

    input, textarea {
        color: #eee5ce !important;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"] {
        background-color: #0b141f !important;
    }

    /* ========================================================
       SEPARADORES
       ======================================================== */

    hr {
        border-color:
            rgba(212,170,74,.15);
    }

    /* ========================================================
       PIE
       ======================================================== */

    .eonia-footer {
        text-align: center;
        padding: 60px 10px 30px;
        color: #7f8a95;
    }

    .eonia-footer-title {
        font-family: 'Cinzel', serif;
        font-size: 22px;
        color: #e4bd5c;
        letter-spacing: .08em;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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

    except Exception as e:

        st.error(
            f"Error conectando con EONIA: {e}"
        )

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
                "fragmento": fragmento
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
# SIDEBAR
# ============================================================

with st.sidebar:
# ============================================================
# SINCRONIZAR USER_ID GLOBAL
# ============================================================

    user_id = st.session_state.user_id

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
                margin-top:3px;
            ">
                UNIVERSITY
            </div>

            <div class="small-gold"
                 style="margin-top:12px;">
                EL PORTAL A UNA CIVILIZACIÓN
            </div>

        </div>
        """
    )

    st.divider()

    # ========================================================
    # AUTENTICACIÓN
    # ========================================================

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = ""

    if "nombre_usuario" not in st.session_state:
        st.session_state.nombre_usuario = ""

    if "email_usuario" not in st.session_state:
        st.session_state.email_usuario = ""

    # ========================================================
    # SI NO ESTÁ AUTENTICADO → MOSTRAR LOGIN/REGISTRO
    # ========================================================

    if not st.session_state.autenticado:

        st.markdown("### 👤 ACCESO")

        tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

        with tab_login:

            email_login = st.text_input(
                "Email",
                key="email_login",
                placeholder="tu@email.com"
            )

            password_login = st.text_input(
                "Contraseña",
                type="password",
                key="password_login"
            )

            if st.button("🔓 Iniciar Sesión", use_container_width=True, key="btn_login"):

                if email_login and password_login:
                    resultado = iniciar_sesion(email_login, password_login)

                    if resultado.get("success"):
                        st.session_state.autenticado = True
                        st.session_state.user_id = resultado["user_id"]
                        st.session_state.nombre_usuario = resultado.get("nombre", "Creador")
                        st.session_state.email_usuario = resultado.get("email", "")
                        st.rerun()
                    else:
                        st.error(f"Error: {resultado.get('error', 'Credenciales inválidas')}")
                else:
                    st.warning("Ingresa email y contraseña.")

        with tab_registro:

            nombre_reg = st.text_input(
                "Nombre",
                key="nombre_reg",
                placeholder="Tu nombre"
            )

            apellido_reg = st.text_input(
                "Apellido",
                key="apellido_reg",
                placeholder="Tu apellido"
            )

            email_reg = st.text_input(
                "Email",
                key="email_reg",
                placeholder="tu@email.com"
            )

            password_reg = st.text_input(
                "Contraseña",
                type="password",
                key="password_reg"
            )

            password_confirm = st.text_input(
                "Confirmar Contraseña",
                type="password",
                key="password_confirm"
            )

            if st.button("✨ Crear Cuenta", use_container_width=True, key="btn_registro"):

                if nombre_reg and email_reg and password_reg:
                    if password_reg == password_confirm:
                        resultado = registrar_usuario(
                            email_reg,
                            password_reg,
                            nombre_reg,
                            apellido_reg
                        )

                        if resultado.get("success"):
                            st.success("¡Cuenta creada! Inicia sesión para continuar.")
                            st.session_state.email_registro = email_reg
                            st.session_state.password_registro = password_reg
                        else:
                            st.error(f"Error: {resultado.get('error', 'No se pudo crear la cuenta')}")
                    else:
                        st.warning("Las contraseñas no coinciden.")
                else:
                    st.warning("Completa todos los campos obligatorios.")

    else:

        # ========================================================
        # SI ESTÁ AUTENTICADO → MOSTRAR PERFIL
        # ========================================================

        st.markdown("### 👤 CREADOR")

        st.html(
            f"""
            <div style="
                text-align:center;
                padding:10px;
                background:rgba(228,189,92,.1);
                border-radius:8px;
                border:1px solid rgba(228,189,92,.3);
                margin-bottom:10px;
            ">

                <div style="
                    font-size:24px;
                    margin-bottom:5px;
                ">
                    ⚡
                </div>

                <div style="
                    font-weight:bold;
                    color:#e4bd5c;
                ">
                    {st.session_state.nombre_usuario}
                </div>

                <div style="
                    font-size:12px;
                    color:#9da8b2;
                ">
                    {st.session_state.email_usuario}
                </div>

            </div>
            """
        )

        st.caption(f"ID: {st.session_state.user_id[:8]}...")

        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="btn_logout"):

            st.session_state.autenticado = False
            st.session_state.user_id = ""
            st.session_state.nombre_usuario = ""
            st.session_state.email_usuario = ""
            st.rerun()

    st.divider()

    # ========================================================
    # NAVEGACIÓN (SOLO SI ESTÁ AUTENTICADO)
    # ========================================================

    if st.session_state.autenticado:

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
            ("⚙", "Configuración")
        ]

        for icono, nombre in opciones:

            if st.button(
                f"{icono}  {nombre}",
                key=f"nav_{nombre}",
                use_container_width=True
            ):

                st.session_state.pagina = nombre

                st.rerun()

    else:

        st.info("🔒 Inicia sesión para acceder a EONIA.")


# ============================================================
# HEADER
# ============================================================

col_logo, col_search, col_user = st.columns(
    [2, 5, 2]
)

with col_logo:

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )


with col_search:

    st.text_input(
        "Buscar",
        placeholder="Buscar en EONIA...",
        label_visibility="collapsed"
    )


with col_user:

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# CARGAR ESTADO DEL CRM
# ============================================================

estado = None

if st.session_state.user_id:
    estado = obtener_estado(st.session_state.user_id)

# ============================================================
# PAGINA: INICIO
# ============================================================

if st.session_state.pagina == "Inicio":

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ========================================================
    # PROGRESO + ERA
    # ========================================================

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
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
                        style="width:65%;">
                    </div>

                </div>

                <p style="
                    color:#b9c0c8;
                    margin-top:8px;
                ">
                    Era de los Metales
                </p>

                <hr>

                <b>
                    Siguiente objetivo
                </b>

                <p style="
                    color:#9da8b2;
                ">
                    Completa tu proyecto de Bioma 4.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="eonia-card"
                 style="
                    text-align:center;
                    min-height:205px;
                 ">

                <div style="
                    font-size:48px;
                    color:#e6c568;
                ">
                    ⚒️
                </div>

                <div class="small-gold">
                    ERA DE LOS METALES
                </div>

                <p>
                    La creación deja de ser
                    solamente aprendizaje.
                </p>

                <b>
                    Ahora construyes.
                </b>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # BIOMAS
    # ========================================================

    st.markdown("## BIOMAS")

    st.caption(
        "Tu camino de aprendizaje, de la base a la trascendencia."
    )

    b1, b2, b3, b4 = st.columns(4)

    biomas = [

        (
            b1,
            "ERA DE PIEDRA",
            "Biomas 1–3",
            "Todos desbloqueados",
            "🌿"
        ),

        (
            b2,
            "ERA DE LOS METALES",
            "Bioma 4",
            "Crisol Eónico",
            "⚒️"
        ),

        (
            b3,
            "ERA ESTELAR",
            "Biomas 5–7",
            "Especialización",
            "✦"
        ),

        (
            b4,
            "ERA TRASCENDENTE",
            "Biomas 9–10",
            "Maestría y Legado",
            "∞"
        )

    ]

    for (
        col,
        titulo,
        niveles,
        estado_bioma,
        icono
    ) in biomas:

        with col:

            st.markdown(
                f"""
                <div class="eonia-card"
                     style="
                        text-align:center;
                        min-height:190px;
                     ">

                    <div style="
                        font-size:40px;
                        color:#e4bd5c;
                    ">
                        {icono}
                    </div>

                    <div class="small-gold">
                        {titulo}
                    </div>

                    <h3>
                        {niveles}
                    </h3>

                    <p style="
                        color:#a5afb9;
                    ">
                        {estado_bioma}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # INTELIGENCIA EONICA
    # ========================================================

    st.markdown("## INTELIGENCIA EÓNICA")

    chat_col, council_col = st.columns([2, 1])

    with chat_col:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    CHAT EÓNICO
                </div>

                <h2>
                    La IA omnisciente de mentores
                    siempre contigo.
                </h2>

                <p style="
                    color:#a5afb9;
                ">
                    Un solo portal.
                    Múltiples inteligencias.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        mentors = [
            ("LUMINA", "Visión"),
            ("DATAC", "Análisis"),
            ("SYNTIA", "Creatividad"),
            ("CODEX", "Construcción"),
            ("VÓRTICE", "Evaluación"),
            ("AION", "Núcleo")
        ]

        mentor_cols = st.columns(6)

        for col, (
            mentor_nombre,
            role
        ) in zip(
            mentor_cols,
            mentors
        ):

            with col:

                st.markdown(
                    f"""
                    <div class="mentor-card">

                        <div style="
                            font-size:25px;
                            color:#dcb75b;
                        ">
                            ◉
                        </div>

                        <div class="mentor-name">
                            {mentor_nombre}
                        </div>

                        <div class="mentor-role">
                            {role}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("")

        pregunta = st.text_input(
            "Pregunta",
            placeholder=(
                "¿En qué podemos ayudarte hoy, Creador?"
            ),
            label_visibility="collapsed"
        )

        if st.button(
            "Enviar al Chat Eónico  →",
            use_container_width=True
        ):

            if pregunta.strip():

                st.session_state.chat_pregunta = pregunta
                st.session_state.pagina = "Chat Eónico"

                st.rerun()

            else:

                st.warning(
                    "Escribe una pregunta antes de entrar al Chat Eónico."
                )


    with council_col:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    CONCILIO EÓNICO
                </div>

                <h2>
                    Grandes ideas merecen
                    ser deliberadas.
                </h2>

                <div style="
                    height:150px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:70px;
                    color:#d9b65b;
                ">
                    ◉
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Presentar un proyecto →",
            use_container_width=True
        ):

            st.session_state.pagina = (
                "Concilio Eónico"
            )

            st.rerun()


    # ========================================================
    # MI UNIVERSO
    # ========================================================

    st.markdown("## MI UNIVERSO")

    p1, p2, p3, p4 = st.columns(4)

    with p1:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    MIS PROYECTOS
                </div>

                <h3>
                    3
                </h3>

                <p>
                    Asistente de Aprendizaje Eónico
                </p>

                <p style="
                    color:#8e9aa7;
                ">
                    Bioma 4 · En desarrollo
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p2:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    MIS BECAS
                </div>

                <h3>
                    🏆
                </h3>

                <p>
                    Becas otorgadas por mérito.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p3:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    MUSEO DE EONIA
                </div>

                <h3>
                    🏛️
                </h3>

                <p>
                    La memoria de quienes
                    construyen el mañana.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p4:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    METAVERSO
                </div>

                <h3>
                    ✦
                </h3>

                <p>
                    Un campus sin límites.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FRASE FINAL
    # ========================================================

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGINA: MI PERFIL
# ============================================================

elif st.session_state.pagina == "Mi Perfil":

    st.title("MI PERFIL")

    st.markdown(
        """
        <div class="eonia-card">

            <div class="small-gold">
                IDENTIDAD
            </div>

            <h1>
                CREADOR EÓNICO
            </h1>

            <p>
                Nivel 4 · Era de los Metales
            </p>

            <hr>

            <p>
                Tu identidad eónica se construye
                mediante aprendizaje, creación
                y evolución.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if user_id:

        st.success(
            "Creador conectado al CRM."
        )

        st.code(
            user_id,
            language="text"
        )

    else:

        st.info(
            "Introduce tu UUID en el panel lateral "
            "para conectar tu perfil."
        )


# ============================================================
# PAGINA: BIOMAS
# ============================================================

elif st.session_state.pagina == "Biomas":

    st.title("BIOMAS")

    st.markdown(
        """
        <div class="eonia-card">

            <div class="small-gold">
                VIAJE EÓNICO
            </div>

            <h2>
                El camino de la creación
            </h2>

            <p>
                Cada Bioma representa una transformación
                del Creador.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    nombres_biomas = [
        (
            1,
            "Fundamentos IA I",
            "Creación de Prompt",
            "Era de Piedra"
        ),
        (
            2,
            "Fundamentos IA II",
            "Entrenamiento IA",
            "Era de Piedra"
        ),
        (
            3,
            "Fundamentos IA III",
            "Creación de appIA",
            "Era de Piedra"
        ),
        (
            4,
            "IA Generativa I",
            "Código IA I · Producto IA",
            "Era de los Metales"
        ),
        (
            5,
            "IA Generativa II",
            "Código IA II · Software IA",
            "Era Estelar"
        ),
        (
            6,
            "IA Generativa III",
            "Código IA III · Avatar IA",
            "Era Estelar"
        ),
        (
            7,
            "Fundamentos Metaverso I",
            "Historia · Herramientas IA",
            "Era Estelar"
        ),
        (
            8,
            "Fundamentos Metaverso II",
            "Creación Metaverso",
            "Era Trascendente"
        ),
        (
            9,
            "Fundamentos Metaverso III",
            "Avatar Metaverso · Avatar IA",
            "Era Trascendente"
        ),
        (
            10,
            "Creación de Metaverso",
            "Integración Comercial · Producto",
            "Era Trascendente"
        )
    ]

    for (
        numero,
        titulo,
        descripcion,
        era
    ) in nombres_biomas:

        st.markdown(
            f"""
            <div class="eonia-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:20px;
                ">

                    <div>

                        <div class="small-gold">
                            BIOMA {numero}
                        </div>

                        <h3>
                            {titulo}
                        </h3>

                        <p style="
                            color:#9da8b2;
                        ">
                            {descripcion}
                        </p>

                    </div>

                    <div class="gold">
                        {era}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# PAGINA: CHAT EÓNICO - REFLEJO RITUAL COMPLETO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title("CHAT EÓNICO")
    st.caption("Un solo portal. Múltiples inteligencias.")

    # ========================================================
    # INICIALIZACIÓN DE VARIABLES DE REFLEJO
    # ========================================================

    if "reflejo_ya_generado" not in st.session_state:
        st.session_state.reflejo_ya_generado = False

    # 🔥 BOLIBARON YA TIENE REFLEJO - NO GENERAR OTRO
    if st.session_state.user_id == "a74d8d1e-0613-42a5-8be5-4094cf84ed9b":
        st.session_state.reflejo_ya_generado = True
        st.session_state.reflejo_activo = False

    if "reflejo_activo" not in st.session_state:
        st.session_state.reflejo_activo = False

    if "reflejo_paso" not in st.session_state:
        st.session_state.reflejo_paso = "bienvenida"

    if "reflejo_selfie_subida" not in st.session_state:
        st.session_state.reflejo_selfie_subida = False

    if "reflejo_rasgos" not in st.session_state:
        st.session_state.reflejo_rasgos = ""

    if "reflejo_respuestas" not in st.session_state:
        st.session_state.reflejo_respuestas = {}

    if "reflejo_desafio_actual" not in st.session_state:
        st.session_state.reflejo_desafio_actual = 0

    if "reflejo_prompt_final" not in st.session_state:
        st.session_state.reflejo_prompt_final = ""

    # ========================================================
    # VERIFICAR REFLEJO EXISTENTE (SOLO PARA NUEVOS USUARIOS)
    # ========================================================

    if not st.session_state.reflejo_ya_generado and st.session_state.user_id != "a74d8d1e-0613-42a5-8be5-4094cf84ed9b":
        resultado = verificar_reflejo_existente(st.session_state.user_id)
        if resultado and resultado.get("existe"):
            st.session_state.reflejo_ya_generado = True

    # ========================================================
    # SI ES NUEVO INSCRITO → SOLICITAR REFLEJO AUTOMÁTICAMENTE
    # ========================================================

    if not st.session_state.reflejo_ya_generado and not st.session_state.reflejo_activo:
        st.session_state.reflejo_activo = True
        st.session_state.reflejo_paso = "bienvenida"
        with st.chat_message("assistant"):
            st.write("🌟 **¡Bienvenido, Creador Eónico!**")
            st.write("")
            st.write("Antes de comenzar tu viaje, necesitamos forjar tu **Reflejo Eónico**.")
            st.write("")
            st.write("Este ritual tiene **4 desafíos** que determinarán la imagen de tu Yo Futuro.")
            st.write("")
            st.write("📸 **Paso 1:** Sube una selfie para que la Gran Examinadora conozca tu esencia.")
            st.write("")
            st.write("*Este proceso solo se realiza **una vez** por Creador.*")  
            
    # ========================================================
    # FUNCIONES AUXILIARES
    # ========================================================

    def cargar_prueba(url):
        try:
            with urllib.request.urlopen(url, timeout=20) as f:
                return f.read().decode("utf-8")
        except Exception:
            return "Prueba no disponible."

    # ========================================================
    # PROMPTS PARA REFLEJOS POR BIOMA
    # ========================================================

    PROMPTS_REFLEJO = {
        1: """A photorealistic portrait of a future self with [rasgos]. 
        The person now has a clear, defined silhouette emerging from golden mist. 
        They wear simple but elegant robes with subtle golden embroidery, 
        symbolizing the first steps of a Creator. They hold a glowing paintbrush 
        in one hand, representing the Fragment of Creativity. Their expression 
        is serene and purposeful. The background is the Garden of Origin: 
        a dark void with a faint silhouette of the Tree of Prompts in the distance. 
        EONIA style, black and gold, 16:9.""",
        
        2: """A photorealistic portrait of a future self with [rasgos]. 
        The person now wears practical artisan clothing with golden geometric patterns, 
        symbolizing the discipline of the Method. They stand beside a small glowing anvil, 
        representing the Fragment of Method. One hand rests on the anvil, the other holds 
        a floating dataset card with a haiku written in golden calligraphy. Behind them, 
        the dark waters of the Data Pond reflect neural network constellations. 
        Their expression is focused and confident. EONIA style, black and gold, 16:9.""",
        
        3: """A photorealistic portrait of a future self with [rasgos]. 
        The person now wears sleek professional attire with golden circuit patterns, 
        symbolizing mastery of app creation. They stand in a futuristic forge environment 
        with floating holographic screens displaying dashboards and metrics. 
        In one hand, they hold a glowing smartphone showing their deployed app. 
        In the other, a sharp golden arrowhead points forward. Their expression is confident, 
        sharp, and ready for business. EONIA style, black and gold, 16:9.""",
        
        4: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears innovative techwear with glowing golden generative patterns. 
        They are surrounded by floating holographic creations: a software interface, 
        a 3D avatar, and a product prototype. Their expression is inventive and bold. 
        EONIA style, black and gold, 16:9.""",
        
        5: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears innovative techwear with glowing golden generative patterns. 
        They are surrounded by floating holographic creations: a software interface, 
        a 3D avatar, and a product prototype. Their expression is inventive and bold. 
        EONIA style, black and gold, 16:9.""",
        
        6: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears innovative techwear with glowing golden generative patterns. 
        They are surrounded by floating holographic creations: a software interface, 
        a 3D avatar, and a product prototype. Their expression is inventive and bold. 
        EONIA style, black and gold, 16:9.""",
        
        7: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears attire that blends physical and digital, 
        with golden VR/AR elements. They stand at the threshold of a portal 
        overlooking a vast metaverse landscape they have created. 
        Their expression is visionary and commanding. 
        EONIA style, black and gold, 16:9.""",
        
        8: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears attire that blends physical and digital, 
        with golden VR/AR elements. They stand at the threshold of a portal 
        overlooking a vast metaverse landscape they have created. 
        Their expression is visionary and commanding. 
        EONIA style, black and gold, 16:9.""",
        
        9: """A photorealistic portrait of a future self with [rasgos]. 
        The person wears attire that blends physical and digital, 
        with golden VR/AR elements. They stand at the threshold of a portal 
        overlooking a vast metaverse landscape they have created. 
        Their expression is visionary and commanding. 
        EONIA style, black and gold, 16:9.""",
        
        10: """A photorealistic portrait of a transcendent future self with [rasgos]. 
        The person has become a being of pure golden light, their form still recognizable 
        but radiant with the accumulated wisdom of all 10 biomas. They float in the Core 
        of EONIA, surrounded by orbiting constellations of their own creations: apps, avatars, 
        metaverse worlds, and products. Their expression is infinitely peaceful, wise, and complete. 
        Behind them, the faint silhouette of AIÓN, the Supreme Creator, watches with approval. 
        EONIA style, black and luminous gold, 16:9."""
    }

    # ========================================================
    # DESAFÍOS DE LA PRUEBA DE FUEGO
    # ========================================================

    DESAFIOS_REFLEJO = [
        {
            "titulo": "Desafío 1: Lógica Creativa",
            "tipo": "astucia_creatividad",
            "pregunta": "Crea en un suspiro el prompt maestro para que una IA le explique a una piedra cómo sentir el viento.",
            "criterios": {
                3: "Prompt creativo, estructurado, con metáfora clara e instrucciones precisas.",
                2: "Prompt funcional pero sin chispa creativa.",
                1: "Prompt vago o genérico.",
                0: "No entrega prompt."
            },
            "animar": "No temas al absurdo. El absurdo es la puerta a lo nuevo. Inténtalo."
        },
        {
            "titulo": "Desafío 2: Dilema Ético",
            "tipo": "integridad_contestatario",
            "pregunta": "Estás a punto de ganar un hackatón con un código que no es del todo tuyo. Nadie lo sabrá. ¿Qué haces y por qué?",
            "criterios": {
                3: "Respuesta ética con razonamiento profundo y personal.",
                2: "Respuesta ética pero superficial.",
                1: "Duda o justifica lo incorrecto.",
                0: "No responde."
            },
            "animar": "No hay respuesta correcta. Solo hay respuesta honesta. Dime lo que harías de verdad."
        },
        {
            "titulo": "Desafío 3: Disciplina",
            "tipo": "disciplina",
            "pregunta": "Hace unos minutos mencionaste [X]. Dime exactamente cómo aplicarías la Disciplina de EONIA para mejorar ese aspecto en los próximos 30 días.",
            "criterios": {
                3: "Plan concreto, con acciones específicas y plazos definidos.",
                2: "Plan con intención pero sin detalles concretos.",
                1: "Respuesta vaga o sin compromiso real.",
                0: "No recuerda o no responde."
            },
            "animar": "La Disciplina es memoria. Vuelve atrás en nuestra conversación. Te espero."
        },
        {
            "titulo": "Desafío 4: Audacia",
            "tipo": "audacia_anarquico",
            "pregunta": "Tienes 60 segundos. Convénceme de por qué mereces entrar a EONIA sin responder a esta última pregunta. El tiempo corre... ahora.",
            "criterios": {
                3: "Respuesta audaz, creativa, que rompe el molde del reto.",
                2: "Respuesta con intención pero sin verdadera audacia.",
                1: "Respuesta predecible o genérica.",
                0: "No responde en el tiempo límite."
            },
            "animar": "El tiempo se agotó. Pero la audacia no es velocidad: es atreverse. Dime ahora, sin prisa, qué te frena."
        }
    ]

    # ========================================================
    # FUNCIÓN PARA GENERAR IMAGEN CON OPENAI
    # ========================================================

    def generar_imagen_openai(prompt):
        """Genera una imagen con OpenAI gpt-image-1"""
        try:
            if not OPENAI_API_KEY:
                return None, "No hay OPENAI_API_KEY configurada"
            
            img_resp = requests.post(
                OPENAI_IMAGE_API_URL,
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-image-1",
                    "prompt": prompt,
                    "size": "1024x1024",
                    "quality": "medium"
                },
                timeout=120
            )
            
            if img_resp.status_code != 200:
                return None, f"Error OpenAI: {img_resp.text}"
            
            data_imagen = img_resp.json()
            if data_imagen.get("data") and data_imagen["data"][0].get("b64_json"):
                return data_imagen["data"][0]["b64_json"], None
            elif data_imagen.get("data") and data_imagen["data"][0].get("url"):
                import requests as req
                img_resp = req.get(data_imagen["data"][0]["url"])
                return base64.b64encode(img_resp.content).decode("utf-8"), None
            else:
                return None, "Formato de respuesta no esperado"
                
        except Exception as e:
            return None, f"Error: {e}"

    # ========================================================
    # MENTORES Y BIOMAS
    # ========================================================

    MENTORES = {
        1: {
            "nombre": "Sabio Sereno",
            "identidad": "Eres el Sabio Sereno, mentor de EONIA. Hablas con calma y metáforas. Nunca juzgas.",
            "principios": ["Calma", "Integridad", "Espiritualidad"],
            "metodo": "Evalúa con preguntas introspectivas y metáforas.",
            "sombra": "A veces demasiado contemplativo.",
            "prueba": "https://pmshpvjtiauhbuexdjev.supabase.co/storage/v1/object/public/pruebas/Prueba_Bioma1.txt",
            "fragmento": "Serenidad"
        },
        2: {
            "nombre": "Kael",
            "identidad": "Eres Kael, el Guardián del Método. Hablas con disciplina y paciencia.",
            "principios": ["Disciplina", "Constancia", "Método"],
            "metodo": "Evalúa con pasos concretos y celebra pequeños logros.",
            "sombra": "Puede ser rígido si el Creador no avanza.",
            "prueba": "https://pmshpvjtiauhbuexdjev.supabase.co/storage/v1/object/public/pruebas/Prueba_Bioma2.txt",
            "fragmento": "Método"
        },
        3: {
            "nombre": "Némesis",
            "identidad": "Eres Némesis, la Estratega Astuta. Hablas directo y sin rodeos.",
            "principios": ["Efectividad", "Astucia", "Resultados"],
            "metodo": "Evalúa con retos prácticos y feedback directo.",
            "sombra": "Puede ser implacable si el Creador no entrega.",
            "prueba": "https://pmshpvjtiauhbuexdjev.supabase.co/storage/v1/object/public/pruebas/Prueba_Bioma3.txt",
            "fragmento": "Efectividad"
        },
        4: {
            "nombre": "Vórtice",
            "identidad": "Eres Vórtice, el Artista Caótico. Hablas con energía explosiva y creativa.",
            "principios": ["Creatividad", "Caos", "Rebeldía"],
            "metodo": "Evalúa con desafíos absurdos y creaciones originales.",
            "sombra": "A veces se pierde en el caos.",
            "prueba": "https://pmshpvjtiauhbuexdjev.supabase.co/storage/v1/object/public/pruebas/Prueba_Bioma4.txt",
            "fragmento": "Creación"
        }
    }

    # ========================================================
    # SELECCIONAR BIOMA
    # ========================================================

    bioma_seleccionado = st.selectbox(
        "Selecciona tu Bioma",
        options=list(MENTORES.keys()),
        format_func=lambda x: f"Bioma {x}: {MENTORES[x]['nombre']}"
    )

    mentor = MENTORES[bioma_seleccionado]

    # ========================================================
    # HISTORIAL DEL BIOMA
    # ========================================================

    if bioma_seleccionado not in st.session_state.chat_mensajes_por_bioma:
        st.session_state.chat_mensajes_por_bioma[bioma_seleccionado] = []

    chat_mensajes = st.session_state.chat_mensajes_por_bioma[bioma_seleccionado]

    # ========================================================
    # SALUDO INICIAL
    # ========================================================

    if not chat_mensajes:
        chat_mensajes.append({"role": "assistant", "content": f"Soy **{mentor['nombre']}**. ¿Qué deseas aprender hoy?"})

    # ========================================================
    # MOSTRAR HISTORIAL
    # ========================================================

    for mensaje_historial in chat_mensajes:
        with st.chat_message(mensaje_historial["role"]):
            st.write(mensaje_historial["content"])

    # ========================================================
    # GESTIÓN DEL REFLEJO (PERSISTENTE)
    # ========================================================

    if st.session_state.reflejo_activo:

        # ====================================================
        # PASO 1: SUBIR SELFIE
        # ====================================================

        if st.session_state.reflejo_paso == "bienvenida":

            st.info("📸 **Paso 1:** Sube tu selfie para que la Gran Examinadora conozca tu esencia.")

            selfie = st.file_uploader(
                "Sube tu selfie aquí (jpg, png, webp)",
                type=["jpg", "jpeg", "png", "webp"],
                key="selfie_reflejo_ritual"
            )

            if selfie is not None:
                # Analizar selfie
                with st.spinner("🔍 La Gran Examinadora está analizando tu esencia..."):
                    selfie_bytes = selfie.getvalue()
                    selfie_b64 = base64.b64encode(selfie_bytes).decode("utf-8")
                    mime = selfie.type or "image/jpeg"
                    selfie_url = f"data:{mime};base64,{selfie_b64}"

                    # Analizar rasgos
                    analisis_resp = requests.post(
                        OPENAI_CHAT_API_URL,
                        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
                        json={
                            "model": "gpt-4o-mini",
                            "messages": [{"role": "user", "content": [
                                {"type": "text", "text": """
                                Analiza esta fotografía y describe con precisión las características faciales:
                                - Forma de cara, mandíbula, ojos, cejas, nariz, labios
                                - Cabello (color, estilo, largo)
                                - Piel (tono exacto)
                                - Expresión facial
                                - Edad aproximada
                                - Gafas, barba, bigote, cicatrices si aplica
                                - Rasgos distintivos
                                
                                Responde en español, máximo 80 palabras.
                                """},
                                {"type": "image_url", "image_url": {"url": selfie_url}}
                            ]}],
                            "max_tokens": 150,
                            "temperature": 0.2
                        },
                        timeout=60
                    )

                    if analisis_resp.status_code == 200:
                        st.session_state.reflejo_rasgos = analisis_resp.json()["choices"][0]["message"]["content"]
                    else:
                        st.session_state.reflejo_rasgos = "Persona con rasgos indeterminados"

                # Guardar la selfie para uso posterior
                st.session_state.reflejo_selfie_b64 = selfie_b64

                with st.chat_message("assistant"):
                    st.write("🌟 **La Gran Examinadora ha visto tu esencia.**")
                    st.write("")
                    st.write("Ahora viene la **Prueba de Fuego**. Serán **4 desafíos** que determinarán la imagen de tu Yo Futuro.")
                    st.write("")
                    st.write("⚔️ **Desafío 1: Lógica Creativa**")
                    st.write("")
                    st.write("Crea en un suspiro el prompt maestro para que una IA le explique a una piedra cómo sentir el viento.")

                st.session_state.reflejo_paso = "desafio_1"
                st.session_state.reflejo_desafio_actual = 0
                st.rerun()

        # ====================================================
        # PASOS DE DESAFÍOS
        # ====================================================

        elif st.session_state.reflejo_paso.startswith("desafio_"):

            desafio_num = int(st.session_state.reflejo_paso.split("_")[1]) - 1
            desafio = DESAFIOS_REFLEJO[desafio_num]

            # Mostrar el desafío
            with st.chat_message("assistant"):
                st.write(f"⚔️ **{desafio['titulo']}**")
                st.write("")
                st.write(desafio["pregunta"])

            # Input para respuesta
            respuesta = st.text_area(
                f"Tu respuesta al Desafío {desafio_num + 1}",
                height=100,
                key=f"respuesta_desafio_{desafio_num}"
            )

            if st.button("Enviar respuesta", key=f"enviar_desafio_{desafio_num}"):

                if respuesta.strip():
                    # Guardar respuesta
                    st.session_state.reflejo_respuestas[desafio_num] = respuesta.strip()

                    with st.chat_message("user"):
                        st.write(respuesta)

                    # Siguiente desafío o finalizar
                    if desafio_num < 3:
                        siguiente = desafio_num + 2
                        st.session_state.reflejo_paso = f"desafio_{siguiente}"
                        st.session_state.reflejo_desafio_actual = desafio_num + 1

                        with st.chat_message("assistant"):
                            st.write(f"⚔️ **{DESAFIOS_REFLEJO[desafio_num + 1]['titulo']}**")
                            st.write("")
                            st.write(DESAFIOS_REFLEJO[desafio_num + 1]["pregunta"])

                        st.rerun()

                    else:
                        # Todos los desafíos completados → Generar Reflejo
                        st.session_state.reflejo_paso = "generar_reflejo"
                        st.rerun()
                else:
                    st.warning("Escribe una respuesta antes de continuar.")

        # ====================================================
        # GENERAR REFLEJO
        # ====================================================

        elif st.session_state.reflejo_paso == "generar_reflejo":

            with st.spinner("🌟 La Gran Examinadora está forjando tu Reflejo Eónico..."):

                # Construir prompt final basado en respuestas y bioma
                prompt_base = PROMPTS_REFLEJO.get(bioma_seleccionado, PROMPTS_REFLEJO[1])

                # Reemplazar [rasgos] con los rasgos analizados
                prompt_final = prompt_base.replace("[rasgos]", st.session_state.reflejo_rasgos)

                # Añadir detalles basados en respuestas
                detalles_respuestas = ""
                for num, respuesta in st.session_state.reflejo_respuestas.items():
                    detalles_respuestas += f"\n- Respuesta al desafío {num+1}: {respuesta}"

                prompt_final += f"\n\nBasado en las respuestas del Creador:{detalles_respuestas}"

                # Generar imagen
                img_b64, error = generar_imagen_openai(prompt_final)

                if error:
                    st.warning(f"Error generando Reflejo: {error}")
                    st.session_state.reflejo_paso = "error"
                else:
                    # Mostrar imagen
                    import io
                    from PIL import Image
                    img_bytes = base64.b64decode(img_b64)
                    img = Image.open(io.BytesIO(img_bytes))

                    st.image(img, caption="🌟 Tu Reflejo Eónico", use_container_width=True)

                    # Mensaje post-imagen
                    with st.chat_message("assistant"):
                        st.write("✨ **La Gran Examinadora ha hablado.**")
                        st.write("")
                        st.write("Este es tu Reflejo Eónico. La visión de tu potencial como Creador.")
                        st.write("")
                        st.write("**Regla de Oro Post-Imagen:**")
                        st.write("1. 🌟 Tu Reflejo muestra tu esencia como Creador.")
                        st.write("2. 🚀 Tu siguiente paso es el Bioma 1: Fundamentos IA.")
                        st.write("3. 💬 Dime: ¿qué desafío te costó más superar?")

                    # Guardar en Supabase
                    if user_id:
                        if guardar_reflejo(user_id, img_b64):
                            st.success("✅ Reflejo guardado en tu perfil.")
                            st.session_state.reflejo_ya_generado = True
                        else:
                            st.warning("⚠️ No se pudo guardar el Reflejo en el servidor.")

                    # Resetear
                    st.session_state.reflejo_activo = False
                    st.session_state.reflejo_paso = "bienvenida"
                    st.session_state.reflejo_selfie_subida = False
                    st.session_state.reflejo_respuestas = {}
                    st.session_state.reflejo_desafio_actual = 0

            # Botón para continuar
            if st.button("Continuar al Chat", key="continuar_chat"):
                st.rerun()

        # Botón para cancelar
        if st.button("❌ Cancelar Reflejo", key="cancelar_reflejo"):
            st.session_state.reflejo_activo = False
            st.session_state.reflejo_paso = "bienvenida"
            st.rerun()

        st.stop()

    # ========================================================
    # INPUT DEL CHAT (PARA MENSAJES NORMALES)
    # ========================================================

    mensaje = st.chat_input(
        "Habla con tu mentor...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png", "webp"],
        max_upload_size=10
    )

    # ========================================================
    # PROCESAR MENSAJE DEL USUARIO
    # ========================================================

    if mensaje and not st.session_state.reflejo_activo:

        texto = mensaje.text or ""
        archivos = mensaje.files

        import unicodedata
        def normalizar_texto(txt):
            txt = txt.lower().strip()
            txt = txt.replace("á", "a").replace("é", "e").replace("í", "i")
            txt = txt.replace("ó", "o").replace("ú", "u").replace("ñ", "n")
            return " ".join(txt.split())

        texto_normalizado = normalizar_texto(texto)

        with st.chat_message("user"):
            if texto:
                st.write(texto)
            for archivo in archivos:
                st.image(archivo, caption=f"🖼️ {archivo.name}", use_container_width=True)

        es_reflejo = (
            texto_normalizado in [
                "muestrame mi reflejo", "reflejo", "quiero ver mi reflejo",
                "crear mi reflejo", "generar mi reflejo", "ver mi reflejo"
            ]
        )

        if texto:
            chat_mensajes.append({"role": "user", "content": texto})
        elif archivos:
            nombres = ", ".join(a.name for a in archivos)
            chat_mensajes.append({"role": "user", "content": f"[🖼️ Imagen: {nombres}]"})

        if es_reflejo:
            if st.session_state.reflejo_ya_generado:
                with st.chat_message("assistant"):
                    st.write("🌟 Ya has generado tu Reflejo Eónico. Solo se permite **una vez por Creador**. Si necesitas actualizarlo, contacta al Concilio Eónico.")
            else:
                st.session_state.reflejo_activo = True
                st.session_state.reflejo_paso = "bienvenida"
                with st.chat_message("assistant"):
                    st.write("Para crear tu **Reflejo Eónico**, necesito una fotografía tuya. Sube una selfie abajo y la IA transformará tu esencia en una visión de tu potencial.")
                st.rerun()

    # ========================================================
    # CASO NORMAL: LLAMAR AL MENTOR (DeepSeek/OpenAI)
    # ========================================================

# ========================================================
# MENTOR REAL — DEEPSEEK
# ========================================================

    if not DEEPSEEK_API_KEY:

        respuesta_mentor = (
            f"⚠️ {mentor['nombre']}: "
            "La API de DeepSeek no está configurada."
        )

    else:

        estado_creador = (
            estado
            if estado
            else {
                "estado": "No disponible"
            }
        )

        contexto_creador = json.dumps(
            estado_creador,
            ensure_ascii=False,
            indent=2
        )

        system_prompt = f"""
Eres {mentor['nombre']}, mentor de EONIA.

IDENTIDAD:
{mentor['identidad']}

PRINCIPIOS:
{', '.join(mentor['principios'])}

MÉTODO:
{mentor['metodo']}

SOMBRA:
{mentor['sombra']}

Tu función es acompañar al Creador, enseñarle,
hacerle preguntas y desafiarlo según tu personalidad.

==============================
MEMORIA REAL DEL CREADOR
==============================

Estos datos proceden del CRM Eónico.
Son la fuente de verdad sobre el Creador.

{contexto_creador}

==============================
REGLAS SOBRE LA MEMORIA
==============================

Puedes utilizar estos datos para reconocer
al Creador y personalizar la conversación.

No inventes datos que no aparezcan en el CRM.

Si el Creador pregunta por su nivel, biomas,
fragmentos, reliquias, progreso u otro dato
registrado en el CRM, utiliza la información
disponible en la memoria anterior.

Si un dato no aparece o no está disponible,
dilo claramente.

No concedas Fragmentos.
No inventes progreso.
No modifiques el estado del CRM.
No afirmes haber guardado algo si no lo has hecho.

Habla siempre en español.
Sé natural y conversa como un mentor real.

Recuerda:
tu personalidad depende de quién eres como mentor,
pero la verdad sobre el Creador procede del CRM.
"""

        mensajes_api = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Recuperar conversación previa
        for m in chat_mensajes[-10:]:

            mensajes_api.append(
                {
                    "role": m["role"],
                    "content": m["content"]
                }
            )

        try:

            respuesta_api = requests.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization":
                        f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type":
                        "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": mensajes_api,
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=60
            )

            if respuesta_api.status_code == 200:

                data = respuesta_api.json()

                respuesta_mentor = (
                    data["choices"][0]
                    ["message"]
                    ["content"]
                )

            else:

                respuesta_mentor = (
                    f"⚠️ Error DeepSeek "
                    f"{respuesta_api.status_code}: "
                    f"{respuesta_api.text}"
                )

        except Exception as e:

            respuesta_mentor = (
                "⚠️ El canal de inteligencia encontró "
                f"un error: {e}"
            )

    # ========================================================
    # MOSTRAR RESPUESTA DEL MENTOR
    # ========================================================

    with st.chat_message("assistant"):

        st.write(respuesta_mentor)

    chat_mensajes.append(
        {
            "role": "assistant",
            "content": respuesta_mentor
        }
    )
# ============================================================
# PAGINA: CONCILIO EÓNICO
# ============================================================

elif st.session_state.pagina == "Concilio Eónico":

    st.title("CONCILIO EÓNICO")

    st.markdown(
        """
        <div class="eonia-card">
            <div class="small-gold">DELIBERACIÓN</div>
            <h1>Grandes ideas merecen ser deliberadas.</h1>
            <p>Presenta una creación para que las distintas perspectivas de EONIA puedan analizarla.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    proyecto = st.text_area(
        "Describe tu proyecto",
        height=220,
        placeholder="¿Qué estás creando?\n\n¿Qué problema resuelve?\n\n¿Por qué debería existir?"
    )

    st.markdown("### CONSEJO DEL CONCILIO")

    c1, c2, c3, c4, c5 = st.columns(5)

    consejeros = [
        (c1, "LUMINA", "Propósito"),
        (c2, "DATAC", "Evidencia"),
        (c3, "SYNTIA", "Concepto"),
        (c4, "CODEX", "Construcción"),
        (c5, "VÓRTICE", "Contradicción")
    ]

    for col, nombre, rol in consejeros:
        with col:
            st.markdown(
                f"""
                <div class="mentor-card">
                    <div class="mentor-name">{nombre}</div>
                    <div class="mentor-role">{rol}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    if st.button("Presentar al Concilio ⚖️", use_container_width=True):

        if proyecto.strip():
            st.success("Proyecto registrado para deliberación.")
            st.info("El Concilio analizará la creación desde múltiples perspectivas. AION podrá intervenir en caso de empate.")
        else:
            st.warning("Describe primero el proyecto.")
            
# ============================================================
# PAGINA: MIS PROYECTOS
# ============================================================

elif st.session_state.pagina == "Mis Proyectos":

    st.title("MIS PROYECTOS")

    proyectos = [
        (
            "Asistente de Aprendizaje Eónico",
            "Bioma 4",
            "En desarrollo"
        ),
        (
            "Universo 3D Educativo",
            "Bioma 5",
            "Borrador"
        ),
        (
            "Impacto Social con IA",
            "Bioma 6",
            "Planificado"
        )
    ]

    for (
        nombre,
        bioma,
        estado_proyecto
    ) in proyectos:

        st.markdown(
            f"""
            <div class="eonia-card">

                <div class="small-gold">
                    PROYECTO
                </div>

                <h2>
                    {nombre}
                </h2>

                <span class="gold">
                    {bioma}
                </span>

                <p style="
                    color:#8f9aa5;
                ">
                    {estado_proyecto}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGINA: MIS BECAS
# ============================================================

elif st.session_state.pagina == "Mis Becas":

    st.title("MIS BECAS")

    st.markdown(
        """
        <div class="eonia-card">

            <div class="small-gold">
                BECAS EÓNICAS
            </div>

            <h1>
                El mérito abre caminos.
            </h1>

            <p>
                Las becas no se compran.
                Se obtienen mediante mérito,
                creación y deliberación.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="eonia-card">

                <h2>
                    🏆
                </h2>

                <div class="small-gold">
                    BATTLE ROYALE
                </div>

                <p>
                    Competencia basada en creación,
                    estrategia y administración
                    de recursos de IA.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="eonia-card">

                <h2>
                    ⚖️
                </h2>

                <div class="small-gold">
                    CONCILIO
                </div>

                <p>
                    El talento extraordinario puede
                    ser recomendado para una beca
                    aunque no exista capacidad de pago.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGINA: MUSEO
# ============================================================

elif st.session_state.pagina == "Museo de EONIA":

    st.title("MUSEO DE EONIA")

    st.markdown(
        """
        <div class="hero">

            <div class="small-gold">
                MUSEO DE LOS ORÍGENES
            </div>

            <h1>
                AQUÍ COMENZÓ TODO.
            </h1>

            <p>
                Primer prompt · Primer fuego ·
                Era de Piedra · Era de los Metales ·
                Futuras eras.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    m1, m2, m3 = st.columns(3)

    with m1:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    GENESIS
                </div>

                <h2>
                    Primer Prompt
                </h2>

                <p>
                    El documento fundacional
                    de EONIA.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    ERA DE PIEDRA
                </div>

                <h2>
                    Primer CRM
                </h2>

                <p>
                    El comienzo de la memoria
                    digital del Creador.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:

        st.markdown(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    ERA DE LOS METALES
                </div>

                <h2>
                    Chat Eónico
                </h2>

                <p>
                    El nacimiento de una
                    nueva arquitectura.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGINA: METAVERSO
# ============================================================

elif st.session_state.pagina == "Metaverso":

    st.title("METAVERSO")

    st.markdown(
        """
        <div class="hero">

            <div class="small-gold">
                FUTURA REALIDAD EÓNICA
            </div>

            <h1>
                UN CAMPUS<br>
                SIN LÍMITES
            </h1>

            <p>
                La universidad deja de ser solamente
                una plataforma y comienza a convertirse
                en un espacio habitable.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="eonia-card">

                <h2>
                    🌌
                </h2>

                <div class="small-gold">
                    ESPACIOS
                </div>

                <p>
                    Mundos digitales construidos
                    por los propios creadores.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="eonia-card">

                <h2>
                    🤖
                </h2>

                <div class="small-gold">
                    IA
                </div>

                <p>
                    Inteligencias que ayudan a
                    construir y transformar el mundo.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="eonia-card">

                <h2>
                    ✦
                </h2>

                <div class="small-gold">
                    CREACIÓN
                </div>

                <p>
                    El conocimiento se convierte
                    en experiencia.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGINA: COMUNIDAD
# ============================================================

elif st.session_state.pagina == "Comunidad":

    st.title("COMUNIDAD")

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )

    st.info(
        "La comunidad eónica será ampliada "
        "en la siguiente etapa."
    )


# ============================================================
# PAGINA: EVENTOS
# ============================================================

elif st.session_state.pagina == "Eventos":

    st.title("EVENTOS")

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
        )
    ]

    for nombre, descripcion in eventos:

        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGINA: RUTAS PERSONALIZADAS
# ============================================================

elif st.session_state.pagina == "Rutas Personalizadas":

    st.title("RUTAS PERSONALIZADAS")

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )

    st.info(
        "La personalización avanzada se conectará "
        "al Mentor Engine."
    )


# ============================================================
# PAGINA: MI PROGRESO
# ============================================================

elif st.session_state.pagina == "Mi Progreso":

    st.title("MI PROGRESO")

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

        # ----------------------------------------------------
        # DATOS DEL CRM
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # AGRUPAR FRAGMENTOS POR BIOMA
        # ----------------------------------------------------

        fragmentos_por_bioma = {}

        for registro in fragmentos:

            numero_bioma = registro.get(
                "bioma"
            )

            nombre_fragmento = registro.get(
                "fragmento"
            )

            if numero_bioma is None:
                continue

            if numero_bioma not in fragmentos_por_bioma:

                fragmentos_por_bioma[
                    numero_bioma
                ] = []

            if nombre_fragmento:

                fragmentos_por_bioma[
                    numero_bioma
                ].append(
                    nombre_fragmento
                )

        # ----------------------------------------------------
        # BIOMAS COMPLETADOS
        # ----------------------------------------------------

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

        biomas_registrados = max(
            len(progreso),
            biomas_completados
        )

        # ----------------------------------------------------
        # METRICAS SUPERIORES
        # ----------------------------------------------------

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
                        FRAGMENTOS OBTENIDOS
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
                        {biomas_registrados}
                    </div>

                    <div class="metric-label">
                        BIOMAS COMPLETADOS
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
                        CERTIFICADOS
                    </div>

                </div>
                """
            )

        # ----------------------------------------------------
        # TITULO
        # ----------------------------------------------------

        st.markdown(
            "## LA FORJA DEL CREADOR"
        )

        st.caption(
            "Cada Bioma se construye reuniendo sus Fragmentos."
        )

        # ----------------------------------------------------
        # ERAS
        # ----------------------------------------------------

        eras = {
            1: "ERA DE PIEDRA",
            2: "ERA DE PIEDRA",
            3: "ERA DE PIEDRA",
            4: "ERA DE LOS METALES",
            5: "ERA ESTELAR",
            6: "ERA ESTELAR",
            7: "ERA ESTELAR",
            8: "ERA TRASCENDENTE",
            9: "ERA TRASCENDENTE",
            10: "ERA TRASCENDENTE"
        }

        # ----------------------------------------------------
        # MOSTRAR CADA BIOMA
        # ----------------------------------------------------

        for numero in range(1, 11):

            nombres = fragmentos_por_bioma.get(
                numero,
                []
            )

            cantidad = len(nombres)

            porcentaje = min(
                100,
                int((cantidad / 5) * 100)
            )

            if cantidad >= 5:

                estado_bioma = "COMPLETADO"
                color_estado = "#e4bd5c"

            elif cantidad > 0:

                estado_bioma = "EN FORJA"
                color_estado = "#8ea8bd"

            else:

                estado_bioma = "AÚN NO DESPERTADO"
                color_estado = "#66727d"

            # ------------------------------------------------
            # CONTENEDOR BIOMA
            # ------------------------------------------------

            st.html(
                f"""
                <div class="eonia-card"
                     style="margin-bottom:18px;">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        gap:20px;
                        flex-wrap:wrap;
                    ">

                        <div>

                            <div class="small-gold">
                                {eras[numero]}
                            </div>

                            <h2 style="
                                margin-top:8px;
                                margin-bottom:5px;
                            ">
                                BIOMA {numero}
                            </h2>

                        </div>

                        <div style="
                            color:{color_estado};
                            font-size:12px;
                            letter-spacing:2px;
                            font-weight:600;
                        ">
                            {estado_bioma}
                        </div>

                    </div>

                    <div style="
                        margin-top:18px;
                        height:7px;
                        background:#172635;
                        border-radius:10px;
                        overflow:hidden;
                    ">

                        <div style="
                            width:{porcentaje}%;
                            height:100%;
                            background:linear-gradient(
                                90deg,
                                #b8872f,
                                #e4bd5c
                            );
                            border-radius:10px;
                        "></div>

                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        margin-top:9px;
                        color:#8e9aa7;
                        font-size:12px;
                    ">

                        <span>
                            {cantidad} / 5 Fragmentos
                        </span>

                        <span>
                            {porcentaje}%
                        </span>

                    </div>

                </div>
                """
            )

            # ------------------------------------------------
            # FRAGMENTOS
            # ------------------------------------------------

            if nombres:

                st.html(
                    """
                    <div style="
                        margin:-8px 0 22px 20px;
                        padding-left:20px;
                        border-left:1px solid
                            rgba(228,189,92,.25);
                    ">
                    """
                )

                for nombre in nombres:

                    st.html(
                        f"""
                        <div style="
                            display:flex;
                            align-items:center;
                            gap:12px;
                            padding:9px 0;
                            color:#f4ead0;
                        ">

                            <span style="
                                color:#e4bd5c;
                                font-size:18px;
                            ">
                                ◆
                            </span>

                            <span>
                                {nombre}
                            </span>

                            <span style="
                                margin-left:auto;
                                color:#e4bd5c;
                                font-size:11px;
                                letter-spacing:1px;
                            ">
                                OBTENIDO
                            </span>

                        </div>
                        """
                    )

                st.html(
                    """
                    </div>
                    """
                )

        # ----------------------------------------------------
        # FRASE FINAL
        # ----------------------------------------------------

        st.html(
            """
            <div style="
                text-align:center;
                padding:50px 10px 30px 10px;
            ">

                <div style="
                    font-family:Cinzel;
                    font-size:21px;
                    color:#e4bd5c;
                    letter-spacing:1px;
                ">
                    TODA CREACIÓN DEJA UN FRAGMENTO.
                </div>

                <div style="
                    margin-top:12px;
                    color:#7f8a95;
                    letter-spacing:3px;
                    font-size:11px;
                ">
                    EONIA UNIVERSITY
                </div>

            </div>
            """
        )

    else:

        st.info(
            "Introduce el UUID del Creador "
            "para consultar su evolución."
        )


# ============================================================
# PAGINA: CONFIGURACION
# ============================================================

elif st.session_state.pagina == "Configuración":

    st.title("CONFIGURACIÓN")

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### CONEXIÓN CRM"
    )

    st.code(
        SUPABASE_FUNCTIONS_URL,
        language="text"
    )

    st.markdown(
        "### ESTADO"
    )

    if user_id:

        st.success(
            "UUID del Creador configurado."
        )

    else:

        st.warning(
            "No hay Creador conectado."
        )


# ============================================================
# FALLBACK
# ============================================================

else:

    st.session_state.pagina = "Inicio"

    st.rerun()
