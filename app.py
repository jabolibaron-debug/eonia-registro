import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import datetime

# CONFIGURACIÓN DE SUPABASE
SUPABASE_URL = "https://pmshpvjtiauhbuexdjev.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtc2hwdmp0aWF1aGJ1ZXhkamV2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ4ODI0MDgsImV4cCI6MjEwMDQ1ODQwOH0.gm_oWPgwjZe_6iN9sLsVjFOus7nN0eUBwkJ2bbbbVc4"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="EONIA - CRM del Creador", page_icon="🔷", layout="wide")

def obtener_supabase():
    return supabase

def crear_cliente() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def guardar_sesion(response):
    if response and response.user and response.session:
        st.session_state.user = response.user
        st.session_state.access_token = response.session.access_token
        st.session_state.refresh_token = response.session.refresh_token
        return True
    return False

def iniciar_sesion(email, password):
    try:
        supabase = crear_cliente()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response
    except Exception as e:
        print(f"Error login: {e}")
        return None

def registrar_usuario(email, password, nombre, celular):
    try:
        supabase = crear_cliente()
        response = supabase.auth.sign_up({"email": email, "password": password})
        if not response or not response.user:
            return "error"
        try:
            supabase.table("suscriptores").insert({"nombre": nombre, "email": email, "celular": celular}).execute()
        except Exception as e:
            print(f"Error creando suscriptor: {e}")
        login = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return login
    except Exception as e:
        print(f"Error registro: {e}")
        return "error"

def cerrar_sesion():
    try:
        supabase = obtener_supabase()
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.refresh_token = None

def obtener_fragmentos(user_id):
 
    r = supabase.table("fragmentos_obtenidos").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

def obtener_progreso(user_id):

    r = supabase.table("progreso_biomas").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

def obtener_creaciones(user_id):

    r = supabase.table("creaciones").select("*").eq("user_id", user_id).order("creado_en", desc=True).execute()
    return r.data if r.data else []

def obtener_certificados(user_id):

    r = supabase.table("certificados").select("*").eq("user_id", user_id).execute()
    return r.data if r.data else []

def emitir_certificado(user_id, bioma, nombre_reliquia, imagen_url=None):
    try:
        supabase = obtener_supabase()
        supabase.table("certificados").insert({
            "user_id": user_id,
            "bioma": bioma,
            "nombre_reliquia": nombre_reliquia,
            "emision": f"Bioma {bioma} completado",
            "imagen_url": imagen_url
        }).execute()
        return True
    except Exception as e:
        print(f"Error certificado: {e}")
        return False

def calcular_progreso_global(user_id):
    progreso = obtener_progreso(user_id)
    if not progreso:
        return 0
    total = sum(p.get("porcentaje", 0) for p in progreso)
    return min(100, int(total / 10))

if "user" not in st.session_state:
    st.session_state.user = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

if st.session_state.user is None:
    st.title("🔷 Portal del Creador EONIA")
    st.write("Inicia sesión o crea una cuenta para entrar al nuevo eón.")
    tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "🔷 Crear Cuenta"])

    with tab1:
        st.subheader("🔑 Iniciar Sesión")
        login_email = st.text_input("Email", key="login_email")
        login_pass = st.text_input("Contraseña", type="password", key="login_pass")
        if st.button("Entrar", use_container_width=True):
            if not login_email or not login_pass:
                st.warning("Ingresa tu email y contraseña.")
            else:
                sesion = iniciar_sesion(login_email, login_pass)
                if guardar_sesion(sesion):
                    st.success("¡Bienvenido de nuevo, Creador!")
                    st.rerun()
                else:
                    st.error("Email o contraseña incorrectos.")

    with tab2:
        st.subheader("🔷 Crear Cuenta")
        rn = st.text_input("Nombre completo", key="registro_nombre")
        re = st.text_input("Email", key="registro_email")
        rc = st.text_input("Celular", key="registro_celular")
        rp = st.text_input("Contraseña", type="password", key="registro_password")
        if st.button("Registrarse", use_container_width=True):
            if not rn or not re or not rc or not rp:
                st.error("Todos los campos son obligatorios.")
            elif "@" not in re:
                st.error("Ingresa un email válido.")
            elif len(rp) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                resultado = registrar_usuario(re, rp, rn, rc)
                if resultado == "error":
                    st.error("Error al crear la cuenta.")
                elif guardar_sesion(resultado):
                    st.success(f"¡Bienvenido a EONIA, {rn}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("Cuenta creada. Inicia sesión.")

else:
    user = st.session_state.user

    with st.sidebar:
        st.title("🔷 Creador")
        st.write(user.email)
        menu = option_menu(
            "Portal",
            ["Dashboard", "Mis Fragmentos", "Progreso por Biomas", "Certificados", "Mi Reflejo", "Mis Creaciones", "Cerrar Sesión"],
            icons=["speedometer2", "gem", "bar-chart", "award", "eye", "lightbulb", "box-arrow-right"],
            default_index=0
        )

    if menu == "Dashboard":
        st.title("📊 Dashboard del Creador")
        st.write("Tu progreso en el nuevo eón.")

        col_refresh, col_space = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄 Actualizar"):
                st.rerun()

        st.info(f"🆔 Tu ID de Creador: `{user.id}`")
        try:
            test = supabase.table("fragmentos_obtenidos").select("*").eq("user_id", str(user.id)).limit(5).execute()
            st.write(f"🔍 Debug - datos con str(user.id): {len(test.data)} filas")
        except Exception as e:
            st.write(f"🔍 Debug - Error: {e}")

        progreso = obtener_progreso(user.id)
        certificados = obtener_certificados(user.id)
        fragmentos = obtener_fragmentos(user.id)

        total_progreso = sum(p.get("porcentaje", 0) for p in progreso)
        progreso_global = min(100, int(total_progreso / 10))

        st.metric("Progreso Global", f"{progreso_global}%")
        st.progress(progreso_global / 100)
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            biomas_completados = len([p for p in progreso if p.get("completado") is True])
            st.metric("Biomas Completados", biomas_completados)
        with col2:
            st.metric("Fragmentos Obtenidos", len(fragmentos))
        with col3:
            st.metric("Certificados Emitidos", len(certificados))

        st.divider()
        st.subheader("🌿 Progreso por Bioma")
        progreso = obtener_progreso(user.id)
        for bioma in range(1, 11):
            p = next((x for x in progreso if x["bioma"] == bioma), None)
            porcentaje = p["porcentaje"] if p else 0
            completado = p["completado"] if p else False

            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.write(f"**Bioma {bioma}**")
            with col2:
                st.progress(porcentaje / 100)
            with col3:
                st.write(f"{porcentaje}%")
            if completado:
                st.success(f"✅ Bioma {bioma} completado")

        st.divider()
        st.link_button("🌐 Volver a EONIA", "https://eoniauniversity.com")

    elif menu == "Mis Fragmentos":
        st.title("💎 Mis Fragmentos")
        fragmentos = obtener_fragmentos(user.id)
        if fragmentos:
            biomas = {}
            for f in fragmentos:
                bioma = f.get("bioma")
                biomas.setdefault(bioma, []).append(f.get("fragmento"))
            for bioma, frags in sorted(biomas.items()):
                with st.expander(f"🌿 Bioma {bioma} — {len(frags)}/5 Fragmentos"):
                    for frag in frags:
                        st.write(f"✅ {frag}")
                    if len(frags) >= 5:
                        st.success("✨ ¡Bioma completado!")
        else:
            st.info("Aún no tienes Fragmentos.")

    elif menu == "Progreso por Biomas":
        st.title("📊 Progreso por Biomas")
        progreso = obtener_progreso(user.id)
        for bioma in range(1, 11):
            p = next((x for x in progreso if x["bioma"] == bioma), None)
            porcentaje = p["porcentaje"] if p else 0
            completado = p["completado"] if p else False

            st.write(f"**Bioma {bioma}**")
            st.progress(porcentaje / 100)
            st.write(f"{porcentaje}%")
            if completado:
                st.success(f"✅ Completado — {porcentaje}%")
            else:
                st.info(f"🔒 {porcentaje}% completado")

    elif menu == "Certificados":
        st.title("🏛️ Reliquias del Creador")
        progreso = obtener_progreso(user.id)
        certificados = obtener_certificados(user.id)

        biomas_completados = [p["bioma"] for p in progreso if p.get("completado") is True]
        biomas_con_reliquia = [c["bioma"] for c in certificados]

        if certificados:
            st.subheader("✨ Reliquias Forjadas")
            for cert in certificados:
                nombre = cert.get("nombre_reliquia", "Reliquia")
                bioma = cert.get("bioma")
                fecha = cert.get("emitido_en", "")
                imagen_url = cert.get("imagen_url")

                with st.container(border=True):
                    if imagen_url and imagen_url.startswith("http"):
                        st.image(imagen_url, width=300)
                    else:
                        st.markdown("## 🏆")

                    st.markdown(f"### {nombre}")
                    st.write(f"**Bioma {bioma}**")
                    if fecha:
                        st.write(f"*Forjada el {fecha[:10]}*")

        biomas_pendientes = [b for b in biomas_completados if b not in biomas_con_reliquia]

        if biomas_pendientes:
            st.subheader("🔮 Reliquias por Forjar")
            for bioma in biomas_pendientes:
                with st.container(border=True):
                    st.markdown(f"## 🌿 Bioma {bioma}")
                    st.write(f"**El Bioma {bioma} ha concluido.** Tu Reliquia te espera.")

                    nombre_reliquia = st.text_input(
                        "Nombre de la Reliquia",
                        value=f"Reliquia del Bioma {bioma}",
                        key=f"nombre_{bioma}"
                    )

                    archivo = st.file_uploader(
                        "Sube la imagen de tu Reliquia (opcional)",
                        type=["png", "jpg", "jpeg", "webp"],
                        key=f"archivo_{bioma}"
                    )

                    if st.button(f"⚒️ Forjar Reliquia del Bioma {bioma}", key=f"forjar_{bioma}"):
                        imagen_url = None

                        if archivo is not None:
                            try:
                                file_name = f"{user.id}_bioma_{bioma}.{archivo.name.split('.')[-1]}"
                                archivo_bytes = archivo.read()
                                supabase.storage.from_("reliquias").upload(file_name, archivo_bytes, file_options={"content-type": archivo.type})
                                imagen_url = supabase.storage.from_("reliquias").get_public_url(file_name)
                            except Exception as e:
                                st.warning(f"La imagen no se pudo subir: {e}")

                        if emitir_certificado(user.id, bioma, nombre_reliquia, imagen_url):
                            st.success(f"🏆 ¡Reliquia forjada: {nombre_reliquia}!")
                            st.rerun()
                        else:
                            st.error("No se pudo forjar la Reliquia.")

        if not biomas_completados and not certificados:
            st.info("Completa un Bioma para forjar tu primera Reliquia.")
    elif menu == "Mi Reflejo":
        st.title("🪞 Mi Reflejo")
        st.write("Tu despertar y tu evolución quedan grabados aquí.")

        # Obtener Reflejo
        r = supabase.table("reflejos").select("*").eq("user_id", user.id).execute()

        # Obtener certificados (Reliquias)
        certificados = obtener_certificados(user.id)

        biomas_con_reliquia = sorted([c["bioma"] for c in certificados])

        # Determinar nivel
        nivel = 1
        if all(b in biomas_con_reliquia for b in [1, 2, 3, 4]):
            nivel = 2
        if all(b in biomas_con_reliquia for b in [5, 6, 7]):
            nivel = 3
        if all(b in biomas_con_reliquia for b in [8, 9, 10]):
            nivel = 4

        # Nombres y descripciones
        reflejos_info = {
            1: ("El Despertar", "Descubrir quién puedes llegar a ser"),
            2: ("El Forjador", "Aprender a crear"),
            3: ("El Arquitecto", "Aprender a construir algo que trascienda"),
            4: ("El Legado", "Convertir tu creación en legado")
        }

        # Mostrar todos los Reflejos desbloqueados
        st.markdown("## 🌟 Reflejos Desbloqueados")

        for i in range(1, nivel + 1):
            nombre, descripcion = reflejos_info[i]
            st.markdown(f"### 🪞 Reflejo {['I', 'II', 'III', 'IV'][i-1]} — {nombre}")
            st.write(f"*{descripcion}*")

            if i == 1 and r.data:
                reflejo = r.data[0]
                if reflejo.get("imagen_url"):
                    st.image(reflejo["imagen_url"], width=300)

        st.divider()

        # Mostrar detalles del Reflejo base
        if r.data:
            reflejo = r.data[0]
            if reflejo.get("mentor_asignado"):
                st.write(f"**Mentor asignado:** {reflejo['mentor_asignado']}")
            if reflejo.get("indice_prosperidad"):
                st.write(f"**Índice de prosperidad:** {reflejo['indice_prosperidad']}")

        # Botón de subida
        st.divider()
        st.subheader("📤 Actualizar Reflejo")

        archivo = st.file_uploader(
            "Sube o actualiza tu imagen del Reflejo",
            type=["png", "jpg", "jpeg", "webp"],
            key="reflejo_upload"
        )

        if archivo is not None:
            try:
                file_name = f"reflejo_{user.id}.{archivo.name.split('.')[-1]}"
                archivo_bytes = archivo.read()
                supabase.storage.from_("reliquias").upload(
                    file_name,
                    archivo_bytes,
                    file_options={"content-type": archivo.type}
                )
                imagen_url = supabase.storage.from_("reliquias").get_public_url(file_name)

                supabase.table("reflejos").upsert({
                    "user_id": user.id,
                    "imagen_url": imagen_url,
                    "indice_prosperidad": None,
                    "mentor_asignado": None,
                    "fecha_despertar": datetime.datetime.now().isoformat(),
                    "nivel": nivel
                }).execute()

                st.success("✅ Tu Reflejo ha sido actualizado.")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # Progreso de Reliquias
        st.divider()
        st.subheader("🏛️ Reliquias para evolucionar tu Reflejo")
        st.write(f"**Reflejo I — El Despertar:** Siempre activo.")
        st.write(f"**Reflejo II — El Forjador:** Reliquias de Biomas 1–4 ({len([b for b in biomas_con_reliquia if b <= 4])}/4)")
        st.write(f"**Reflejo III — El Arquitecto:** Reliquias de Biomas 5–7 ({len([b for b in biomas_con_reliquia if 5 <= b <= 7])}/3)")
        st.write(f"**Reflejo IV — El Legado:** Reliquias de Biomas 8–10 ({len([b for b in biomas_con_reliquia if b >= 8])}/3)")

        # Mostrar progreso de Reliquias
        st.divider()
        st.subheader("🏛️ Reliquias para evolucionar tu Reflejo")

        st.write(f"**Reflejo I — El Despertar:** Siempre activo.")
        st.write(f"**Reflejo II — El Forjador:** Reliquias de Biomas 1–4 ({len([b for b in biomas_con_reliquia if b <= 4])}/4)")
        st.write(f"**Reflejo III — El Arquitecto:** Reliquias de Biomas 5–7 ({len([b for b in biomas_con_reliquia if 5 <= b <= 7])}/3)")
        st.write(f"**Reflejo IV — El Legado:** Reliquias de Biomas 8–10 ({len([b for b in biomas_con_reliquia if b >= 8])}/3)")

    elif menu == "Mis Creaciones":
        st.title("💡 Mis Creaciones")
        st.write("Las ideas que has transformado con el Reflejo Inverso.")

        creaciones = obtener_creaciones(user.id)

        if creaciones:
            for creacion in creaciones:
                with st.expander(f"💡 {creacion['idea_original'][:60]}..."):
                    st.write(f"**Yo Futuro:** {creacion.get('yo_futuro', '')}")
                    st.write(f"**Producto IA:** {creacion.get('producto_ia', '')}")
                    st.write(f"**Prompt Maestro:** {creacion.get('prompt_maestro', '')}")
                    st.write(f"**Primer Paso:** {creacion.get('primer_paso', '')}")
                    st.write(f"**Frase del Reflejo:** {creacion.get('frase_reflejo', '')}")
                    if creacion.get('fragmento_otorgado'):
                        st.success(f"🏆 Fragmento otorgado: {creacion['fragmento_otorgado']}")
                    st.write(f"**Fecha:** {creacion['creado_en'][:10]}")
        else:
            st.info("Aún no tienes creaciones. Usa el Reflejo Inverso para transformar tu primera idea.")

    elif menu == "Cerrar Sesión":
        cerrar_sesion()
        st.rerun()
