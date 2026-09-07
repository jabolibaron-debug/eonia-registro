import streamlit as st
import requests
import os
from textwrap import dedent

# ============================================================
# CONFIGURACIÓN DE APIS
# ============================================================
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
OPENAI_IMAGE_API_URL = "https://api.openai.com/v1/images/generations"
OPENAI_CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ============================================================
# RENDERIZADOR HTML EÓNICO
# ============================================================

_original_markdown = st.markdown


def html(content):
    st.html(dedent(content))


def _eonia_markdown(body, *args, **kwargs):

    # Si el contenido permite HTML y realmente contiene HTML,
    # lo enviamos al motor HTML de Streamlit.
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

    # Todo Markdown normal continúa funcionando
    # exactamente como antes.
    return _original_markdown(
        body,
        *args,
        **kwargs
    )


st.markdown = _eonia_markdown

# ============================================================
# EONIA UNIVERSITY — CRM
# ERA DE LOS METALES
# ============================================================

st.set_page_config(
    page_title="EONIA University — Era de los Metales",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
# SESSION STATE
# ============================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "mentor_activo" not in st.session_state:
    st.session_state.mentor_activo = "AION"


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

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 👤 CREADOR")

    user_id = st.text_input(
        "ID del Creador",
        value=st.session_state.user_id,
        placeholder="UUID del Creador",
        label_visibility="collapsed"
    )

    st.session_state.user_id = user_id

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

if user_id:

    estado = obtener_estado(user_id)


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

    col1, col2 = st.columns(
        [2, 1]
    )

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

    chat_col, council_col = st.columns(
        [2, 1]
    )

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
            mentor,
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
                            {mentor}
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

            if pregunta:

                st.session_state.pagina = "Chat Eónico"

                st.session_state.chat_pregunta = pregunta

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
# PAGINA: CHAT EONICO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title("CHAT EÓNICO")
    st.caption("Un solo portal. Múltiples inteligencias.")

    import urllib.request

    def cargar_prueba(url):
        try:
            with urllib.request.urlopen(url) as f:
                return f.read().decode("utf-8")
        except:
            return "Prueba no disponible"

    # MENTORES Y BIOMAS
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

    bioma_seleccionado = st.selectbox(
        "Selecciona tu Bioma",
        options=list(MENTORES.keys()),
        format_func=lambda x: f"Bioma {x}: {MENTORES[x]['nombre']}"
    )

    mentor = MENTORES[bioma_seleccionado]

    # Historial
    if "chat_mensajes" not in st.session_state:
        st.session_state.chat_mensajes = []

    # Saludo inicial
    if not st.session_state.chat_mensajes:
        st.session_state.chat_mensajes.append({
            "role": "assistant",
            "content": f"Soy **{mentor['nombre']}**. ¿Qué deseas aprender hoy?"
        })

    # Mostrar historial
    for mensaje in st.session_state.chat_mensajes:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])

        # Entrada con soporte de imágenes
    mensaje = st.chat_input(
        "Habla con tu mentor...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png", "webp"],
        max_upload_size=10
    )

    if mensaje:
        texto = mensaje.text
        archivos = mensaje.files

        # Agregar texto al historial
        if texto:
            st.session_state.chat_mensajes.append({
                "role": "user",
                "content": texto
            })

        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            if texto:
                st.write(texto)

            for archivo in archivos:
                st.image(
                    archivo,
                    caption=f"🖼️ {archivo.name}",
                    use_container_width=True
                )

        # Si hay archivos, registrarlos
        if archivos:
            for archivo in archivos:
                st.session_state.chat_mensajes.append({
                    "role": "user",
                    "content": f"[Imagen enviada: {archivo.name}]"
                })
        # ============================================
        # LÓGICA DEL REFLEJO
        # ============================================
        if "reflejo" in mensaje.lower():
            with st.spinner("Generando tu Reflejo..."):
                try:
                    img_resp = requests.post(
                        OPENAI_IMAGE_API_URL,
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "dall-e-3",
                            "prompt": (
                                "Un reflejo dorado de un Creador Eónico, "
                                "estilo EONIA, negro y dorado."
                            ),
                            "size": "1024x1024"
                        },
                        timeout=60
                    )
                    if img_resp.status_code == 200:
                        img_url = img_resp.json()["data"][0]["url"]
                        st.image(img_url, caption="Tu Reflejo Eónico")
                except:
                    st.warning("No se pudo generar el Reflejo.")

        # ============================================
        # CARGA DE PRUEBA
        # ============================================
        contenido_prueba = cargar_prueba(mentor["prueba"])

        # ============================================
        # DETECCIÓN DE IMÁGENES
        # ============================================
        hay_imagen = "imagen" in mensaje.lower() or bool(archivos)

        if hay_imagen:
            try:
                contenido_mensajes = [
                    {
                        "role": "system",
                        "content": (
                            mentor["identidad"] + "\n"
                            "Principios: " + ", ".join(mentor["principios"]) + "\n"
                            "Método: " + mentor["metodo"] + "\n"
                            "Sombra: " + mentor["sombra"] + "\n"
                            "Prueba: " + contenido_prueba + "\n"
                            "Fragmento a otorgar: " + mentor["fragmento"]
                        )
                    },
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_mensajes
                    ]
                ]

                if archivos:
                    contenido_mensajes.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": mensaje.text or "Analiza esta imagen"},
                            *[
                                {
                                    "type": "image_url",
                                    "image_url": {"url": "data:image/jpeg;base64," + __import__("base64").b64encode(archivo.read()).decode()}
                                }
                                for archivo in archivos
                            ]
                        ]
                    })

                respuesta = requests.post(
                    OPENAI_CHAT_API_URL,
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": contenido_mensajes
                    },
                    timeout=90
                )

                if respuesta.status_code == 200:
                    data = respuesta.json()
                    respuesta_texto = data["choices"][0]["message"]["content"]
                else:
                    respuesta_texto = f"Error OpenAI {respuesta.status_code}: {respuesta.text}"

            except Exception as e:
                respuesta_texto = f"Error de conexión con OpenAI: {e}"

        else:
            try:
                respuesta = requests.post(
                    DEEPSEEK_API_URL,
                    headers={
                        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    mentor["identidad"] + "\n"
                                    "Principios: " + ", ".join(mentor["principios"]) + "\n"
                                    "Método: " + mentor["metodo"] + "\n"
                                    "Sombra: " + mentor["sombra"] + "\n"
                                    "Prueba: " + contenido_prueba + "\n"
                                    "Fragmento a otorgar: " + mentor["fragmento"]
                                )
                            },
                            *[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.chat_mensajes
                            ]
                        ]
                    },
                    timeout=60
                )

                if respuesta.status_code == 200:
                    data = respuesta.json()
                    respuesta_texto = data["choices"][0]["message"]["content"]
                else:
                    respuesta_texto = f"Error DeepSeek {respuesta.status_code}: {respuesta.text}"

            except Exception as e:
                respuesta_texto = f"Error de conexión con DeepSeek: {e}"

        st.session_state.chat_mensajes.append({
            "role": "assistant",
            "content": respuesta_texto
        })

        with st.chat_message("assistant"):
            st.write(respuesta_texto)

        if "imagen" in mensaje.lower() and OPENAI_API_KEY:
            with st.spinner("Generando imagen..."):
                try:
                    img_resp = requests.post(
                        OPENAI_IMAGE_API_URL,
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "dall-e-3",
                            "prompt": mensaje,
                            "size": "1024x1024"
                        },
                        timeout=60
                    )
                    if img_resp.status_code == 200:
                        img_url = img_resp.json()["data"][0]["url"]
                        st.image(img_url, caption="Reflejo de EONIA")
                except:
                    pass
# ============================================================
# PAGINA: CONCILIO EONICO
# ============================================================

elif st.session_state.pagina == "Concilio Eónico":

    st.title("CONCILIO EÓNICO")

    st.markdown(
        """
        <div class="eonia-card">

            <div class="small-gold">
                DELIBERACIÓN
            </div>

            <h1>
                Grandes ideas merecen ser deliberadas.
            </h1>

            <p>
                Presenta una creación para que las
                distintas perspectivas de EONIA
                puedan analizarla.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    proyecto = st.text_area(
        "Describe tu proyecto",
        height=220,
        placeholder=(
            "¿Qué estás creando?\n\n"
            "¿Qué problema resuelve?\n\n"
            "¿Por qué debería existir?"
        )
    )

    st.markdown("### CONSEJO DEL CONCILIO")

    c1, c2, c3, c4, c5 = st.columns(5)

    consejeros = [
        (
            c1,
            "LUMINA",
            "Propósito"
        ),
        (
            c2,
            "DATAC",
            "Evidencia"
        ),
        (
            c3,
            "SYNTIA",
            "Concepto"
        ),
        (
            c4,
            "CODEX",
            "Construcción"
        ),
        (
            c5,
            "VÓRTICE",
            "Contradicción"
        )
    ]

    for col, nombre, rol in consejeros:

        with col:

            st.markdown(
                f"""
                <div class="mentor-card">

                    <div class="mentor-name">
                        {nombre}
                    </div>

                    <div class="mentor-role">
                        {rol}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    if st.button(
        "Presentar al Concilio ⚖️",
        use_container_width=True
    ):

        if proyecto.strip():

            st.success(
                "Proyecto registrado para deliberación."
            )

            st.info(
                "El Concilio analizará la creación "
                "desde múltiples perspectivas. "
                "AION podrá intervenir en caso de empate."
            )

        else:

            st.warning(
                "Describe primero el proyecto."
            )


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

    # --------------------------------------------------------
    # CABECERA
    # --------------------------------------------------------

    st.html("""
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
    """)

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

            numero_bioma = registro.get("bioma")
            nombre_fragmento = registro.get("fragmento")

            if numero_bioma is None:
                continue

            if numero_bioma not in fragmentos_por_bioma:
                fragmentos_por_bioma[numero_bioma] = []

            if nombre_fragmento:
                fragmentos_por_bioma[numero_bioma].append(
                    nombre_fragmento
                )

        # ----------------------------------------------------
        # BIOMAS COMPLETADOS
        # ----------------------------------------------------

        biomas_completados = 0

        for numero in range(1, 11):

            cantidad = len(
                fragmentos_por_bioma.get(numero, [])
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

            st.html(f"""
            <div class="eonia-card"
                 style="text-align:center;">

                <div class="metric-number">
                    {len(fragmentos)}
                </div>

                <div class="metric-label">
                    FRAGMENTOS OBTENIDOS
                </div>

            </div>
            """)

        with col2:

            st.html(f"""
            <div class="eonia-card"
                 style="text-align:center;">

                <div class="metric-number">
                    {biomas_registrados}
                </div>

                <div class="metric-label">
                    BIOMAS COMPLETADOS
                </div>

            </div>
            """)

        with col3:

            st.html(f"""
            <div class="eonia-card"
                 style="text-align:center;">

                <div class="metric-number">
                    {len(certificados)}
                </div>

                <div class="metric-label">
                    CERTIFICADOS
                </div>

            </div>
            """)

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

            # ----------------------------------------------
            # CONTENEDOR DEL BIOMA
            # ----------------------------------------------

            st.html(f"""
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
            """)

            # ----------------------------------------------
            # FRAGMENTOS DEL BIOMA
            # ----------------------------------------------

            if nombres:

                st.html("""
                <div style="
                    margin:-8px 0 22px 20px;
                    padding-left:20px;
                    border-left:1px solid rgba(228,189,92,.25);
                ">
                """)

                for nombre in nombres:

                    st.html(f"""
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
                    """)

                st.html("""
                </div>
                """)

        # ----------------------------------------------------
        # FRASE FINAL
        # ----------------------------------------------------

        st.html("""
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
        """)

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

    st.markdown("### CONEXIÓN CRM")

    st.code(
        SUPABASE_FUNCTIONS_URL,
        language="text"
    )

    st.markdown("### ESTADO")

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
