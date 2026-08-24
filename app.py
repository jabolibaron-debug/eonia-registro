import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import datetime

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://pmshpvjtiauhbuexdjev.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2hwdmp0aWF1aGJ1ZXhkamV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ4ODI0MDgsImV4cCI6MjEwMDQ1ODQwOH0.gm_oWPgwjZe_6iN9sLsVjFOus7nN0eUBwkJ2bbbbVc4"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="EONIA - CRM del Creador", page_icon="🔷", layout="wide")

# -------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------------

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
    except:
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

def asignar_fragmento(user_id, bioma, fragmento):
    """Asigna un Fragmento a un Creador y actualiza el progreso."""
    # Insertar fragmento
    supabase.table("fragmentos_obtenidos").insert({
        "user_id": user_id, "bioma": bioma, "fragmento": fragmento
    }).execute()
    # Actualizar progreso
    frags = obtener_fragmentos(user_id)
    frags_bioma = [f for f in frags if f["bioma"] == bioma]
    porcentaje = min(100, len(frags_bioma) * 20)  # 5 fragmentos = 100%
    supabase.table("progreso_biomas").upsert({
        "user_id": user_id, "bioma": bioma, "porcentaje": porcentaje,
        "completado": porcentaje == 100
    }).execute()

def emitir_certificado(user_id, bioma, nombre_reliquia):
    """Emite un certificado (Reliquia) al completar un Bioma."""
    supabase.table("certificados").insert({
        "user_id": user_id, "bioma": bioma,
        "nombre_reliquia": nombre_reliquia,
        "emision": f"Bioma {bioma} completado"
    }).execute()

def calcular_progreso_global(user_id):
    """Calcula el progreso global del Creador."""
    progreso = obtener_progreso(user_id)
    if not progreso:
        return 0
    total = sum(p["porcentaje"] for p in progreso)
    return min(100, int(total / 10))  # 10 biomas, cada uno 100%

# -------------------------------------------------------------------
# PANTALLA DE LOGIN / REGISTRO
# -------------------------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🔷 Portal del Creador EONIA")
    st.write("Inicia sesión o crea una cuenta para ver tu progreso.")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

    with tab1:
        st.subheader("🔑 Iniciar Sesión")
        login_email = st.text_input("Email", key="le")
        login_pass = st.text_input("Contraseña", type="password", key="lp")
        if st.button("Entrar"):
            sesion = iniciar_sesion(login_email, login_pass)
            if sesion and sesion.user:
                st.session_state.user = sesion.user
                st.success("¡Bienvenido de nuevo, Creador!")
                st.rerun()
            else:
                st.error("Email o contraseña incorrectos.")

    with tab2:
        st.subheader("🔷 Crear Cuenta")
        rn = st.text_input("Nombre completo", key="rn")
        re = st.text_input("Email", key="re")
        rc = st.text_input("Celular", key="rc")
        rp = st.text_input("Contraseña", type="password", key="rp")
        if st.button("Registrarse"):
            if not rn or not re or not rc or not rp:
                st.error("Todos los campos son obligatorios.")
            elif "@" not in re:
                st.error("Ingresa un email válido.")
            elif len(rp) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                resultado = registrar_usuario(re, rp, rn, rc)
                if resultado == "email_existe":
                    st.error("Este email ya está registrado.")
                elif resultado == "login_fallo":
                    st.warning("Cuenta creada. Inicia sesión manualmente.")
                elif resultado and resultado.user:
                    st.session_state.user = resultado.user
                    st.success(f"¡Bienvenido a EONIA, {rn}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Error al crear la cuenta.")

else:
    user = st.session_state.user

    with st.sidebar:
        st.title(f"🔷 Creador")
        st.write(user.email)
        menu = option_menu(
            "Portal",
            ["Dashboard", "Mis Fragmentos", "Progreso por Biomas", "Certificados", "Cerrar Sesión"],
            icons=["speedometer2", "gem", "bar-chart", "award", "box-arrow-right"],
            default_index=0
        )

    # -------------------------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------------------------
    if menu == "Dashboard":
        st.title("📊 Dashboard del Creador")
        st.write("Tu progreso en el nuevo eón.")

        # Progreso global
        progreso_global = calcular_progreso_global(user.id)
        st.metric("Progreso Global", f"{progreso_global}%")

        st.progress(progreso_global / 100)

        st.divider()

        # Resumen por Bioma
        progreso = obtener_progreso(user.id)
        certificados = obtener_certificados(user.id)
        fragmentos = obtener_fragmentos(user.id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Biomas Completados", len([c for c in certificados]))
        with col2:
            st.metric("Fragmentos Obtenidos", len(fragmentos))
        with col3:
            st.metric("Certificados Emitidos", len(certificados))

        st.divider()

        # Progreso por Bioma en barras
        st.subheader("🌿 Progreso por Bioma")
        for bioma in range(1, 11):
            p = next((x for x in progreso if x["bioma"] == bioma), None)
            porcentaje = p["porcentaje"] if p else 0
            completado = p["completado"] if p else False

            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**Bioma {bioma}**")
            with col2:
                st.progress(porcentaje / 100)
            if completado:
                st.success(f"✅ Bioma {bioma} completado")

        st.divider()
        st.link_button("🌐 Volver a eoniauniversity.com", "https://eoniauniversity.com")

    # -------------------------------------------------------------------
    # MIS FRAGMENTOS
    # -------------------------------------------------------------------
    elif menu == "Mis Fragmentos":
        st.title("💎 Mis Fragmentos")
        fragmentos = obtener_fragmentos(user.id)
        if fragmentos:
            biomas = {}
            for f in fragmentos:
                biomas.setdefault(f["bioma"], []).append(f["fragmento"])
            for bioma, frags in sorted(biomas.items()):
                with st.expander(f"🌿 Bioma {bioma} — {len(frags)}/5 Fragmentos"):
                    for frag in frags:
                        st.write(f"✅ {frag}")
                    if len(frags) == 5:
                        st.success("✨ ¡Bioma completado!")
        else:
            st.info("Aún no tienes Fragmentos. Completa tu primer Bioma.")

    # -------------------------------------------------------------------
    # PROGRESO POR BIOMAS
    # -------------------------------------------------------------------
    elif menu == "Progreso por Biomas":
        st.title("📊 Progreso por Biomas")
        progreso = obtener_progreso(user.id)
        for bioma in range(1, 11):
            p = next((x for x in progreso if x["bioma"] == bioma), None)
            porcentaje = p["porcentaje"] if p else 0
            completado = p["completado"] if p else False

            st.write(f"**Bioma {bioma}**")
            st.progress(porcentaje / 100)
            if completado:
                st.success(f"✅ Completado — {porcentaje}%")
            else:
                st.info(f"🔒 {porcentaje}% completado")

    # -------------------------------------------------------------------
    # CERTIFICADOS (RELIQUIAS)
    # -------------------------------------------------------------------
    elif menu == "Certificados":
        st.title("🎓 Mis Certificados (Reliquias)")
        certificados = obtener_certificados(user.id)
        if certificados:
            for cert in certificados:
                with st.expander(f"📜 {cert['nombre_reliquia']} — Bioma {cert['bioma']}"):
                    st.write(f"**Emisión:** {cert['emision']}")
                    st.write(f"**Fecha:** {cert['emitido_en'][:10]}")
        else:
            st.info("Aún no tienes certificados. Completa biomas para obtenerlos.")

    # -------------------------------------------------------------------
    # CERRAR SESIÓN
    # -------------------------------------------------------------------
    elif menu == "Cerrar Sesión":
        st.session_state.user = None
        st.rerun()
