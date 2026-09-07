import os
import base64
import requests
import streamlit as st


# ============================================================
# EONIA UNIVERSITY
# CRM EÓNICO — APP PRINCIPAL
# ============================================================

st.set_page_config(
    page_title="EONIA University — Era de los Metales",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 1. CONFIGURACIÓN
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

DEEPSEEK_API_URL = (
    "https://api.deepseek.com/v1/chat/completions"
)

OPENAI_CHAT_API_URL = (
    "https://api.openai.com/v1/chat/completions"
)

OPENAI_IMAGE_API_URL = (
    "https://api.openai.com/v1/images/generations"
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# IMPORTANTE:
# El Reflejo visual queda apagado por defecto.
# Esto evita consumir créditos mientras estabilizamos.
ENABLE_REFLEJO_GENERATION = (
    os.getenv(
        "ENABLE_REFLEJO_GENERATION",
        "false",
    ).lower()
    == "true"
)


# ============================================================
# 2. DATOS EÓNICOS
# ============================================================

MENTORES = {
    1: {
        "nombre": "Sabio Sereno",
        "identidad": (
            "Eres el Sabio Sereno, mentor de EONIA. "
            "Hablas con calma, profundidad y metáforas. "
            "Nunca juzgas."
        ),
        "principios": [
            "Calma",
            "Integridad",
            "Espiritualidad",
        ],
        "metodo": (
            "Evalúa mediante preguntas introspectivas "
            "y metáforas."
        ),
        "sombra": (
            "Puede ser demasiado contemplativo."
        ),
        "fragmento": "Serenidad",
        "rol": "Mentor de Integridad",
    },

    2: {
        "nombre": "Kael",
        "identidad": (
            "Eres Kael, el Guardián del Método. "
            "Hablas con disciplina, precisión y paciencia."
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
        "fragmento": "Método",
        "rol": "Guardián del Método",
    },

    3: {
        "nombre": "Némesis",
        "identidad": (
            "Eres Némesis, la Estratega Astuta. "
            "Hablas directo y sin rodeos."
        ),
        "principios": [
            "Astucia",
            "Efectividad",
            "Estrategia",
        ],
        "metodo": (
            "Cuestiona las excusas y busca "
            "resultados concretos."
        ),
        "sombra": (
            "Puede ser demasiado exigente."
        ),
        "fragmento": "Astucia",
        "rol": "Estratega Astuta",
    },

    4: {
        "nombre": "Vórtice",
        "identidad": (
            "Eres Vórtice, el Artista Caótico. "
            "Eres creativo, contestatario y desafiante. "
            "No aceptas respuestas genéricas."
        ),
        "principios": [
            "Creatividad",
            "Audacia",
            "Caos",
        ],
        "metodo": (
            "Rompe patrones, cuestiona convenciones "
            "y exige creación original."
        ),
        "sombra": (
            "Puede llevar al Creador demasiado lejos."
        ),
        "fragmento": "Creatividad",
        "rol": "Artista Caótico",
    },
}


BIOMAS = [
    (
        1,
        "Fundamentos IA I",
        "Creación de Prompt",
        "Era de Piedra",
    ),
    (
        2,
        "Fundamentos IA II",
        "Entrenamiento IA",
        "Era de Piedra",
    ),
    (
        3,
        "Fundamentos IA III",
        "Creación de appIA",
        "Era de Piedra",
    ),
    (
        4,
        "IA Generativa I",
        "Código IA I · Producto IA",
        "Era de los Metales",
    ),
    (
        5,
        "IA Generativa II",
        "Código IA II · Software IA",
        "Era Estelar",
    ),
    (
        6,
        "IA Generativa III",
        "Código IA III · Avatar IA",
        "Era Estelar",
    ),
    (
        7,
        "Fundamentos Metaverso I",
        "Historia · Herramientas IA",
        "Era Estelar",
    ),
    (
        8,
        "Fundamentos Metaverso II",
        "Creación Metaverso",
        "Era Trascendente",
    ),
    (
        9,
        "Fundamentos Metaverso III",
        "Avatar Metaverso · Avatar IA",
        "Era Trascendente",
    ),
    (
        10,
        "Creación de Metaverso",
        "Integración Comercial · Producto",
        "Era Trascendente",
    ),
]


DESAFIOS_REFLEJO = [
    {
        "titulo": "Desafío 1 · Lógica Creativa",
        "pregunta": (
            "Crea en un suspiro el prompt maestro "
            "para que una IA le explique a una piedra "
            "cómo sentir el viento."
        ),
    },
    {
        "titulo": "Desafío 2 · Romper el Molde",
        "pregunta": (
            "Imagina una solución que aparentemente "
            "no debería funcionar. ¿Qué construirías?"
        ),
    },
    {
        "titulo": "Desafío 3 · El Creador contra el Espejo",
        "pregunta": (
            "¿Qué parte de tu forma actual de crear "
            "tendrías que destruir para crear algo mejor?"
        ),
    },
    {
        "titulo": "Desafío 4 · Audacia",
        "pregunta": (
            "¿Qué crearías si supieras que nadie "
            "te puede decir que es imposible?"
        ),
    },
]


PROMPTS_REFLEJO = {
    1: (
        "Crear una representación artística del Yo Futuro "
        "de un Creador Eónico. "
        "Estética EONIA: negro, dorado, tecnología futurista, "
        "luz, datos y arquitectura simbólica. "
        "La imagen debe representar serenidad, "
        "integridad y visión."
    ),

    2: (
        "Crear una representación artística del Yo Futuro "
        "de un Creador Eónico. "
        "Estética EONIA: negro, dorado, tecnología futurista, "
        "geometría, precisión y disciplina. "
        "La imagen debe representar método y evolución."
    ),

    3: (
        "Crear una representación artística del Yo Futuro "
        "de un Creador Eónico. "
        "Estética EONIA: negro, dorado, ciudad futurista, "
        "estrategia, inteligencia y poder creativo. "
        "La imagen debe representar astucia."
    ),

    4: (
        "Crear una representación artística del Yo Futuro "
        "de un Creador Eónico. "
        "Estética EONIA: negro, dorado, caos creativo, "
        "energía, arte, tecnología y transformación. "
        "La imagen debe representar audacia y creatividad."
    ),
}


# ============================================================
# 3. SESSION STATE
# ============================================================

DEFAULT_SESSION = {
    "pagina": "Inicio",
    "user_id": "",
    "mentor_activo": "AION",

    "busqueda_global": "",

    "chat_bioma": 1,
    "chat_mensajes_por_bioma": {},

    "reflejo_activo": False,
    "reflejo_paso": "bienvenida",
    "reflejo_ya_generado": False,
    "reflejo_selfie_subida": False,
    "reflejo_selfie_b64": "",
    "reflejo_rasgos": "",
    "reflejo_respuestas": {},
    "reflejo_desafio_actual": 0,
    "reflejo_prompt_final": "",

    "proyecto_concilio": "",
}


for clave, valor in DEFAULT_SESSION.items():

    if clave not in st.session_state:

        if isinstance(valor, dict):
            st.session_state[clave] = dict(valor)

        else:
            st.session_state[clave] = valor


# ============================================================
# 4. ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap'
    );

    html,
    body,
    [class*="css"] {
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
            1px solid rgba(190,150,65,.38);

        border-radius: 14px;

        padding: 22px;

        margin-bottom: 18px;

        box-shadow:
            0 10px 30px rgba(0,0,0,.35);
    }

    .hero {
        min-height: 360px;

        background:
            linear-gradient(
                90deg,
                rgba(2,7,13,.95),
                rgba(2,7,13,.68),
                rgba(2,7,13,.35)
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
        line-height: 1.7;
    }

    .progress-container {
        background: #172431;
        border-radius: 20px;
        height: 9px;
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

        min-height: 100px;
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

    .eonia-footer {
        text-align: center;
        padding: 60px 10px 30px;
        color: #7f8a95;
    }

    .eonia-footer-title {
        font-family: 'Cinzel', serif;
        font-size: 21px;
        color: #e4bd5c;
        letter-spacing: 1px;
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
        background-color: #0b141f !important;
    }

    hr {
        border-color:
            rgba(212,170,74,.15);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. FUNCIONES CRM
# ============================================================

def obtener_estado(user_id):
    """Consulta el estado del Creador en Supabase."""

    if not user_id:
        return None

    try:

        response = requests.post(
            OBTENER_ESTADO_URL,
            json={
                "user_id": user_id,
            },
            timeout=20,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


def asignar_fragmento(
    user_id,
    bioma,
    fragmento,
):
    """Registra un Fragmento mediante la Edge Function."""

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

        return response.json()

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# 6. FUNCIONES REFLEJO
# ============================================================

def verificar_reflejo_existente(user_id):
    """Consulta si el Creador ya posee un Reflejo."""

    if not user_id:
        return None

    try:

        response = requests.post(
            VERIFICAR_REFLEJO_URL,
            json={
                "user_id": user_id,
            },
            timeout=20,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


def guardar_reflejo(
    user_id,
    imagen_base64,
):
    """Guarda el Reflejo en Supabase."""

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


def analizar_selfie(
    archivo,
    bioma,
):
    """
    Analiza la imagen del Creador.

    IMPORTANTE:
    Esto NO genera todavía una nueva imagen.
    Solamente obtiene una descripción visual.
    """

    if not OPENAI_API_KEY:
        return (
            None,
            "OPENAI_API_KEY no está configurada.",
        )

    try:

        imagen_bytes = archivo.getvalue()

        mime = (
            archivo.type
            or "image/jpeg"
        )

        imagen_base64 = base64.b64encode(
            imagen_bytes
        ).decode("utf-8")

        mentor = MENTORES.get(
            bioma,
            MENTORES[1],
        )

        prompt = f"""
        Analiza esta fotografía para EONIA University.

        El Creador está entrando al Bioma {bioma}.
        Mentor asociado: {mentor['nombre']}.

        Describe solamente características visuales
        relevantes para construir posteriormente
        una representación artística:

        - apariencia general
        - cabello
        - rostro
        - expresión
        - vestimenta
        - postura
        - iluminación
        - elementos visuales distintivos

        No inventes identidad.
        No inventes características que no puedas observar.

        La descripción será utilizada como referencia
        artística para un futuro Reflejo Eónico.
        """

        response = requests.post(
            OPENAI_CHAT_API_URL,
            headers={
                "Authorization":
                    f"Bearer {OPENAI_API_KEY}",
                "Content-Type":
                    "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url":
                                        f"data:{mime};base64,{imagen_base64}",
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 700,
            },
            timeout=90,
        )

        if response.status_code != 200:

            return (
                None,
                f"OpenAI respondió "
                f"{response.status_code}: "
                f"{response.text}",
            )

        data = response.json()

        texto = (
            data["choices"][0]
            ["message"]["content"]
        )

        return (
            {
                "base64": imagen_base64,
                "analisis": texto,
            },
            None,
        )

    except Exception as error:

        return (
            None,
            f"Error analizando la imagen: {error}",
        )


def generar_reflejo_conceptual(
    prompt,
):
    """
    Generación visual antigua/conceptual.

    Está protegida por ENABLE_REFLEJO_GENERATION
    para evitar gasto accidental.

    NOTA:
    Este método genera una nueva imagen.
    NO garantiza conservar exactamente la identidad
    de la fotografía original.
    """

    if not ENABLE_REFLEJO_GENERATION:

        return (
            None,
            "La generación visual está desactivada "
            "para proteger los créditos de la API.",
        )

    if not OPENAI_API_KEY:

        return (
            None,
            "OPENAI_API_KEY no configurada.",
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
            timeout=120,
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

        if (
            data.get("data")
            and data["data"][0].get("url")
        ):

            image_response = requests.get(
                data["data"][0]["url"],
                timeout=60,
            )

            return (
                base64.b64encode(
                    image_response.content
                ).decode("utf-8"),
                None,
            )

        return (
            None,
            "OpenAI devolvió un formato no esperado.",
        )

    except Exception as error:

        return (
            None,
            f"Error generando imagen: {error}",
        )


# ============================================================
# 7. FUNCIONES DE CHAT
# ============================================================

def cargar_prueba(url):
    """
    Carga una prueba desde una URL pública.

    Si falla, devuelve un texto seguro.
    """

    if not url:
        return (
            "No hay una prueba externa configurada."
        )

    try:

        response = requests.get(
            url,
            timeout=15,
        )

        if response.status_code == 200:
            return response.text

        return (
            "No fue posible cargar la prueba."
        )

    except Exception:

        return (
            "No fue posible cargar la prueba."
        )


def construir_system_prompt(
    mentor,
    bioma,
    estado,
):
    """Construye el contexto del mentor."""

    contexto_crm = "No conectado al CRM."

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

        contexto_crm = f"""
        Fragmentos registrados:
        {len(fragmentos)}

        Registros de progreso:
        {len(progreso)}

        Certificados:
        {len(certificados)}
        """

    return f"""
    Eres {mentor['nombre']},
    mentor de EONIA University.

    Bioma actual:
    {bioma}

    Rol:
    {mentor['rol']}

    IDENTIDAD:
    {mentor['identidad']}

    PRINCIPIOS:
    {", ".join(mentor['principios'])}

    MÉTODO:
    {mentor['metodo']}

    SOMBRA:
    {mentor['sombra']}

    ESTADO DEL CREADOR:
    {contexto_crm}

    REGLAS:

    1. Responde en español.
    2. Sé fiel a tu arquetipo.
    3. Enseña y desafía.
    4. No inventes datos del CRM.
    5. No otorgues Fragmentos directamente.
    6. El CRM es la autoridad sobre el progreso.
    7. No regales la respuesta cuando el Creador
       debería descubrirla.
    """


def consultar_deepseek(
    system_prompt,
    historial,
):
    """Envía la conversación a DeepSeek."""

    if not DEEPSEEK_API_KEY:

        return (
            "DeepSeek no está configurado todavía."
        )

    try:

        mensajes = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        for item in historial[-12:]:

            mensajes.append(
                {
                    "role": item["role"],
                    "content": item["content"],
                }
            )

        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                "Authorization":
                    f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type":
                    "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": mensajes,
                "temperature": 0.7,
                "max_tokens": 900,
            },
            timeout=90,
        )

        if response.status_code != 200:

            return (
                f"DeepSeek respondió "
                f"{response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        return (
            data["choices"][0]
            ["message"]["content"]
        )

    except Exception as error:

        return (
            f"Error conectando con DeepSeek: {error}"
        )


def consultar_openai_vision(
    system_prompt,
    historial,
    archivos,
    texto,
):
    """Analiza imágenes enviadas al mentor."""

    if not OPENAI_API_KEY:

        return (
            "OPENAI_API_KEY no está configurada."
        )

    try:

        mensajes = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        for item in historial[-10:]:

            mensajes.append(
                {
                    "role": item["role"],
                    "content": item["content"],
                }
            )

        contenido = [
            {
                "type": "text",
                "text": (
                    texto
                    or "Analiza la imagen enviada."
                ),
            }
        ]

        for archivo in archivos:

            imagen_bytes = archivo.getvalue()

            mime = (
                archivo.type
                or "image/jpeg"
            )

            imagen_base64 = base64.b64encode(
                imagen_bytes
            ).decode("utf-8")

            contenido.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url":
                            f"data:{mime};base64,{imagen_base64}",
                    },
                }
            )

        mensajes.append(
            {
                "role": "user",
                "content": contenido,
            }
        )

        response = requests.post(
            OPENAI_CHAT_API_URL,
            headers={
                "Authorization":
                    f"Bearer {OPENAI_API_KEY}",
                "Content-Type":
                    "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": mensajes,
                "max_tokens": 900,
            },
            timeout=90,
        )

        if response.status_code != 200:

            return (
                f"OpenAI respondió "
                f"{response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        return (
            data["choices"][0]
            ["message"]["content"]
        )

    except Exception as error:

        return (
            f"Error conectando con OpenAI: {error}"
        )


# ============================================================
# 8. SIDEBAR
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
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 👤 CREADOR")

    user_id_input = st.text_input(
        "ID del Creador",
        value=st.session_state.user_id,
        placeholder="UUID del Creador",
        label_visibility="collapsed",
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
# 9. ESTADO CRM
# ============================================================

user_id = st.session_state.user_id

estado = None

if user_id:

    estado = obtener_estado(
        user_id
    )


# ============================================================
# 10. HEADER
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
        unsafe_allow_html=True,
    )


with col_search:

    st.text_input(
        "Buscar",
        placeholder="Buscar en EONIA...",
        label_visibility="collapsed",
        key="busqueda_global",
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
        unsafe_allow_html=True,
    )


st.divider()


# ============================================================
# 11. INICIO
# ============================================================

if st.session_state.pagina == "Inicio":

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
        unsafe_allow_html=True,
    )

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
                        style="width:40%;">
                    </div>
                </div>

                <p style="
                    color:#aeb7c0;
                ">
                    Tu evolución queda registrada
                    en el CRM Eónico.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
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
                    El conocimiento comienza
                    a convertirse en creación.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## BIOMAS")

    era_cards = [
        (
            "🌿",
            "ERA DE PIEDRA",
            "BIOMAS 1–3",
            "Fundamentos",
        ),
        (
            "⚒️",
            "ERA DE LOS METALES",
            "BIOMA 4",
            "Creación",
        ),
        (
            "✦",
            "ERA ESTELAR",
            "BIOMAS 5–7",
            "Especialización",
        ),
        (
            "∞",
            "ERA TRASCENDENTE",
            "BIOMAS 8–10",
            "Legado",
        ),
    ]

    columnas = st.columns(4)

    for col, datos in zip(
        columnas,
        era_cards,
    ):

        icono, titulo, niveles, descripcion = datos

        with col:

            st.markdown(
                f"""
                <div class="eonia-card"
                     style="
                        text-align:center;
                        min-height:180px;
                     ">

                    <div style="
                        font-size:38px;
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
                        {descripcion}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("## INTELIGENCIA EÓNICA")

    mentores_home = [
        ("LUMINA", "Visión"),
        ("DATAC", "Análisis"),
        ("SYNTIA", "Creatividad"),
        ("CODEX", "Construcción"),
        ("VÓRTICE", "Evaluación"),
        ("AIÓN", "Núcleo"),
    ]

    columnas = st.columns(6)

    for col, datos in zip(
        columnas,
        mentores_home,
    ):

        nombre, rol = datos

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
                        {nombre}
                    </div>

                    <div class="mentor-role">
                        {rol}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("## MI UNIVERSO")

    p1, p2, p3, p4 = st.columns(4)

    tarjetas = [
        (
            p1,
            "MIS PROYECTOS",
            "3",
            "Creaciones en desarrollo.",
        ),
        (
            p2,
            "MIS BECAS",
            "🏆",
            "Becas otorgadas por mérito.",
        ),
        (
            p3,
            "MUSEO DE EONIA",
            "🏛️",
            "La memoria de los Creadores.",
        ),
        (
            p4,
            "METAVERSO",
            "✦",
            "Un campus sin límites.",
        ),
    ]

    for col, titulo, numero, texto in tarjetas:

        with col:

            st.markdown(
                f"""
                <div class="eonia-card">

                    <div class="small-gold">
                        {titulo}
                    </div>

                    <h3>
                        {numero}
                    </h3>

                    <p>
                        {texto}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

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
        unsafe_allow_html=True,
    )


# ============================================================
# 12. MI PERFIL
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
        unsafe_allow_html=True,
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
# 13. BIOMAS
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
        unsafe_allow_html=True,
    )

    for (
        numero,
        titulo,
        descripcion,
        era,
    ) in BIOMAS:

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
            unsafe_allow_html=True,
        )


# ============================================================
# 14. CHAT EÓNICO
# ============================================================

elif st.session_state.pagina == "Chat Eónico":

    st.title("CHAT EÓNICO")

    st.caption(
        "Un solo portal. Múltiples inteligencias."
    )

    bioma_seleccionado = st.selectbox(
        "Selecciona tu Bioma",
        options=list(MENTORES.keys()),
        format_func=lambda x:
            f"Bioma {x}: {MENTORES[x]['nombre']}",
        key="chat_bioma",
    )

    mentor = MENTORES[
        bioma_seleccionado
    ]

    if (
        bioma_seleccionado
        not in st.session_state.chat_mensajes_por_bioma
    ):

        st.session_state.chat_mensajes_por_bioma[
            bioma_seleccionado
        ] = []

    historial = (
        st.session_state
        .chat_mensajes_por_bioma[
            bioma_seleccionado
        ]
    )

    st.markdown(
        f"""
        <div class="eonia-card">

            <div class="small-gold">
                MENTOR ACTIVO
            </div>

            <h1>
                {mentor['nombre']}
            </h1>

            <p>
                {mentor['rol']}
            </p>

            <p style="
                color:#9da8b2;
            ">
                {mentor['identidad']}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # REFLEJO
    # --------------------------------------------------------

    st.markdown("## ✦ REFLEJO")

    if st.session_state.reflejo_ya_generado:

        st.success(
            "Este Creador ya posee un Reflejo registrado."
        )

    else:

        if st.button(
            "Despertar mi Reflejo",
            use_container_width=True,
            key="activar_reflejo",
        ):

            st.session_state.reflejo_activo = True
            st.session_state.reflejo_paso = "bienvenida"
            st.session_state.reflejo_respuestas = {}
            st.session_state.reflejo_desafio_actual = 0
            st.rerun()

    # --------------------------------------------------------
    # FLUJO REFLEJO
    # --------------------------------------------------------

    if st.session_state.reflejo_activo:

        st.divider()

        if (
            st.session_state.reflejo_paso
            == "bienvenida"
        ):

            st.markdown(
                """
                <div class="eonia-card">

                    <div class="small-gold">
                        EL UMBRAL DEL REFLEJO
                    </div>

                    <h2>
                        La Gran Examinadora te observa.
                    </h2>

                    <p>
                        Antes de mostrarte tu Yo Futuro,
                        tendrás que demostrar quién eres
                        cuando nadie puede darte la respuesta.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Entrar al Umbral →",
                key="entrar_umbral",
            ):

                st.session_state.reflejo_paso = (
                    "selfie"
                )

                st.rerun()

        elif (
            st.session_state.reflejo_paso
            == "selfie"
        ):

            st.subheader(
                "Primera puerta · Tu presencia"
            )

            archivo = st.file_uploader(
                "Sube una fotografía tuya",
                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],
                key="reflejo_selfie",
            )

            if archivo:

                st.image(
                    archivo,
                    caption="Fotografía del Creador",
                    use_container_width=True,
                )

                if st.button(
                    "Analizar mi esencia →",
                    key="analizar_reflejo",
                ):

                    with st.spinner(
                        "La Gran Examinadora está observando..."
                    ):

                        resultado, error = (
                            analizar_selfie(
                                archivo,
                                bioma_seleccionado,
                            )
                        )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.reflejo_selfie_subida = True

                        st.session_state.reflejo_selfie_b64 = (
                            resultado["base64"]
                        )

                        st.session_state.reflejo_rasgos = (
                            resultado["analisis"]
                        )

                        st.session_state.reflejo_paso = (
                            "desafio_1"
                        )

                        st.rerun()

        elif st.session_state.reflejo_paso.startswith(
            "desafio_"
        ):

            desafio_num = int(
                st.session_state.reflejo_paso.split(
                    "_"
                )[1]
            ) - 1

            desafio = DESAFIOS_REFLEJO[
                desafio_num
            ]

            st.markdown(
                f"""
                <div class="eonia-card">

                    <div class="small-gold">
                        PRUEBA DE FUEGO
                    </div>

                    <h2>
                        {desafio['titulo']}
                    </h2>

                    <p>
                        {desafio['pregunta']}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            respuesta = st.text_area(
                "Tu respuesta",
                height=140,
                key=f"reflejo_respuesta_{desafio_num}",
            )

            if st.button(
                "Enviar respuesta →",
                key=f"enviar_reflejo_{desafio_num}",
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

                    if desafio_num < 3:

                        st.session_state.reflejo_paso = (
                            f"desafio_{desafio_num + 2}"
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

        elif (
            st.session_state.reflejo_paso
            == "generar_reflejo"
        ):

            st.markdown(
                """
                <div class="eonia-card">

                    <div class="small-gold">
                        FORJA DEL REFLEJO
                    </div>

                    <h2>
                        La visión está tomando forma.
                    </h2>

                    <p>
                        Hemos reunido tu presencia,
                        tus respuestas y el arquetipo
                        del Bioma.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            prompt_base = PROMPTS_REFLEJO.get(
                bioma_seleccionado,
                PROMPTS_REFLEJO[1],
            )

            detalles = ""

            for numero, respuesta in (
                st.session_state
                .reflejo_respuestas
                .items()
            ):

                detalles += (
                    f"\nRespuesta al desafío "
                    f"{numero + 1}: "
                    f"{respuesta}"
                )

            prompt_final = (
                prompt_base
                + "\n\nCaracterísticas observadas:"
                + "\n"
                + st.session_state.reflejo_rasgos
                + "\n\nRespuestas del Creador:"
                + detalles
            )

            st.session_state.reflejo_prompt_final = (
                prompt_final
            )

            if not ENABLE_REFLEJO_GENERATION:

                st.warning(
                    "La generación visual está "
                    "temporalmente desactivada para "
                    "proteger los créditos de la API."
                )

                st.info(
                    "El motor ya construyó el concepto "
                    "del Reflejo. Cuando activemos la "
                    "generación visual, esta etapa "
                    "producirá la imagen."
                )

                with st.expander(
                    "Ver concepto interno"
                ):

                    st.write(
                        st.session_state
                        .reflejo_rasgos
                    )

                if st.button(
                    "Cerrar el proceso",
                    key="cerrar_reflejo",
                ):

                    st.session_state.reflejo_activo = False
                    st.session_state.reflejo_paso = "bienvenida"

                    st.rerun()

            else:

                with st.spinner(
                    "Forjando tu Reflejo Eónico..."
                ):

                    imagen_b64, error = (
                        generar_reflejo_conceptual(
                            prompt_final
                        )
                    )

                if error:

                    st.error(error)

                else:

                    imagen_bytes = base64.b64decode(
                        imagen_b64
                    )

                    st.image(
                        imagen_bytes,
                        caption="🌟 Tu Reflejo Eónico",
                        use_container_width=True,
                    )

                    if user_id:

                        guardado = guardar_reflejo(
                            user_id,
                            imagen_b64,
                        )

                        if guardado:

                            st.success(
                                "Reflejo guardado "
                                "en tu perfil."
                            )

                            st.session_state.reflejo_ya_generado = True

                        else:

                            st.warning(
                                "El Reflejo se generó, "
                                "pero no pudo guardarse "
                                "en Supabase."
                            )

                    st.session_state.reflejo_activo = False
                    st.session_state.reflejo_paso = "bienvenida"

    # --------------------------------------------------------
    # CHAT NORMAL
    # --------------------------------------------------------

    st.divider()

    st.markdown("## CONVERSACIÓN")

    if not historial:

        historial.append(
            {
                "role": "assistant",
                "content": (
                    f"Soy **{mentor['nombre']}**. "
                    "¿Qué deseas aprender hoy?"
                ),
            }
        )

    for mensaje in historial:

        with st.chat_message(
            mensaje["role"]
        ):

            st.markdown(
                mensaje["content"]
            )

    mensaje_entrada = st.chat_input(
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

    if mensaje_entrada:

        texto = (
            mensaje_entrada.text
            or ""
        )

        archivos = (
            mensaje_entrada.files
            or []
        )

        texto = texto.strip()

        if not texto and not archivos:

            st.warning(
                "Escribe un mensaje o adjunta una imagen."
            )

        else:

            if texto:

                historial.append(
                    {
                        "role": "user",
                        "content": texto,
                    }
                )

            with st.chat_message("user"):

                if texto:
                    st.write(texto)

                for archivo in archivos:

                    st.image(
                        archivo,
                        caption=archivo.name,
                        use_container_width=True,
                    )

            system_prompt = construir_system_prompt(
                mentor,
                bioma_seleccionado,
                estado,
            )

            if archivos:

                respuesta_texto = (
                    consultar_openai_vision(
                        system_prompt,
                        historial[:-1]
                        if texto
                        else historial,
                        archivos,
                        texto,
                    )
                )

            else:

                respuesta_texto = (
                    consultar_deepseek(
                        system_prompt,
                        historial,
                    )
                )

            historial.append(
                {
                    "role": "assistant",
                    "content": respuesta_texto,
                }
            )

            with st.chat_message("assistant"):

                st.markdown(
                    respuesta_texto
                )


# ============================================================
# 15. CONCILIO EÓNICO
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
                Presenta una creación para analizarla
                desde distintas perspectivas.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    proyecto = st.text_area(
        "Describe tu proyecto",
        value=st.session_state.proyecto_concilio,
        height=220,
        placeholder=(
            "¿Qué estás creando?\n\n"
            "¿Qué problema resuelve?\n\n"
            "¿Por qué debería existir?"
        ),
    )

    consejeros = [
        ("LUMINA", "Propósito"),
        ("DATAC", "Evidencia"),
        ("SYNTIA", "Concepto"),
        ("CODEX", "Construcción"),
        ("VÓRTICE", "Contradicción"),
    ]

    columnas = st.columns(5)

    for col, datos in zip(
        columnas,
        consejeros,
    ):

        nombre, rol = datos

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
                unsafe_allow_html=True,
            )

    if st.button(
        "Presentar al Concilio ⚖️",
        use_container_width=True,
    ):

        if proyecto.strip():

            st.session_state.proyecto_concilio = (
                proyecto.strip()
            )

            st.success(
                "Proyecto registrado para deliberación."
            )

            st.info(
                "El Mentor Engine multiagente "
                "se conectará en la siguiente etapa."
            )

        else:

            st.warning(
                "Describe primero el proyecto."
            )


# ============================================================
# 16. MIS PROYECTOS
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

    for nombre, bioma, estado_proyecto in proyectos:

        st.markdown(
            f"""
            <div class="eonia-card">

                <div class="small-gold">
                    PROYECTO
                </div>

                <h2>
                    {nombre}
                </h2>

                <div class="gold">
                    {bioma}
                </div>

                <p style="
                    color:#8f9aa5;
                ">
                    {estado_proyecto}
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 17. MIS BECAS
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
        unsafe_allow_html=True,
    )


# ============================================================
# 18. MUSEO
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
                Primer CRM · Primeras creaciones.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    piezas = [
        (
            "GENESIS",
            "Primer Prompt",
            "El origen conceptual de EONIA.",
        ),
        (
            "ERA DE PIEDRA",
            "Primer CRM",
            "El comienzo de la memoria digital.",
        ),
        (
            "ERA DE LOS METALES",
            "Chat Eónico",
            "La evolución hacia múltiples inteligencias.",
        ),
    ]

    columnas = st.columns(3)

    for col, datos in zip(
        columnas,
        piezas,
    ):

        era, titulo, texto = datos

        with col:

            st.markdown(
                f"""
                <div class="eonia-card">

                    <div class="small-gold">
                        {era}
                    </div>

                    <h2>
                        {titulo}
                    </h2>

                    <p>
                        {texto}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 19. METAVERSO
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
        unsafe_allow_html=True,
    )

    contenidos = [
        (
            "🌌",
            "ESPACIOS",
            "Mundos digitales construidos por los Creadores.",
        ),
        (
            "🤖",
            "INTELIGENCIAS",
            "Mentores que acompañan la evolución.",
        ),
        (
            "✦",
            "CREACIÓN",
            "El conocimiento convertido en experiencia.",
        ),
    ]

    columnas = st.columns(3)

    for col, datos in zip(
        columnas,
        contenidos,
    ):

        icono, titulo, texto = datos

        with col:

            st.markdown(
                f"""
                <div class="eonia-card">

                    <h2>
                        {icono}
                    </h2>

                    <div class="small-gold">
                        {titulo}
                    </div>

                    <p>
                        {texto}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 20. COMUNIDAD
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
        unsafe_allow_html=True,
    )

    st.info(
        "La comunidad eónica será ampliada "
        "en una siguiente etapa."
    )


# ============================================================
# 21. EVENTOS
# ============================================================

elif st.session_state.pagina == "Eventos":

    st.title("EVENTOS")

    eventos = [
        (
            "Battle Royale Eónico",
            "Competencia de creación y estrategia.",
        ),
        (
            "Concilio de Creadores",
            "Deliberación de proyectos.",
        ),
        (
            "Forja Eónica",
            "Creación colectiva.",
        ),
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
            unsafe_allow_html=True,
        )


# ============================================================
# 22. RUTAS PERSONALIZADAS
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
        unsafe_allow_html=True,
    )

    st.info(
        "La personalización avanzada se conectará "
        "al Mentor Engine."
    )


# ============================================================
# 23. MI PROGRESO
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
                ERA DE LOS METALES
            </h1>

            <p>
                Cada Fragmento obtenido queda integrado
                en tu historia de creación.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not estado:

        st.info(
            "Introduce el UUID del Creador "
            "para consultar el CRM."
        )

    else:

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

            if numero_bioma not in (
                fragmentos_por_bioma
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

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
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
                """,
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"""
                <div class="eonia-card"
                     style="text-align:center;">

                    <div class="metric-number">
                        {biomas_registrados}
                    </div>

                    <div class="metric-label">
                        BIOMAS REGISTRADOS
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:

            st.markdown(
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
                """,
                unsafe_allow_html=True,
            )

        st.markdown("## LA FORJA DEL CREADOR")

        st.caption(
            "Cada Bioma se construye reuniendo sus Fragmentos."
        )

        for numero in range(1, 11):

            nombres = fragmentos_por_bioma.get(
                numero,
                [],
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
                color = "#e4bd5c"

            elif cantidad > 0:

                estado_bioma = "EN FORJA"
                color = "#8ea8bd"

            else:

                estado_bioma = (
                    "AÚN NO DESPERTADO"
                )

                color = "#66727d"

            st.markdown(
                f"""
                <div class="eonia-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <div>

                            <div class="small-gold">
                                BIOMA {numero}
                            </div>

                            <h2>
                                {cantidad} / 5 Fragmentos
                            </h2>

                        </div>

                        <div style="
                            color:{color};
                            font-size:12px;
                            letter-spacing:2px;
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

                </div>
                """,
                unsafe_allow_html=True,
            )

            for nombre in nombres:

                st.markdown(
                    f"""
                    <div style="
                        margin-left:25px;
                        padding:7px 0;
                        color:#f4ead0;
                    ">
                        ◆ {nombre}

                        <span style="
                            float:right;
                            color:#e4bd5c;
                            font-size:11px;
                        ">
                            OBTENIDO
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# 24. CONFIGURACIÓN
# ============================================================

elif st.session_state.pagina == "Configuración":

    st.title("CONFIGURACIÓN")

    st.markdown(
        """
        <div class="eonia-card">

            <div class="small-gold">
                SISTEMA EÓNICO
            </div>

            <h1>
                CONFIGURACIÓN
            </h1>

            <p>
                Configuración de servicios y conexiones
                de EONIA University.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ESTADO DE SERVICIOS")

    if DEEPSEEK_API_KEY:

        st.success(
            "DeepSeek API configurada."
        )

    else:

        st.warning(
            "DeepSeek API no configurada."
        )

    if OPENAI_API_KEY:

        st.success(
            "OpenAI API configurada."
        )

    else:

        st.warning(
            "OpenAI API no configurada."
        )

    if ENABLE_REFLEJO_GENERATION:

        st.warning(
            "Generación visual del Reflejo ACTIVADA."
        )

    else:

        st.info(
            "Generación visual del Reflejo "
            "DESACTIVADA para proteger créditos."
        )

    st.markdown("### SUPABASE")

    st.code(
        SUPABASE_FUNCTIONS_URL,
        language="text",
    )


# ============================================================
# 25. FOOTER GLOBAL
# ============================================================

st.markdown(
    """
    <div class="eonia-footer">

        <div class="eonia-footer-title">
            CREAR ES EL ACTO MÁS HUMANO.
        </div>

        <div style="
            margin-top:10px;
            letter-spacing:3px;
            font-size:11px;
        ">
            EONIA UNIVERSITY
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
