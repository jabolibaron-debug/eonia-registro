import os
import requests
import streamlit as st
from textwrap import dedent

def html(content):
    st.markdown(
        dedent(content),
        unsafe_allow_html=True
    )

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
# CONFIGURACIÓN
# ============================================================

SUPABASE_FUNCTIONS_URL = os.getenv(
    "SUPABASE_FUNCTIONS_URL",
    "https://pmshpvjtiauhbuexdjev.supabase.co/functions/v1"
)

OBTENER_ESTADO_URL = f"{SUPABASE_FUNCTIONS_URL}/obtener_estado"
ASIGNAR_FRAGMENTO_URL = f"{SUPABASE_FUNCTIONS_URL}/asignar_fragmento"

# ============================================================
# ESTILO EONIA
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% 0%, #17283a 0%, #07111d 35%, #02060b 100%);
    color: #f4ead0;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #07121e 0%, #03070c 100%);
    border-right: 1px solid rgba(212,170,74,.35);
}

[data-testid="stSidebar"] * {
    color: #eee5ce;
}

/* TITULOS */

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    letter-spacing: .04em;
}

.gold {
    color: #e4bd5c;
}

.small-gold {
    color: #c9a94c;
    font-size: 12px;
    letter-spacing: .15em;
}

/* TARJETAS */

.eonia-card {
    background:
        linear-gradient(
            145deg,
            rgba(20,38,54,.96),
            rgba(5,12,20,.96)
        );

    border: 1px solid rgba(190,150,65,.38);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 18px;

    box-shadow:
        0 10px 30px rgba(0,0,0,.35),
        inset 0 0 25px rgba(212,170,74,.025);
}

.hero {
    min-height: 360px;

    background:
        linear-gradient(
            90deg,
            rgba(2,7,13,.95),
            rgba(2,7,13,.45),
            rgba(2,7,13,.25)
        ),
        url("https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1800&q=80");

    background-size: cover;
    background-position: center;

    border-radius: 18px;
    border: 1px solid rgba(212,170,74,.4);

    padding: 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero h1 {
    font-size: 42px;
    line-height: 1.05;
    max-width: 650px;
}

.hero p {
    max-width: 620px;
    color: #ddd3bb;
    font-size: 16px;
}

/* MENTORES */

.mentor-card {
    text-align: center;
    padding: 15px 8px;
    border: 1px solid rgba(200,160,70,.25);
    border-radius: 12px;
    background: rgba(5,12,20,.7);
}

.mentor-name {
    font-family: 'Cinzel', serif;
    color: #e4bd5c;
    font-size: 14px;
}

.mentor-role {
    color: #9ba8b5;
    font-size: 11px;
}

/* PROGRESO */

.progress-container {
    background: #172431;
    border-radius: 20px;
    height: 10px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background:
        linear-gradient(90deg, #a87924, #f1d178);
}

/* BOTONES */

.stButton > button {
    background:
        linear-gradient(135deg, #c89d42, #8b6725);

    color: #080b0e;
    border: 0;
    border-radius: 8px;

    font-weight: 700;

    padding: 10px 20px;
}

.stButton > button:hover {
    background:
        linear-gradient(135deg, #f0cf73, #bd8c2e);

    color: #000;
}

/* MÉTRICAS */

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

hr {
    border-color: rgba(212,170,74,.15);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "user_id" not in st.session_state:
    st.session_state.user_id = ""


# ============================================================
# FUNCIONES CRM
# ============================================================

def obtener_estado(user_id):

    try:

        response = requests.post(
            OBTENER_ESTADO_URL,
            json={"user_id": user_id},
            timeout=20
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception as e:

        st.error(f"Error conectando con EONIA: {e}")

        return None


def asignar_fragmento(user_id, bioma, fragmento):

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
        <div style="text-align:center;">
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

            <div class="small-gold">
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
        "⌂  Inicio",
        "◉  Mi Perfil",
        "◈  Biomas",
        "◌  Chat Eónico",
        "♜  Concilio Eónico",
        "◆  Mis Proyectos",
        "◇  Mis Becas",
        "▣  Museo de EONIA",
        "✦  Metaverso",
        "♧  Comunidad",
        "◷  Eventos",
        "⌁  Rutas Personalizadas",
        "◒  Mi Progreso",
        "⚙  Configuración"
    ]

    for opcion in opciones:

        nombre = opcion.split("  ")[-1]

        if st.button(
            opcion,
            key=f"nav_{nombre}",
            use_container_width=True
        ):
            st.session_state.pagina = nombre


# ============================================================
# HEADER
# ============================================================

col_logo, col_search, col_user = st.columns([2, 5, 2])

with col_logo:

    st.markdown(
        """
        <div style="
            font-family:Cinzel;
            font-size:22px;
            letter-spacing:5px;
            color:#e5c46b;
        ">
            EONIA
        </div>
        """,
        unsafe_allow_html=True
    )

with col_search:

    st.text_input(
        "",
        placeholder="Buscar en EONIA...",
        label_visibility="collapsed"
    )

with col_user:

    st.markdown(
        """
        <div style="text-align:right;">
            <span style="color:#e5c46b;">
            ◉
            </span>
            &nbsp;
            <b>Creador Eónico</b><br>
            <small style="color:#8c98a5;">
            Nivel 4 · Era de los Metales
            </small>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# CARGAR ESTADO
# ============================================================

estado = None

if user_id:

    estado = obtener_estado(user_id)


# ============================================================
# PÁGINA INICIO
# ============================================================

if st.session_state.pagina == "Inicio":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

html("""
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
""")

    st.write("")

    # --------------------------------------------------------
    # PROGRESO + FRASE
    # --------------------------------------------------------

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            """
            <div class="eonia-card">

            <div class="small-gold">
            MI PROGRESO
            </div>

            <h2>Nivel 4</h2>

            <div class="progress-container">
                <div class="progress-bar"
                     style="width:65%;">
                </div>
            </div>

            <p style="color:#b9c0c8;">
            Era de los Metales
            </p>

            <hr>

            <b>Siguiente objetivo</b>

            <p style="color:#9da8b2;">
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
                 style="text-align:center;">

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

    for col, titulo, niveles, estado_bioma, icono in biomas:

        with col:

            st.markdown(
                f"""
                <div class="eonia-card"
                     style="text-align:center;
                            min-height:190px;">

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

                    <p style="color:#a5afb9;">
                    {estado_bioma}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # CHAT + CONCILIO
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
            La IA omnisciente de mentores siempre contigo.
            </h2>

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

        for col, (mentor, role) in zip(
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
            "",
            placeholder="¿En qué podemos ayudarte hoy, Creador?",
            label_visibility="collapsed"
        )

        if st.button(
            "Enviar al Chat Eónico  →",
            use_container_width=True
        ):

            if pregunta:

                st.info(
                    "El motor del Chat Eónico se conectará aquí "
                    "con el Mentor Engine."
                )

    with council_col:

        st.markdown(
            """
            <div class="eonia-card">

            <div class="small-gold">
            CONCILIO EÓNICO
            </div>

            <h2>
            Grandes ideas merecen ser deliberadas.
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

            st.session_state.pagina = "Concilio Eónico"


    # ========================================================
    # PROYECTOS / BECAS / MUSEO / METAVERSO
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

            <p style="color:#8e9aa7;">
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
        <div style="
            text-align:center;
            padding:50px 10px;
            margin-top:20px;
        ">

            <div style="
                font-family:Cinzel;
                font-size:22px;
                color:#e4bd5c;
            ">
            “DEL PRIMER PROMPT
            AL IMPACTO ETERNO.”
            </div>

            <div style="
                margin-top:15px;
                color:#7f8a95;
                letter-spacing:3px;
            ">
            EONIA UNIVERSITY
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PÁGINA MI PROGRESO
# ============================================================

elif st.session_state.pagina == "Mi Progreso":

    st.title("MI PROGRESO")

    st.markdown(
        """
        <div class="eonia-card">

        <div class="small-gold">
        VIAJE DEL CREADOR
        </div>

        <h1>
        Era de los Metales
        </h1>

        <p>
        Tu evolución queda registrada en el CRM Eónico.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if estado:

        st.json(estado)

    else:

        st.info(
            "Introduce el UUID del Creador para consultar "
            "el estado real del CRM."
        )


# ============================================================
# PÁGINA BIOMAS
# ============================================================

elif st.session_state.pagina == "Biomas":

    st.title("BIOMAS")

    st.markdown(
        """
        <div class="eonia-card">

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

    for numero in range(1, 11):

        era = (
            "Era de Piedra"
            if numero <= 3
            else
            "Era de los Metales"
            if numero == 4
            else
            "Era Estelar"
            if numero <= 7
            else
            "Era Trascendente"
        )

        st.markdown(
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
            {era}
            </span>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CHAT EÓNICO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title("CHAT EÓNICO")

    st.caption(
        "Un solo portal. Múltiples inteligencias."
    )

    mentor = st.selectbox(
        "Selecciona tu perspectiva",
        [
            "AION — Núcleo",
            "LUMINA — Visión",
            "DATAC — Análisis",
            "SYNTIA — Creatividad",
            "CODEX — Construcción",
            "VÓRTICE — Evaluación"
        ]
    )

    st.markdown(
        f"""
        <div class="eonia-card">

        <div class="small-gold">
        MENTOR ACTIVO
        </div>

        <h1>
        {mentor}
        </h1>

        <p>
        Esta interfaz queda preparada para conectarse
        posteriormente con el Mentor Engine.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    mensaje = st.chat_input(
        "Habla con tu mentor..."
    )

    if mensaje:

        with st.chat_message("user"):
            st.write(mensaje)

        with st.chat_message("assistant"):
            st.write(
                "El Mentor Engine recibirá este mensaje "
                "en la siguiente integración."
            )


# ============================================================
# CONCILIO
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
        Presenta una creación para que las distintas
        perspectivas de EONIA puedan analizarla.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    proyecto = st.text_area(
        "Describe tu proyecto"
    )

    if st.button(
        "Presentar al Concilio ⚖️",
        use_container_width=True
    ):

        if proyecto:

            st.success(
                "Proyecto registrado para deliberación."
            )

            st.write(
                "LUMINA · DATAC · SYNTIA · CODEX · VÓRTICE · AION"
            )


# ============================================================
# PROYECTOS
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

    for nombre, bioma, estado_proyecto in proyectos:

        st.markdown(
            f"""
            <div class="eonia-card">

            <h3>
            {nombre}
            </h3>

            <span class="gold">
            {bioma}
            </span>

            <p style="color:#8f9aa5;">
            {estado_proyecto}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# BECAS
# ============================================================

elif st.session_state.pagina == "Mis Becas":

    st.title("MIS BECAS")

    st.markdown(
        """
        <div class="eonia-card">

        <h2>
        El mérito abre caminos.
        </h2>

        <p>
        Las becas no se compran.
        Se obtienen mediante mérito, creación y deliberación.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MUSEO
# ============================================================

elif st.session_state.pagina == "Museo de EONIA":

    st.title("MUSEO DE EONIA")

    st.markdown(
        """
        <div class="eonia-card">

        <div class="small-gold">
        MUSEO DE LOS ORÍGENES
        </div>

        <h1>
        Aquí comenzó todo.
        </h1>

        <p>
        Primer prompt · Primer fuego · Era de Piedra ·
        Era de los Metales · Futuras eras.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# METAVERSO
# ============================================================

elif st.session_state.pagina == "Metaverso":

    st.title("METAVERSO")

    st.markdown(
        """
        <div class="hero">

        <div class="small-gold">
        EONIA METAVERSE
        </div>

        <h1>
        UN CAMPUS SIN LÍMITES
        </h1>

        <p>
        La universidad deja de ser solamente una interfaz.
        El espacio se convierte en realidad habitable.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PERFIL
# ============================================================

elif st.session_state.pagina == "Mi Perfil":

    st.title("MI PERFIL")

    st.markdown(
        """
        <div class="eonia-card">

        <div class="small-gold">
        IDENTIDAD EÓNICA
        </div>

        <h1>
        Creador Eónico
        </h1>

        <p>
        Nivel 4 · Era de los Metales
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CONFIGURACIÓN
# ============================================================

elif st.session_state.pagina == "Configuración":

    st.title("CONFIGURACIÓN")

    st.info(
        "Configuración del Creador, privacidad, "
        "preferencias de mentores y seguridad."
    )


# ============================================================
# COMUNIDAD / EVENTOS / RUTAS
# ============================================================

else:

    st.title(st.session_state.pagina)

    st.markdown(
        """
        <div class="eonia-card">

        <h2>
        Próximamente
        </h2>

        <p>
        Este módulo forma parte de la arquitectura
        de la Era de los Metales.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
