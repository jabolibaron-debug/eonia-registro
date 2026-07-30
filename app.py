import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import datetime

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://pmshpvjtiauhbuexdjev.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2hwdmp0aWF1aGJ1ZXhkamV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ4ODI0MDgsImV4cCI6MjEwMDQ1ODQwOH0.gm_oWPgwjZe_6iN9sLsVjFOus7nN0eUBwkJ2bbbbVc4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="EONIA - Portal del Creador", page_icon="🔷", layout="wide")

# -------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------------

def iniciar_sesion(email, password):
    """Inicia sesión con Supabase Auth"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return None

def registrar_usuario(email, password, nombre, celular):
    """Registra un nuevo usuario en Supabase Auth y guarda sus datos"""
    try:
        # Crear usuario en Auth
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        # Guardar datos adicionales en la tabla suscriptores (reutilizamos la existente)
        data = {
            "nombre": nombre,
            "email": email,
            "celular": celular
        }
        supabase.table("suscriptores").insert(data).execute()
        return response
    except Exception as e:
        return None

def obtener_fragmentos(user_id):
    """Obtiene los Fragmentos de un Creador"""
    response = supabase.table("fragmentos_obtenidos").select("*").eq("user_id", user_id).execute()
    return response.data if response.data else []

def obtener_progreso(user_id):
    """Obtiene el progreso por Bioma de un Creador"""
    response = supabase.table("progreso_biomas").select("*").eq("user_id", user_id).execute()
    return response.data if response.data else []

def obtener_certificados(user_id):
    """Obtiene los certificados de un Creador"""
    response = supabase.table("certificados").select("*").eq("user_id", user_id).execute()
    return response.data if response.data else []

def asignar_fragmento(user_id, bioma, fragmento):
    """Asigna un Fragmento a un Creador (para uso del admin o mentores)"""
    data = {
        "user_id": user_id,
        "bioma": bioma,
        "fragmento": fragmento
    }
    supabase.table("fragmentos_obtenidos").insert(data).execute()

def completar_bioma(user_id, bioma):
    """Marca un Bioma como completado"""
    data = {
        "user_id": user_id,
        "bioma": bioma,
        "completado": True,
        "fecha_completado": datetime.datetime.now().isoformat()
    }
    supabase.table("progreso_biomas").upsert(data).execute()

# -------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -------------------------------------------------------------------

# Si no hay sesión, mostrar Login o Registro
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    # Menú de Login / Registro
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

    with tab1:
        st.subheader("🔑 Iniciar Sesión")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Contraseña", type="password", key="login_password")
        if st.button("Entrar"):
            response = iniciar_sesion(login_email, login_password)
            if response and response.user:
                st.session_state.user = response.user
                st.success("¡Bienvenido de nuevo, Creador!")
                st.rerun()
            else:
                st.error("Email o contraseña incorrectos.")

    with tab2:
        st.subheader("🔷 Crear Cuenta")
        reg_nombre = st.text_input("Nombre completo", key="reg_nombre")
        reg_email = st.text_input("Email", key="reg_email")
        reg_celular = st.text_input("Celular", key="reg_celular")
        reg_password = st.text_input("Contraseña", type="password", key="reg_password")
        if st.button("Registrarse"):
            if not reg_nombre or not reg_email or not reg_celular or not reg_password:
                st.error("Todos los campos son obligatorios.")
            elif "@" not in reg_email:
                st.error("Ingresa un email válido.")
            else:
                response = registrar_usuario(reg_email, reg_password, reg_nombre, reg_celular)
                if response and response.user:
                    st.success("¡Cuenta creada! Ahora inicia sesión.")
                else:
                    st.error("Error al crear la cuenta. El email puede estar en uso.")

else:
    # -------------------------------------------------------------------
    # USUARIO AUTENTICADO - PORTAL DEL CREADOR
    # -------------------------------------------------------------------
    user = st.session_state.user

    # Menú lateral
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=EONIA", width=80)
        st.title(f"🔷 {user.email}")

        menu = option_menu(
            menu_title="Portal del Creador",
            options=["Mi Perfil", "Mis Fragmentos", "Progreso", "Certificados", "Cerrar Sesión"],
            icons=["person", "gem", "bar-chart", "award", "box-arrow-right"],
            default_index=0
        )

    # -------------------------------------------------------------------
    # PÁGINA: MI PERFIL
    # -------------------------------------------------------------------
    if menu == "Mi Perfil":
        st.title("👤 Mi Perfil")
        st.write(f"**Email:** {user.email}")
        st.write(f"**ID del Creador:** {user.id}")

        # Mostrar progreso general
        progreso = obtener_progreso(user.id)
        biomas_completados = [p["bioma"] for p in progreso if p["completado"]]
        st.metric("Biomas Completados", len(biomas_completados))

        st.divider()
        st.link_button("🌐 Volver a eoniauniversity.com", "https://eoniauniversity.com")

    # -------------------------------------------------------------------
    # PÁGINA: MIS FRAGMENTOS
    # -------------------------------------------------------------------
    elif menu == "Mis Fragmentos":
        st.title("💎 Mis Fragmentos")
        fragmentos = obtener_fragmentos(user.id)

        if fragmentos:
            # Agrupar por Bioma
            biomas = {}
            for f in fragmentos:
                bioma = f["bioma"]
                if bioma not in biomas:
                    biomas[bioma] = []
                biomas[bioma].append(f["fragmento"])

            for bioma, frags in sorted(biomas.items()):
                with st.expander(f"🌿 Bioma {bioma} — {len(frags)}/5 Fragmentos"):
                    for frag in frags:
                        st.write(f"✅ {frag}")
                    if len(frags) == 5:
                        st.success("✨ ¡Bioma completado!")
        else:
            st.info("Aún no has obtenido ningún Fragmento. Completa tu primer Bioma para verlos aquí.")

    # -------------------------------------------------------------------
    # PÁGINA: PROGRESO
    # -------------------------------------------------------------------
    elif menu == "Progreso":
        st.title("📊 Progreso por Biomas")
        progreso = obtener_progreso(user.id)

        for bioma_num in range(1, 11):
            completado = any(p["bioma"] == bioma_num and p["completado"] for p in progreso)
            if completado:
                st.success(f"🌿 Bioma {bioma_num} — ✅ Completado")
            else:
                st.info(f"🌿 Bioma {bioma_num} — 🔒 Pendiente")

    # -------------------------------------------------------------------
    # PÁGINA: CERTIFICADOS
    # -------------------------------------------------------------------
    elif menu == "Certificados":
        st.title("🎓 Mis Certificados")
        certificados = obtener_certificados(user.id)

        if certificados:
            for cert in certificados:
                st.write(f"📜 Bioma {cert['bioma']} — Emitido: {cert['emitido_en'][:10]}")
        else:
            st.info("Aún no tienes certificados. Completa biomas para obtenerlos.")

    # -------------------------------------------------------------------
    # CERRAR SESIÓN
    # -------------------------------------------------------------------
    elif menu == "Cerrar Sesión":
        st.session_state.user = None
        st.rerun()
