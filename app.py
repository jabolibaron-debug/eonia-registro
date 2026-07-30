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
        if response is not None and hasattr(response, 'user') and response.user is not None:
            return response
        return None
    except Exception as e:
        st.error(f"Error al iniciar sesión: {str(e)}")
        return None

def registrar_usuario(email, password, nombre, celular):
    try:
        # Crear usuario
        signup = supabase.auth.sign_up({"email": email, "password": password})
        
        if signup and hasattr(signup, 'session') and signup.session:
            # Si sign_up ya devuelve sesión, guardamos datos y retornamos
            supabase.table("suscriptores").insert({
                "nombre": nombre, "email": email, "celular": celular
            }).execute()
            return signup
        
        elif signup and hasattr(signup, 'user') and signup.user:
            # Si tiene user pero no session, guardamos datos e intentamos login
            supabase.table("suscriptores").insert({
                "nombre": nombre, "email": email, "celular": celular
            }).execute()
            
            login = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if login and hasattr(login, 'user') and login.user:
                return login
        
        return None
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

# -------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -------------------------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🔷 Portal del Creador EONIA")
    st.write("Inicia sesión o crea una cuenta para comenzar tu viaje.")
    
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
            elif len(reg_password) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                try:
                    st.write("Intentando registrar...")
                    
                    # Paso 1: Crear en Auth
                    signup = supabase.auth.sign_up({
                        "email": reg_email,
                        "password": reg_password
                    })
                    st.write(f"Respuesta sign_up: {signup}")
                    
                    if signup is None:
                        st.error("Error: No se recibió respuesta de Supabase.")
                    elif hasattr(signup, 'user') and signup.user is not None:
                        st.success("Usuario creado en Auth.")
                        
                        # Paso 2: Guardar en suscriptores
                        data = {"nombre": reg_nombre, "email": reg_email, "celular": reg_celular}
                        insert_result = supabase.table("suscriptores").insert(data).execute()
                        st.write(f"Insert resultado: {insert_result}")
                        
                        # Paso 3: Iniciar sesión
                        login = supabase.auth.sign_in_with_password({
                            "email": reg_email,
                            "password": reg_password
                        })
                        st.write(f"Login resultado: {login}")
                        
                        if login and hasattr(login, 'user') and login.user:
                            st.session_state.user = login.user
                            st.success(f"¡Bienvenido a EONIA, {reg_nombre}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.warning("Cuenta creada pero no se pudo iniciar sesión. Ve a Iniciar Sesión.")
                    else:
                        st.error(f"Error en sign_up: {signup}")
                        
                except Exception as e:
                    st.error(f"Excepción: {str(e)}")

else:
    user = st.session_state.user

    with st.sidebar:
        st.title(f"🔷 {user.email[:20]}...")
        menu = option_menu(
            menu_title="Portal del Creador",
            options=["Mi Perfil", "Mis Fragmentos", "Progreso", "Certificados", "Cerrar Sesión"],
            icons=["person", "gem", "bar-chart", "award", "box-arrow-right"],
            default_index=0
        )

    if menu == "Mi Perfil":
        st.title("👤 Mi Perfil")
        st.write(f"**Email:** {user.email}")
        st.write(f"**ID del Creador:** {user.id}")
        progreso = obtener_progreso(user.id)
        biomas_completados = [p["bioma"] for p in progreso if p["completado"]]
        st.metric("Biomas Completados", len(biomas_completados))
        st.divider()
        st.link_button("🌐 Volver a eoniauniversity.com", "https://eoniauniversity.com")

    elif menu == "Mis Fragmentos":
        st.title("💎 Mis Fragmentos")
        fragmentos = obtener_fragmentos(user.id)
        if fragmentos:
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

    elif menu == "Progreso":
        st.title("📊 Progreso por Biomas")
        progreso = obtener_progreso(user.id)
        for bioma_num in range(1, 11):
            completado = any(p["bioma"] == bioma_num and p["completado"] for p in progreso)
            if completado:
                st.success(f"🌿 Bioma {bioma_num} — ✅ Completado")
            else:
                st.info(f"🌿 Bioma {bioma_num} — 🔒 Pendiente")

    elif menu == "Certificados":
        st.title("🎓 Mis Certificados")
        certificados = obtener_certificados(user.id)
        if certificados:
            for cert in certificados:
                st.write(f"📜 Bioma {cert['bioma']} — Emitido: {cert['emitido_en'][:10]}")
        else:
            st.info("Aún no tienes certificados. Completa biomas para obtenerlos.")

    elif menu == "Cerrar Sesión":
        st.session_state.user = None
        st.rerun()
