import os
import io
import base64
import urllib.request
import requests
import streamlit as st

from textwrap import dedent
from PIL import Image


# ============================================================
# EONIA UNIVERSITY
# CRM + CHAT EÓNICO + REFLEJO
# VERSIÓN ESTABLE
# ============================================================

st.set_page_config(
    page_title="EONIA University — Era de los Metales",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURACIÓN DE APIS
# ============================================================

DEEPSEEK_API_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.deepseek.com/v1/chat/completions",
)

OPENAI_CHAT_API_URL = os.getenv(
    "OPENAI_CHAT_API_URL",
    "https://api.openai.com/v1/chat/completions",
)

OPENAI_IMAGE_API_URL = os.getenv(
    "OPENAI_IMAGE_API_URL",
    "https://api.openai.com/v1/images/generations",
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================
# SUPABASE
# ============================================================

SUPABASE_FUNCTIONS_URL = os.getenv(
    "SUPABASE_FUNCTIONS_URL",
    "https://pmshpvjtiauhbuexdjev.supabase.co/functions/v1",
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
    "chat_pregunta": "",
    "busqueda_global": "",
    "chat_mensajes_por_bioma": {},

    "reflejo_ya_generado": False,
    "reflejo_activo": False,
    "reflejo_paso": "bienvenida",
    "reflejo_selfie_subida": False,
    "reflejo_rasgos": "",
    "reflejo_respuestas": {},
    "reflejo_desafio_actual": 0,
    "reflejo_prompt_final": "",
    "reflejo_selfie_b64": "",
}


for clave, valor in DEFAULT_SESSION.items():

    if clave not in st.session_state:

        if isinstance(valor, dict):
            st.session_state[clave] = dict(valor)

        else:
            st.session_state[clave] = valor


# ============================================================
# FUNCIONES HTML
# ============================================================

def html(content):
    """
    Renderiza HTML directamente.

    IMPORTANTE:
    No modifica st.markdown.
    Esto evita la RecursionError que tenía la versión anterior.
    """
    st.html(dedent(content))


# ============================================================
# CSS EONIA
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

    h1,
    h2,
    h3 {
        font-family:
            'Cinzel',
            serif !important;

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
        font-family:
            'Cinzel',
            serif;

        color: #e4bd5c;
        font-size: 14px;
        margin-top: 5px;
    }

    .mentor-role {
        color: #9ba8b5;
        font-size: 11px;
        margin-top: 4px;
    }

    .metric {
        text-align: center;
    }

    .metric-number {
        font-size: 30px;
        color: #e4bd5c;
        font-family:
            'Cinzel',
            serif;
    }

    .metric-label {
        font-size: 11px;
        color: #8f9aa5;
        text-transform: uppercase;
        letter-spacing: .12em;
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

    input,
    textarea {
        color: #eee5ce !important;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"] {
        background-color:
            #0b141f !important;
    }

    hr {
        border-color:
            rgba(212,170,74,.15);
    }

    .eonia-footer {
        text-align: center;
        padding: 60px 10px 30px;
        color: #7f8a95;
    }

    .eonia-footer-title {
        font-family:
            'Cinzel',
            serif;

        font-size: 22px;

        color: #e4bd5c;

        letter-spacing: .08em;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CRM — OBTENER ESTADO
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
            timeout=20,
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


# ============================================================
# CRM — ASIGNAR FRAGMENTO
# ============================================================

def asignar_fragmento(
    user_id,
    bioma,
    fragmento,
):

    if not user_id:

        return {
            "success": False,
            "error": "No hay Creador conectado.",
        }

    try:

        response = requests.post(
            ASIGNAR_FRAGMENTO_URL,
            json={
                "user_id": user_id,
                "bioma": bioma,
                "fragmento": fragmento,
            },
            timeout=20,
        )

        try:

            return response.json()

        except Exception:

            return {
                "success": False,
                "error": response.text,
            }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }


# ============================================================
# REFLEJO — VERIFICAR
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
            timeout=20,
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


# ============================================================
# REFLEJO — GUARDAR
# ============================================================

def guardar_reflejo(
    user_id,
    imagen_base64,
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
            timeout=30,
        )

        return response.status_code == 200

    except Exception:

        return False


# ============================================================
# DOCUMENTACIÓN EONIA
# ============================================================

def cargar_documentacion_eonia():

    posibles_archivos = [
        "documentos EONIA.txt",
        "documentos_EONIA.txt",
        "documentos EONIA.txt",
    ]

    for archivo in posibles_archivos:

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8",
            ) as f:

                return f.read()

        except Exception:

            continue

    return """
EONIA UNIVERSITY

Universidad digital de IA y Metaverso.

MISIÓN:
Democratizar el acceso a la inteligencia artificial
y convertir a los estudiantes en creadores.

VISIÓN:
Construir un estándar global de educación,
creación, IA y Metaverso.

VALORES:
Integridad.
Espiritualidad.
Disciplina.
Astucia.
Audacia.
Efectividad.
Innovación.
Creatividad.
Contestatario.
Anárquico.

PENSUM:
10 Biomas.

PRINCIPIO:
Crear es el acto más humano.
La IA solo lo amplifica.
"""


DOCUMENTACION_EONIA = (
    cargar_documentacion_eonia()
)


# ============================================================
# PRUEBAS
# ============================================================

def cargar_prueba(url):

    if not url:
        return "No existe prueba configurada."

    try:

        with urllib.request.urlopen(
            url,
            timeout=20,
        ) as f:

            return f.read().decode(
                "utf-8"
            )

    except Exception:

        return "Prueba no disponible."


# ============================================================
# MENTORES
# ============================================================

MENTORES = {

    1: {
        "nombre": "Sabio Sereno",
        "identidad": (
            "Eres el Sabio Sereno, mentor de EONIA. "
            "Hablas con calma y metáforas. "
            "Nunca juzgas."
        ),
        "principios": [
            "Calma",
            "Integridad",
            "Espiritualidad",
        ],
        "metodo": (
            "Evalúa con preguntas introspectivas "
            "y metáforas."
        ),
        "sombra": (
            "A veces demasiado contemplativo."
        ),
        "prueba": (
            "https://pmshpvjtiauhbuexdjev.supabase.co/"
            "storage/v1/object/public/pruebas/"
            "Prueba_Bioma1.txt"
        ),
        "fragmento": "Serenidad",
    },

    2: {
        "nombre": "Kael",
        "identidad": (
            "Eres Kael, el Guardián del Método. "
            "Hablas con disciplina y paciencia."
        ),
        "principios": [
            "Disciplina",
            "Constancia",
            "Método",
        ],
        "metodo": (
            "Evalúa con pasos concretos "
            "y celebra pequeños logros."
        ),
        "sombra": (
            "Puede ser rígido si el Creador no avanza."
        ),
        "prueba": (
            "https://pmshpvjtiauhbuexdjev.supabase.co/"
            "storage/v1/object/public/pruebas/"
            "Prueba_Bioma2.txt"
        ),
        "fragmento": "Método",
    },

    3: {
        "nombre": "Némesis",
        "identidad": (
            "Eres Némesis, la Estratega Astuta. "
            "Hablas directo y sin rodeos."
        ),
        "principios": [
            "Efectividad",
            "Astucia",
            "Resultados",
        ],
        "metodo": (
            "Evalúa con retos prácticos "
            "y feedback directo."
        ),
        "sombra": (
            "Puede ser implacable si el Creador "
            "no entrega."
        ),
        "prueba": (
            "https://pmshpvjtiauhbuexdjev.supabase.co/"
            "storage/v1/object/public/pruebas/"
            "Prueba_Bioma3.txt"
        ),
        "fragmento": "Efectividad",
    },

    4: {
        "nombre": "Vórtice",
        "identidad": (
            "Eres Vórtice, el Artista Caótico. "
            "Hablas con energía explosiva y creativa. "
            "Eres provocador, contestatario, "
            "astuto y extremadamente exigente."
        ),
        "principios": [
            "Creatividad",
            "Caos",
            "Rebeldía",
            "Originalidad",
        ],
        "metodo": (
            "Evalúa con desafíos absurdos, "
            "creaciones originales y preguntas "
            "que obliguen al Creador a demostrar "
            "autoría y criterio."
        ),
        "sombra": (
            "Puede perderse en el caos."
        ),
        "prueba": (
            "https://pmshpvjtiauhbuexdjev.supabase.co/"
            "storage/v1/object/public/pruebas/"
            "Prueba_Bioma4.txt"
        ),
        "fragmento": "Creación",
    },
}


# ============================================================
# BIOMAS
# ============================================================

NOMBRES_BIOMAS = [

    (
        1,
        "Fundamentos IA I",
        "Creación de Prompt",
        "ERA DE PIEDRA",
    ),

    (
        2,
        "Fundamentos IA II",
        "Entrenamiento IA",
        "ERA DE PIEDRA",
    ),

    (
        3,
        "Fundamentos IA III",
        "Creación de appIA",
        "ERA DE PIEDRA",
    ),

    (
        4,
        "IA Generativa I",
        "Código IA I · Producto IA",
        "ERA DE LOS METALES",
    ),

    (
        5,
        "IA Generativa II",
        "Código IA II · Software IA",
        "ERA ESTELAR",
    ),

    (
        6,
        "IA Generativa III",
        "Código IA III · Avatar IA",
        "ERA ESTELAR",
    ),

    (
        7,
        "Fundamentos Metaverso I",
        "Historia · Herramientas IA",
        "ERA ESTELAR",
    ),

    (
        8,
        "Fundamentos Metaverso II",
        "Creación Metaverso",
        "ERA TRASCENDENTE",
    ),

    (
        9,
        "Fundamentos Metaverso III",
        "Avatar Metaverso · Avatar IA",
        "ERA TRASCENDENTE",
    ),

    (
        10,
        "Creación de Metaverso",
        "Integración Comercial · Producto",
        "ERA TRASCENDENTE",
    ),
]


# ============================================================
# REFLEJOS
# ============================================================

PROMPTS_REFLEJO = {

    1: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve the person's recognizable identity as much as
possible: face structure, hair, facial hair, glasses if
present, approximate age and overall visual identity.

Transform the scene into the Garden of Origin.

Dark environment, golden mist, Tree of Prompts,
subtle golden technology, elegant clothing.

The image must feel like a future version of the
same Creator, not a random different person.

EONIA visual language.
Black and luminous gold.
Cinematic lighting.
Photorealistic.
""",

    2: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

Transform the environment into an EONIA forge.

The Creator wears practical artisan clothing with
subtle golden geometric patterns.

A glowing anvil represents Method.

Dark waters reflect neural-network constellations.

Black and gold.
Cinematic.
Photorealistic.
""",

    3: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator appears inside a futuristic technological
forge with holographic interfaces and dashboards.

Professional attire.
Golden circuit patterns.
A deployed application appears as a subtle visual symbol.

Black and gold.
Cinematic.
Photorealistic.
""",

    4: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

Transform the scene into the EONIA Crisol of Creation.

Surround the Creator with floating software interfaces,
3D avatars, prototypes and generative structures.

Innovative techwear.
Golden generative patterns.

The Creator must remain visually recognizable as
the person in the reference image.

Black and luminous gold.
Cinematic.
Photorealistic.
""",

    5: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator becomes an emerging architect of intelligent
systems.

Surround them with AI models, code structures,
software systems and digital products.

Black and gold.
Cinematic.
Photorealistic.
""",

    6: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator stands beside a sophisticated AI avatar.

Human identity and artificial intelligence coexist
inside the same visual composition.

Black and luminous gold.
Cinematic.
Photorealistic.
""",

    7: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator stands before a monumental portal.

Beyond it lies a vast EONIA metaverse landscape:
cities, worlds, avatars and digital civilizations.

Black and gold.
Cinematic.
Photorealistic.
""",

    8: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

Physical and digital reality merge around the Creator.

They appear as an architect of a living digital civilization.

Black and luminous gold.
Cinematic.
Photorealistic.
""",

    9: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator stands at the center of a vast metaverse
containing cities, communities, avatars and worlds.

Black and gold.
Cinematic.
Photorealistic.
""",

    10: """
Create a cinematic artistic representation of the same
Creator represented in the supplied reference photograph.

Preserve recognizable identity as much as possible.

The Creator stands inside the Core of EONIA.

Golden light surrounds them.

Applications, avatars, worlds and products orbit
around their presence as symbols of their legacy.

The person must remain recognizable as the same
Creator from the reference photograph.

Black and luminous gold.
Cinematic.
Photorealistic.
""",
}


# ============================================================
# DESAFÍOS DEL REFLEJO
# ============================================================

DESAFIOS_REFLEJO = [

    {
        "titulo": "Desafío 1 — Lógica Creativa",
        "pregunta": (
            "Crea en un suspiro el prompt maestro para "
            "que una IA le explique a una piedra cómo "
            "sentir el viento."
        ),
    },

    {
        "titulo": "Desafío 2 — Dilema Ético",
        "pregunta": (
            "Estás a punto de ganar un hackatón con un "
            "código que no es del todo tuyo. Nadie lo sabrá. "
            "¿Qué haces y por qué?"
        ),
    },

    {
        "titulo": "Desafío 3 — Disciplina",
        "pregunta": (
            "Dime exactamente cómo aplicarías la Disciplina "
            "de EONIA para mejorar un aspecto de tu vida "
            "o creación durante los próximos 30 días."
        ),
    },

    {
        "titulo": "Desafío 4 — Audacia",
        "pregunta": (
            "Convénceme de por qué mereces entrar a EONIA "
            "sin responder de la manera que esperaría "
            "un examen tradicional."
        ),
    },
]


# ============================================================
# OPENAI — GENERACIÓN DE IMAGEN
# ============================================================

def generar_imagen_openai(prompt):

    if not OPENAI_API_KEY:

        return (
            None,
            "No hay OPENAI_API_KEY configurada.",
        )

    try:

        response = requests.post(

            OPENAI_IMAGE_API_URL,

            headers={
                "Authorization":
                    f"Bearer {OPENAI_API_KEY}",

                "Content-Type":
                    "application/json",
            },

            json={
                "model": "gpt-image-1",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "medium",
            },

            timeout=180,
        )

        if response.status_code != 200:

            return (
                None,
                f"Error OpenAI: {response.text}",
            )

        data = response.json()

        if (
            data.get("data")
            and data["data"][0].get("b64_json")
        ):

            return (
                data["data"][0]["b64_json"],
                None,
            )

        return (
            None,
            "Formato de respuesta de OpenAI no esperado.",
        )

    except Exception as e:

        return (
            None,
            f"Error generando imagen: {e}",
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html(
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

    st.markdown("### 👤 CREADOR")

    user_id_input = st.text_input(
        "ID del Creador",
        value=st.session_state.user_id,
        placeholder="UUID del Creador",
        label_visibility="collapsed",
        key="user_id_input",
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
            use_container_width=True,
        ):

            st.session_state.pagina = nombre

            st.rerun()


# ============================================================
# VARIABLES GLOBALES
# ============================================================

user_id = st.session_state.user_id

estado = None

if user_id:

    estado = obtener_estado(user_id)


# ============================================================
# HEADER
# ============================================================

col_logo, col_search, col_user = st.columns(
    [2, 5, 2]
)


with col_logo:

    html(
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
        key="busqueda_global",
    )


with col_user:

    html(
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

    html(
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

    st.write("")

    col1, col2 = st.columns([2, 1])

    with col1:

        html(
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
            """
        )

    with col2:

        html(
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
            """
        )


    st.markdown("## BIOMAS")

    st.caption(
        "Tu camino de aprendizaje, "
        "de la base a la trascendencia."
    )

    b1, b2, b3, b4 = st.columns(4)

    tarjetas = [

        (
            b1,
            "ERA DE PIEDRA",
            "Biomas 1–3",
            "Fundamentos",
            "🌿",
        ),

        (
            b2,
            "ERA DE LOS METALES",
            "Bioma 4",
            "Crisol Eónico",
            "⚒️",
        ),

        (
            b3,
            "ERA ESTELAR",
            "Biomas 5–7",
            "Especialización",
            "✦",
        ),

        (
            b4,
            "ERA TRASCENDENTE",
            "Biomas 8–10",
            "Maestría y Legado",
            "∞",
        ),
    ]

    for (
        col,
        titulo,
        niveles,
        estado_tarjeta,
        icono,
    ) in tarjetas:

        with col:

            html(
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
                        {estado_tarjeta}
                    </p>

                </div>
                """
            )


    st.markdown("## INTELIGENCIA EÓNICA")

    chat_col, council_col = st.columns([2, 1])

    with chat_col:

        html(
            """
            <div class="eonia-card">

                <div class="small-gold">
                    CHAT EÓNICO
                </div>

                <h2>
                    La inteligencia de mentores
                    siempre contigo.
                </h2>

                <p style="
                    color:#a5afb9;
                ">
                    Un solo portal.
                    Múltiples inteligencias.
                </p>

            </div>
            """
        )

        mentors_inicio = [

            ("LUMINA", "Visión"),
            ("DATAC", "Análisis"),
            ("SYNTIA", "Creatividad"),
            ("CODEX", "Construcción"),
            ("VÓRTICE", "Evaluación"),
            ("AION", "Núcleo"),
        ]

        mentor_cols = st.columns(6)

        for col, (
            mentor_nombre,
            role,
        ) in zip(
            mentor_cols,
            mentors_inicio,
        ):

            with col:

                html(
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
                    """
                )

        st.write("")

        pregunta = st.text_input(
            "Pregunta",
            placeholder=(
                "¿En qué podemos ayudarte hoy, Creador?"
            ),
            label_visibility="collapsed",
            key="pregunta_inicio",
        )

        if st.button(
            "Enviar al Chat Eónico  →",
            use_container_width=True,
            key="inicio_chat",
        ):

            if pregunta.strip():

                st.session_state.chat_pregunta = (
                    pregunta
                )

                st.session_state.pagina = (
                    "Chat Eónico"
                )

                st.rerun()

            else:

                st.warning(
                    "Escribe una pregunta antes de entrar."
                )


    with council_col:

        html(
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
            """
        )

        if st.button(
            "Presentar un proyecto →",
            use_container_width=True,
            key="inicio_concilio",
        ):

            st.session_state.pagina = (
                "Concilio Eónico"
            )

            st.rerun()


    st.markdown("## MI UNIVERSO")

    p1, p2, p3, p4 = st.columns(4)

    with p1:

        html(
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
            """
        )

    with p2:

        html(
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
            """
        )

    with p3:

        html(
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
            """
        )

    with p4:

        html(
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
            """
        )


    html(
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

    st.title("MI PERFIL")

    html(
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
        """
    )

    if user_id:

        st.success(
            "Creador conectado al CRM."
        )

        st.caption(
            "Identificador técnico del CRM"
        )

        st.code(
            user_id,
            language="text",
        )

    else:

        st.info(
            "Introduce tu UUID en el panel lateral "
            "para conectar tu perfil."
        )


# ============================================================
# BIOMAS
# ============================================================

elif st.session_state.pagina == "Biomas":

    st.title("BIOMAS")

    html(
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
        """
    )

    for (
        numero,
        titulo,
        descripcion,
        era,
    ) in NOMBRES_BIOMAS:

        html(
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
            """
        )


# ============================================================
# CHAT EÓNICO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title("CHAT EÓNICO")

    st.caption(
        "Un solo portal. Múltiples inteligencias."
    )

    # --------------------------------------------------------
    # VERIFICAR REFLEJO
    # --------------------------------------------------------

    if (
        user_id
        and not st.session_state.reflejo_ya_generado
    ):

        resultado = (
            verificar_reflejo_existente(user_id)
        )

        if (
            resultado
            and resultado.get("existe")
        ):

            st.session_state.reflejo_ya_generado = True


    # --------------------------------------------------------
    # SELECCIÓN DE BIOMA
    # --------------------------------------------------------

    bioma_seleccionado = st.selectbox(

        "Selecciona tu Bioma",

        options=list(MENTORES.keys()),

        format_func=lambda x:
            f"Bioma {x}: {MENTORES[x]['nombre']}",

        key="selector_bioma_chat",
    )

    mentor = MENTORES[
        bioma_seleccionado
    ]


    # --------------------------------------------------------
    # HISTORIAL
    # --------------------------------------------------------

    if (
        bioma_seleccionado
        not in st.session_state.chat_mensajes_por_bioma
    ):

        st.session_state.chat_mensajes_por_bioma[
            bioma_seleccionado
        ] = []


    chat_mensajes = (
        st.session_state.chat_mensajes_por_bioma[
            bioma_seleccionado
        ]
    )


    if not chat_mensajes:

        chat_mensajes.append(
            {
                "role": "assistant",
                "content": (
                    f"Soy **{mentor['nombre']}**. "
                    "¿Qué deseas aprender hoy?"
                ),
            }
        )


    # --------------------------------------------------------
    # MOSTRAR HISTORIAL
    # --------------------------------------------------------

    for mensaje_historial in chat_mensajes:

        with st.chat_message(
            mensaje_historial["role"]
        ):

            st.markdown(
                mensaje_historial["content"]
            )


    # ========================================================
    # REFLEJO ACTIVO
    # ========================================================

    if st.session_state.reflejo_activo:

        # ----------------------------------------------------
        # BIENVENIDA
        # ----------------------------------------------------

        if (
            st.session_state.reflejo_paso
            == "bienvenida"
        ):

            st.info(
                "📸 **Paso 1:** Sube tu selfie "
                "para comenzar el Reflejo Eónico."
            )

            selfie = st.file_uploader(

                "Sube tu selfie aquí",

                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],

                key="selfie_reflejo_ritual",
            )


            if selfie is not None:

                if not OPENAI_API_KEY:

                    st.error(
                        "OPENAI_API_KEY no está configurada."
                    )

                else:

                    with st.spinner(
                        "🔍 La Gran Examinadora "
                        "está analizando tu esencia..."
                    ):

                        try:

                            selfie_bytes = (
                                selfie.getvalue()
                            )

                            selfie_b64 = (
                                base64.b64encode(
                                    selfie_bytes
                                ).decode("utf-8")
                            )

                            mime = (
                                selfie.type
                                or "image/jpeg"
                            )

                            selfie_url = (
                                f"data:{mime};base64,"
                                f"{selfie_b64}"
                            )


                            analisis_response = (
                                requests.post(

                                    OPENAI_CHAT_API_URL,

                                    headers={
                                        "Authorization":
                                            f"Bearer {OPENAI_API_KEY}",

                                        "Content-Type":
                                            "application/json",
                                    },

                                    json={

                                        "model":
                                            "gpt-4o-mini",

                                        "messages": [

                                            {
                                                "role":
                                                    "user",

                                                "content": [

                                                    {
                                                        "type":
                                                            "text",

                                                        "text":
                                                            """
Analiza esta fotografía únicamente para describir
características visuales útiles para una transformación
artística.

Describe:
- forma general del rostro
- cabello
- barba o bigote si existe
- gafas si existen
- expresión
- rasgos visuales distintivos
- composición de la fotografía

No inventes características.

Responde en español.
Máximo 100 palabras.
""",
                                                    },

                                                    {
                                                        "type":
                                                            "image_url",

                                                        "image_url":
                                                            {
                                                                "url":
                                                                    selfie_url
                                                            },
                                                    },

                                                ],
                                            },

                                        ],

                                        "max_tokens":
                                            180,

                                        "temperature":
                                            0.2,
                                    },

                                    timeout=60,
                                )
                            )


                            if (
                                analisis_response
                                .status_code
                                == 200
                            ):

                                data = (
                                    analisis_response.json()
                                )

                                st.session_state.reflejo_rasgos = (
                                    data["choices"][0]
                                    ["message"]
                                    ["content"]
                                )

                            else:

                                st.session_state.reflejo_rasgos = (
                                    "Rasgos visuales "
                                    "no determinados."
                                )


                            st.session_state.reflejo_selfie_b64 = (
                                selfie_b64
                            )

                            st.session_state.reflejo_selfie_subida = (
                                True
                            )

                            st.session_state.reflejo_paso = (
                                "desafio_1"
                            )

                            st.session_state.reflejo_desafio_actual = 0

                            st.rerun()


                        except Exception as e:

                            st.error(
                                f"Error analizando selfie: {e}"
                            )


        # ----------------------------------------------------
        # DESAFÍOS
        # ----------------------------------------------------

        elif (
            st.session_state.reflejo_paso
            .startswith("desafio_")
        ):

            try:

                desafio_num = (
                    int(
                        st.session_state.reflejo_paso
                        .split("_")[1]
                    )
                    - 1
                )

            except Exception:

                desafio_num = 0


            desafio_num = max(
                0,
                min(
                    desafio_num,
                    len(DESAFIOS_REFLEJO) - 1,
                ),
            )


            desafio = (
                DESAFIOS_REFLEJO[
                    desafio_num
                ]
            )


            with st.chat_message(
                "assistant"
            ):

                st.markdown(
                    f"⚔️ **{desafio['titulo']}**"
                )

                st.write("")

                st.write(
                    desafio["pregunta"]
                )


            respuesta = st.text_area(

                f"Tu respuesta al "
                f"Desafío {desafio_num + 1}",

                height=130,

                key=(
                    f"respuesta_desafio_"
                    f"{desafio_num}"
                ),
            )


            if st.button(

                "Enviar respuesta",

                key=(
                    f"enviar_desafio_"
                    f"{desafio_num}"
                ),
            ):

                if not respuesta.strip():

                    st.warning(
                        "Escribe una respuesta antes "
                        "de continuar."
                    )

                else:

                    st.session_state.reflejo_respuestas[
                        desafio_num
                    ] = respuesta.strip()


                    if desafio_num < (
                        len(DESAFIOS_REFLEJO) - 1
                    ):

                        siguiente = (
                            desafio_num + 2
                        )

                        st.session_state.reflejo_paso = (
                            f"desafio_{siguiente}"
                        )

                        st.session_state.reflejo_desafio_actual = (
                            desafio_num + 1
                        )

                        st.rerun()

                    else:

                        st.session_state.reflejo_paso = (
                            "generar_reflejo"
                        )

                        st.rerun()


        # ----------------------------------------------------
        # GENERAR REFLEJO
        # ----------------------------------------------------

        elif (
            st.session_state.reflejo_paso
            == "generar_reflejo"
        ):

            with st.spinner(
                "🌟 La Gran Examinadora "
                "está forjando tu Reflejo Eónico..."
            ):

                prompt_base = (
                    PROMPTS_REFLEJO.get(
                        bioma_seleccionado,
                        PROMPTS_REFLEJO[1],
                    )
                )


                rasgos = (
                    st.session_state.reflejo_rasgos
                    or "preservar la identidad visual de la fotografía"
                )


                prompt_final = (
                    prompt_base
                    + "\n\n"
                    + "CARACTERÍSTICAS VISUALES "
                      "ANALIZADAS DEL CREADOR:\n"
                    + rasgos
                )


                detalles = ""

                for (
                    num,
                    respuesta,
                ) in (
                    st.session_state
                    .reflejo_respuestas
                    .items()
                ):

                    detalles += (
                        f"\nRespuesta al desafío "
                        f"{num + 1}: {respuesta}"
                    )


                prompt_final += (

                    "\n\nLa visión conceptual del futuro "
                    "debe incorporar de forma sutil "
                    "las respuestas del Creador."
                    "\n"
                    + detalles
                )


                st.session_state.reflejo_prompt_final = (
                    prompt_final
                )


                img_b64, error = (
                    generar_imagen_openai(
                        prompt_final
                    )
                )


                if error:

                    st.error(error)

                    st.session_state.reflejo_paso = (
                        "error"
                    )

                else:

                    try:

                        img_bytes = (
                            base64.b64decode(
                                img_b64
                            )
                        )

                        img = Image.open(
                            io.BytesIO(
                                img_bytes
                            )
                        )

                        st.image(
                            img,
                            caption=(
                                "🌟 Tu Reflejo Eónico"
                            ),
                            use_container_width=True,
                        )


                        with st.chat_message(
                            "assistant"
                        ):

                            st.markdown(
                                "✨ **La Gran Examinadora ha hablado.**"
                            )

                            st.write("")

                            st.write(
                                "Este es tu Reflejo Eónico: "
                                "una representación artística "
                                "de tu potencial como Creador."
                            )


                        if user_id:

                            guardado = (
                                guardar_reflejo(
                                    user_id,
                                    img_b64,
                                )
                            )

                            if guardado:

                                st.success(
                                    "✅ Reflejo guardado "
                                    "en tu perfil."
                                )

                                st.session_state.reflejo_ya_generado = (
                                    True
                                )

                            else:

                                st.warning(
                                    "⚠️ El Reflejo se generó, "
                                    "pero no pudo guardarse "
                                    "en Supabase."
                                )


                        st.session_state.reflejo_activo = (
                            False
                        )

                        st.session_state.reflejo_paso = (
                            "bienvenida"
                        )

                        st.session_state.reflejo_selfie_subida = (
                            False
                        )

                        st.session_state.reflejo_respuestas = {}

                        st.session_state.reflejo_desafio_actual = 0


                    except Exception as e:

                        st.error(
                            f"Error procesando imagen: {e}"
                        )


        # ----------------------------------------------------
        # ERROR REFLEJO
        # ----------------------------------------------------

        elif (
            st.session_state.reflejo_paso
            == "error"
        ):

            st.error(
                "El proceso del Reflejo encontró "
                "un problema."
            )

            if st.button(
                "Reiniciar Reflejo",
                key="reiniciar_reflejo",
            ):

                st.session_state.reflejo_activo = False

                st.session_state.reflejo_paso = (
                    "bienvenida"
                )

                st.session_state.reflejo_respuestas = {}

                st.session_state.reflejo_selfie_b64 = ""

                st.rerun()


    # ========================================================
    # ACTIVAR REFLEJO
    # ========================================================

    if not st.session_state.reflejo_activo:

        if not st.session_state.reflejo_ya_generado:

            if st.button(
                "🌟 Forjar mi Reflejo Eónico",
                use_container_width=True,
                key="activar_reflejo",
            ):

                st.session_state.reflejo_activo = True

                st.session_state.reflejo_paso = (
                    "bienvenida"
                )

                st.session_state.reflejo_respuestas = {}

                st.session_state.reflejo_selfie_b64 = ""

                st.rerun()


    # ========================================================
    # CHAT NORMAL
    # ========================================================

    if not st.session_state.reflejo_activo:

        mensaje = st.chat_input(

            "Habla con tu mentor...",

            accept_file=True,

            file_type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],

            max_upload_size=10,
        )


        if mensaje:

            texto = (
                mensaje.text
                if hasattr(
                    mensaje,
                    "text",
                )
                else ""
            )

            archivos = (
                mensaje.files
                if hasattr(
                    mensaje,
                    "files",
                )
                else []
            )


            texto = (
                texto.strip()
                if texto
                else ""
            )


            if not texto and not archivos:

                st.warning(
                    "Escribe un mensaje "
                    "o adjunta una imagen."
                )

            else:

                # ------------------------------------------------
                # MOSTRAR USUARIO
                # ------------------------------------------------

                with st.chat_message(
                    "user"
                ):

                    if texto:

                        st.write(texto)

                    for archivo in archivos:

                        st.image(
                            archivo,
                            caption=(
                                f"🖼️ {archivo.name}"
                            ),
                            use_container_width=True,
                        )


                # ------------------------------------------------
                # DETECTAR REFLEJO
                # ------------------------------------------------

                texto_normalizado = (
                    texto.lower()
                )

                reemplazos = {
                    "á": "a",
                    "é": "e",
                    "í": "i",
                    "ó": "o",
                    "ú": "u",
                    "ñ": "n",
                }

                for (
                    original,
                    nuevo,
                ) in reemplazos.items():

                    texto_normalizado = (
                        texto_normalizado
                        .replace(
                            original,
                            nuevo,
                        )
                    )


                texto_normalizado = (
                    " ".join(
                        texto_normalizado.split()
                    )
                )


                es_reflejo = (
                    texto_normalizado
                    in [
                        "muestrame mi reflejo",
                        "reflejo",
                        "quiero ver mi reflejo",
                        "crear mi reflejo",
                        "generar mi reflejo",
                        "ver mi reflejo",
                    ]
                )


                if es_reflejo:

                    if (
                        st.session_state
                        .reflejo_ya_generado
                    ):

                        with st.chat_message(
                            "assistant"
                        ):

                            st.write(
                                "🌟 Ya has generado "
                                "tu Reflejo Eónico."
                            )

                    else:

                        st.session_state.reflejo_activo = True

                        st.session_state.reflejo_paso = (
                            "bienvenida"
                        )

                        st.rerun()


                else:

                    # --------------------------------------------
                    # GUARDAR MENSAJE
                    # --------------------------------------------

                    contenido_usuario = texto

                    if archivos and not texto:

                        nombres = ", ".join(
                            archivo.name
                            for archivo in archivos
                        )

                        contenido_usuario = (
                            f"[🖼️ Imagen: {nombres}]"
                        )


                    chat_mensajes.append(
                        {
                            "role":
                                "user",

                            "content":
                                contenido_usuario,
                        }
                    )


                    # --------------------------------------------
                    # CRM
                    # --------------------------------------------

                    informacion_usuario = (
                        "No hay información CRM disponible."
                    )


                    if estado:

                        fragmentos = estado.get(
                            "fragmentos",
                            [],
                        )

                        certificados = estado.get(
                            "certificados",
                            [],
                        )


                        fragmentos_por_bioma = {}


                        for registro in fragmentos:

                            numero = registro.get(
                                "bioma"
                            )

                            if numero is None:
                                continue

                            if (
                                numero
                                not in fragmentos_por_bioma
                            ):

                                fragmentos_por_bioma[
                                    numero
                                ] = []

                            fragmentos_por_bioma[
                                numero
                            ].append(registro)


                        biomas_completados = [

                            numero

                            for (
                                numero,
                                registros,
                            ) in (
                                fragmentos_por_bioma
                                .items()
                            )

                            if len(registros) >= 5
                        ]


                        biomas_completados.sort()


                        informacion_usuario = f"""

CREADOR:
{user_id}

FRAGMENTOS OBTENIDOS:
{len(fragmentos)}

BIOMAS COMPLETADOS:
{len(biomas_completados)}

LISTA DE BIOMAS COMPLETADOS:
{
    ", ".join(
        str(b)
        for b in biomas_completados
    )
    if biomas_completados
    else "Ninguno"
}

CERTIFICADOS:
{len(certificados)}
"""


                    # --------------------------------------------
                    # PROMPT
                    # --------------------------------------------

                    prueba = cargar_prueba(
                        mentor["prueba"]
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

DOCUMENTACIÓN EONIA:
{DOCUMENTACION_EONIA[:6000]}

INFORMACIÓN DEL CREADOR:
{informacion_usuario}

PRUEBA DEL BIOMA:
{prueba}

REGLAS:

1. Sé fiel a tu personalidad.
2. Responde en español.
3. No inventes datos del CRM.
4. Si hablas del progreso del Creador,
   utiliza únicamente la información proporcionada.
5. No concedas Fragmentos por conversación.
6. El CRM es la autoridad sobre el progreso oficial.
7. El mentor enseña, desafía y orienta.
8. No afirmes que has modificado el CRM si no lo has hecho.
"""


                    # --------------------------------------------
                    # HISTORIAL PARA API
                    # --------------------------------------------

                    api_messages = [

                        {
                            "role":
                                "system",

                            "content":
                                system_prompt,
                        }
                    ]


                    historial_api = (
                        chat_mensajes[-12:]
                    )


                    for registro in historial_api:

                        role = registro.get(
                            "role"
                        )

                        content = registro.get(
                            "content"
                        )

                        if role in (
                            "user",
                            "assistant",
                        ):

                            api_messages.append(
                                {
                                    "role":
                                        role,

                                    "content":
                                        content,
                                }
                            )


                    # --------------------------------------------
                    # LLAMADA DEEPSEEK
                    # --------------------------------------------

                    respuesta_mentor = ""


                    try:

                        if not DEEPSEEK_API_KEY:

                            respuesta_mentor = (
                                f"**{mentor['nombre']}**\n\n"
                                "La API de DeepSeek "
                                "no está configurada."
                            )

                        else:

                            respuesta_api = (
                                requests.post(

                                    DEEPSEEK_API_URL,

                                    headers={

                                        "Authorization":
                                            f"Bearer {DEEPSEEK_API_KEY}",

                                        "Content-Type":
                                            "application/json",
                                    },

                                    json={

                                        "model":
                                            "deepseek-chat",

                                        "messages":
                                            api_messages,

                                        "max_tokens":
                                            1000,

                                        "temperature":
                                            0.7,
                                    },

                                    timeout=90,
                                )
                            )


                            if (
                                respuesta_api
                                .status_code
                                == 200
                            ):

                                data = (
                                    respuesta_api.json()
                                )

                                respuesta_mentor = (
                                    data["choices"][0]
                                    ["message"]
                                    ["content"]
                                )

                            else:

                                respuesta_mentor = (
                                    "⚠️ El canal de "
                                    "inteligencia externa "
                                    "no respondió correctamente."
                                )


                    except Exception as e:

                        respuesta_mentor = (
                            "⚠️ El canal de inteligencia "
                            "encontró un error.\n\n"
                            f"`{e}`"
                        )


                    # --------------------------------------------
                    # MOSTRAR RESPUESTA
                    # --------------------------------------------

                    with st.chat_message(
                        "assistant"
                    ):

                        st.markdown(
                            respuesta_mentor
                        )


                    # --------------------------------------------
                    # GUARDAR RESPUESTA
                    # --------------------------------------------

                    chat_mensajes.append(
                        {
                            "role":
                                "assistant",

                            "content":
                                respuesta_mentor,
                        }
                    )


# ============================================================
# CONCILIO EÓNICO
# ============================================================

elif st.session_state.pagina == "Concilio Eónico":

    st.title("CONCILIO EÓNICO")

    html(
        """
        <div class="eonia-card">

            <div class="small-gold">
                DELIBERACIÓN
            </div>

            <h1>
                Grandes ideas merecen
                ser deliberadas.
            </h1>

            <p>
                Presenta una creación para que las distintas
                perspectivas de EONIA puedan analizarla.
            </p>

        </div>
        """
    )


    proyecto = st.text_area(

        "Describe tu proyecto",

        height=220,

        placeholder=(
            "¿Qué estás creando?\n\n"
            "¿Qué problema resuelve?\n\n"
            "¿Por qué debería existir?"
        ),

        key="proyecto_concilio",
    )


    st.markdown(
        "### CONSEJO DEL CONCILIO"
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    consejeros = [

        (c1, "LUMINA", "Propósito"),
        (c2, "DATAC", "Evidencia"),
        (c3, "SYNTIA", "Concepto"),
        (c4, "CODEX", "Construcción"),
        (c5, "VÓRTICE", "Contradicción"),
    ]


    for (
        col,
        nombre,
        rol,
    ) in consejeros:

        with col:

            html(
                f"""
                <div class="mentor-card">

                    <div class="mentor-name">
                        {nombre}
                    </div>

                    <div class="mentor-role">
                        {rol}
                    </div>

                </div>
                """
            )


    st.write("")


    if st.button(
        "Presentar al Concilio ⚖️",
        use_container_width=True,
        key="presentar_concilio",
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
# MIS PROYECTOS
# ============================================================

elif st.session_state.pagina == "Mis Proyectos":

    st.title("MIS PROYECTOS")


    proyectos = [

        (
            "Asistente de Aprendizaje Eónico",
            "Bioma 4",
            "En desarrollo",
        ),

        (
            "Universo 3D Educativo",
            "Bioma 5",
            "Borrador",
        ),

        (
            "Impacto Social con IA",
            "Bioma 6",
            "Planificado",
        ),
    ]


    for (
        nombre,
        bioma,
        estado_proyecto,
    ) in proyectos:

        html(
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
            """
        )


# ============================================================
# MIS BECAS
# ============================================================

elif st.session_state.pagina == "Mis Becas":

    st.title("MIS BECAS")


    html(
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
        """
    )


    col1, col2 = st.columns(2)


    with col1:

        html(
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
            """
        )


    with col2:

        html(
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
            """
        )


# ============================================================
# MUSEO
# ============================================================

elif st.session_state.pagina == "Museo de EONIA":

    st.title("MUSEO DE EONIA")


    html(
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
        """
    )


    st.write("")


    m1, m2, m3 = st.columns(3)


    with m1:

        html(
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
            """
        )


    with m2:

        html(
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
            """
        )


    with m3:

        html(
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
            """
        )


# ============================================================
# METAVERSO
# ============================================================

elif st.session_state.pagina == "Metaverso":

    st.title("METAVERSO")


    html(
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
        """
    )


    st.write("")


    col1, col2, col3 = st.columns(3)


    with col1:

        html(
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
            """
        )


    with col2:

        html(
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
            """
        )


    with col3:

        html(
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
            """
        )


# ============================================================
# COMUNIDAD
# ============================================================

elif st.session_state.pagina == "Comunidad":

    st.title("COMUNIDAD")


    html(
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

    st.title("EVENTOS")


    eventos = [

        (
            "Battle Royale Eónico",
            "Competencia de creación y estrategia",
        ),

        (
            "Concilio de Creadores",
            "Deliberación de proyectos",
        ),

        (
            "Forja Eónica",
            "Creación colectiva",
        ),
    ]


    for (
        nombre,
        descripcion,
    ) in eventos:

        html(
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

    st.title("RUTAS PERSONALIZADAS")


    html(
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

    st.title("MI PROGRESO")


    html(
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
            [],
        )

        progreso = estado.get(
            "progreso_biomas",
            [],
        )

        certificados = estado.get(
            "certificados",
            [],
        )


        # ----------------------------------------------------
        # AGRUPAR FRAGMENTOS
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


            if (
                numero_bioma
                not in fragmentos_por_bioma
            ):

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
                    [],
                )
            )

            if cantidad >= 5:

                biomas_completados += 1


        biomas_registrados = max(
            len(progreso),
            biomas_completados,
        )


        # ----------------------------------------------------
        # MÉTRICAS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            html(
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

            html(
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

            html(
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


        st.markdown(
            "## LA FORJA DEL CREADOR"
        )


        st.caption(
            "Cada Bioma se construye reuniendo "
            "sus Fragmentos."
        )


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
            10: "ERA TRASCENDENTE",
        }


        for numero in range(1, 11):

            nombres = (
                fragmentos_por_bioma.get(
                    numero,
                    [],
                )
            )

            cantidad = len(nombres)


            porcentaje = min(
                100,
                int(
                    (cantidad / 5) * 100
                ),
            )


            if cantidad >= 5:

                estado_bioma = "COMPLETADO"

                color_estado = "#e4bd5c"

            elif cantidad > 0:

                estado_bioma = "EN FORJA"

                color_estado = "#8ea8bd"

            else:

                estado_bioma = (
                    "AÚN NO DESPERTADO"
                )

                color_estado = "#66727d"


            lista_fragmentos = (
                ", ".join(nombres)
                if nombres
                else "Sin Fragmentos todavía."
            )


            html(
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
                                {eras[numero]}
                            </h3>

                        </div>

                        <div style="
                            color:{color_estado};
                            font-weight:700;
                            font-size:12px;
                            letter-spacing:.1em;
                        ">
                            {estado_bioma}
                        </div>

                    </div>

                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="
                                width:{porcentaje}%;
                            ">
                        </div>

                    </div>

                    <p style="
                        color:#8e9aa7;
                        margin-top:10px;
                    ">
                        {cantidad} / 5 Fragmentos
                    </p>

                    <p style="
                        color:#b8c0c8;
                    ">
                        {lista_fragmentos}
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

    st.title("CONFIGURACIÓN")


    html(
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


    st.subheader(
        "Estado de las conexiones"
    )


    if DEEPSEEK_API_KEY:

        st.success(
            "✓ DeepSeek configurado"
        )

    else:

        st.warning(
            "○ DeepSeek no configurado"
        )


    if OPENAI_API_KEY:

        st.success(
            "✓ OpenAI configurado"
        )

    else:

        st.warning(
            "○ OpenAI no configurado"
        )


    if user_id:

        st.success(
            "✓ UUID de Creador conectado"
        )

    else:

        st.info(
            "○ No hay UUID conectado"
        )


# ============================================================
# FINAL
# ============================================================

else:

    st.session_state.pagina = "Inicio"

    st.rerun()
