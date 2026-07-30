import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import datetime

SUPABASE_URL = "https://pmshpvjtiauhbuexdjev.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2hwdmp0aWF1aGJ1ZXhkamV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ4ODI0MDgsImV4cCI6MjEwMDQ1ODQwOH0.gm_oWPgwjZe_6iN9sLsVjFOus7nN0eUBwkJ2bbbbVc4"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="EONIA - Portal del Creador", page_icon="🔷", layout="wide")

def iniciar_sesion(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response if response and response.user else None
    except:
        return None

def registrar_usuario(email, password, nombre, celular):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if not response or not response.user:
            return "email_existe"
        supabase.table("suscriptores").insert({"nombre": nombre, "email": email, "celular": celular}).execute()
        login = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return login if login and login.user else "login_fallo"
    except Exception as e:
        if any(x in str(e).lower() for x in ["already registered", "already exists", "duplicate"]):
            return "email_existe"
        return "error"

def obtener_fragmentos(user_id):
    r = supabase.table("fragmentos_obtenidos").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

def obtener_progreso(user_id):
    r = supabase.table("progreso_biomas").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

def obtener_certificados(user_id):
    r = supabase.table("certificados").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🔷 Portal del Creador EONIA")
    st.write("Inicia sesión o crea una cuenta para comenzar tu viaje.")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

    with tab1:
        st.subheader("🔑 Iniciar Sesión")
        e = st.text_input("Email", key="le")
        p = st.text_input("Contraseña", type="password", key="lp")
        if st.button("Entrar"):
            r = iniciar_sesion(e, p)
            if r and r.user:
                st.session_state.user = r.user
                st.success("¡Bienvenido de nuevo, Creador!")
                st.rerun()
            else:
                st.error("Email o contraseña incorrectos.")

    with tab2:
        st.subheader("🔷 Crear Cuenta")
        n = st.text_input("Nombre completo", key="rn")
        e = st.text_input("Email", key="re")
        c = st.text_input("Celular", key="rc")
        p = st.text_input("Contraseña", type="password", key="rp")
        if st.button("Registrarse"):
            if not n or not e or not c or not p:
                st.error("Todos los campos son obligatorios.")
            elif "@" not in e:
                st.error("Ingresa un email válido.")
            elif len(p) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                r = registrar_usuario(e, p, n, c)
                if r == "email_existe":
                    st.error("Este email ya está registrado.")
                elif r == "login_fallo":
                    st.warning("Cuenta creada. Inicia sesión manualmente.")
                elif r and r.user:
                    st.session_state.user = r.user
                    st.success(f"¡Bienvenido a EONIA, {n}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Error al crear la cuenta.")

else:
    user = st.session_state.user
    with st.sidebar:
        st.title(f"🔷 {user.email[:20]}...")
        menu = option_menu("Portal del Creador", ["Mi Perfil", "Mis Fragmentos", "Progreso", "Certificados", "Cerrar Sesión"],
                          icons=["person", "gem", "bar-chart", "award", "box-arrow-right"], default_index=0)

    if menu == "Mi Perfil":
        st.title("👤 Mi Perfil")
        st.write(f"**Email:** {user.email}")
        st.write(f"**ID:** {user.id}")
        p = obtener_progreso(user.id)
        st.metric("Biomas Completados", len([x for x in p if x["completado"]]))
        st.divider()
        st.link_button("🌐 Volver a eoniauniversity.com", "https://eoniauniversity.com")

    elif menu == "Mis Fragmentos":
        st.title("💎 Mis Fragmentos")
        f = obtener_fragmentos(user.id)
        if f:
            b = {}
            for x in f:
                b.setdefault(x["bioma"], []).append(x["fragmento"])
            for k, v in sorted(b.items()):
                with st.expander(f"🌿 Bioma {k} — {len(v)}/5 Fragmentos"):
                    for i in v:
                        st.write(f"✅ {i}")
                    if len(v) == 5:
                        st.success("✨ ¡Bioma completado!")
        else:
            st.info("Aún no tienes Fragmentos.")

    elif menu == "Progreso":
        st.title("📊 Progreso por Biomas")
        p = obtener_progreso(user.id)
        for i in range(1, 11):
            if any(x["bioma"] == i and x["completado"] for x in p):
                st.success(f"🌿 Bioma {i} — ✅ Completado")
            else:
                st.info(f"🌿 Bioma {i} — 🔒 Pendiente")

    elif menu == "Certificados":
        st.title("🎓 Mis Certificados")
        c = obtener_certificados(user.id)
        if c:
            for x in c:
                st.write(f"📜 Bioma {x['bioma']} — Emitido: {x['emitido_en'][:10]}")
        else:
            st.info("Aún no tienes certificados.")

    elif menu == "Cerrar Sesión":
        st.session_state.user = None
        st.rerun()
