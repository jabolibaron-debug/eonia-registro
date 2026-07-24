"""
RED SOCIAL CON STREAMLIT + SUPABASE
Versión para DSR - ¡Súper fácil!
"""

import streamlit as st
from supabase import create_client
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DE SUPABASE
# ============================================================
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="SocialConnect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto"
)

# Estilos personalizados (opcional)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .post-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .post-author {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }
    .post-author img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }
    .post-content {
        margin: 0.5rem 0;
    }
    .post-actions {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #eee;
    }
    .sidebar-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .user-avatar-large {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto;
        display: block;
        border: 3px solid #667eea;
    }
    .stat-box {
        text-align: center;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================

def hash_password(password):
    """Hashear contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    """Iniciar sesión"""
    try:
        response = supabase.table('usuarios').select('*').eq('email', email).execute()
        if response.data:
            usuario = response.data[0]
            if hash_password(password) == usuario['password_hash']:
                return usuario
    except:
        pass
    return None

def register_user(nombre, username, email, password):
    """Registrar usuario"""
    try:
        # Verificar si existe
        existing = supabase.table('usuarios').select('*').or_(f'email.eq.{email},username.eq.{username}').execute()
        if existing.data:
            return None, "El usuario o email ya existe"
        
        # Crear usuario
        nuevo_usuario = {
            'nombre': nombre,
            'username': username,
            'email': email,
            'password_hash': hash_password(password),
            'avatar': f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}",
            'bio': f'Hola, soy {nombre}'
        }
        
        response = supabase.table('usuarios').insert(nuevo_usuario).execute()
        if response.data:
            return response.data[0], None
        return None, "Error al crear usuario"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_user_posts(user_id):
    """Obtener posts de un usuario"""
    try:
        response = supabase.table('posts').select('*').eq('usuario_id', user_id).order('created_at', desc=True).execute()
        return response.data
    except:
        return []

def get_all_posts():
    """Obtener todos los posts"""
    try:
        response = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').order('created_at', desc=True).limit(20).execute()
        return response.data
    except:
        return []

def create_post(user_id, contenido, imagen=None):
    """Crear un post"""
    try:
        nuevo_post = {
            'usuario_id': user_id,
            'contenido': contenido,
            'imagen': imagen
        }
        response = supabase.table('posts').insert(nuevo_post).execute()
        return response.data[0] if response.data else None
    except:
        return None

def like_post(user_id, post_id):
    """Dar o quitar like"""
    try:
        existing = supabase.table('likes').select('*').eq('usuario_id', user_id).eq('post_id', post_id).execute()
        
        if existing.data:
            # Quitar like
            supabase.table('likes').delete().eq('usuario_id', user_id).eq('post_id', post_id).execute()
            return 'unliked'
        else:
            # Dar like
            supabase.table('likes').insert({
                'usuario_id': user_id,
                'post_id': post_id
            }).execute()
            return 'liked'
    except:
        return None

def get_likes_count(post_id):
    """Obtener cantidad de likes"""
    try:
        response = supabase.table('likes').select('*').eq('post_id', post_id).execute()
        return len(response.data)
    except:
        return 0

def user_liked_post(user_id, post_id):
    """Verificar si el usuario dio like"""
    try:
        response = supabase.table('likes').select('*').eq('usuario_id', user_id).eq('post_id', post_id).execute()
        return len(response.data) > 0
    except:
        return False

def add_comment(user_id, post_id, contenido):
    """Añadir comentario"""
    try:
        nuevo_comentario = {
            'usuario_id': user_id,
            'post_id': post_id,
            'contenido': contenido
        }
        response = supabase.table('comentarios').insert(nuevo_comentario).execute()
        return response.data[0] if response.data else None
    except:
        return None

def get_comments(post_id):
    """Obtener comentarios de un post"""
    try:
        response = supabase.table('comentarios').select('*, usuarios(nombre, username, avatar)').eq('post_id', post_id).order('created_at', desc=True).execute()
        return response.data
    except:
        return []

# ============================================================
# INICIALIZAR SESIÓN
# ============================================================

if 'usuario' not in st.session_state:
    st.session_state.usuario = None

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'

# ============================================================
# SIDEBAR - NAVEGACIÓN
# ============================================================

with st.sidebar:
    st.title("🚀 SocialConnect")
    
    if st.session_state.usuario:
        # Usuario logueado
        usuario = st.session_state.usuario
        
        st.image(usuario['avatar'], width=100)
        st.markdown(f"### {usuario['nombre']}")
        st.markdown(f"@{usuario['username']}")
        st.divider()
        
        # Menú de navegación
        opcion = st.radio(
            "Navegación",
            ["🏠 Inicio", "👤 Mi Perfil", "🔍 Explorar", "📊 Estadísticas"]
        )
        
        if opcion == "🏠 Inicio":
            st.session_state.pagina = 'inicio'
        elif opcion == "👤 Mi Perfil":
            st.session_state.pagina = 'perfil'
        elif opcion == "🔍 Explorar":
            st.session_state.pagina = 'explorar'
        elif opcion == "📊 Estadísticas":
            st.session_state.pagina = 'estadisticas'
        
        st.divider()
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.usuario = None
            st.rerun()
            
    else:
        # Usuario no logueado
        st.info("👋 Inicia sesión o regístrate")
        
        opcion_auth = st.radio(
            "Acceso",
            ["🔐 Iniciar Sesión", "📝 Registrarse"]
        )
        
        if opcion_auth == "🔐 Iniciar Sesión":
            st.session_state.pagina = 'login'
        else:
            st.session_state.pagina = 'register'

# ============================================================
# PÁGINA DE LOGIN
# ============================================================

if st.session_state.pagina == 'login':
    st.markdown('<div class="main-header"><h1>🔐 Iniciar Sesión</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("### Bienvenido de vuelta")
            
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Contraseña", type="password")
            
            if st.button("Ingresar", use_container_width=True):
                if email and password:
                    usuario = login_user(email, password)
                    if usuario:
                        st.session_state.usuario = usuario
                        st.session_state.pagina = 'inicio'
                        st.success("✅ ¡Bienvenido!")
                        st.rerun()
                    else:
                        st.error("❌ Email o contraseña incorrectos")
                else:
                    st.warning("⚠️ Completa todos los campos")
            
            st.divider()
            st.markdown("¿No tienes cuenta? **Regístrate** en el menú lateral")

# ============================================================
# PÁGINA DE REGISTRO
# ============================================================

elif st.session_state.pagina == 'register':
    st.markdown('<div class="main-header"><h1>📝 Registrarse</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("### Únete a la comunidad")
            
            nombre = st.text_input("👤 Nombre completo")
            username = st.text_input("🏷️ Usuario (sin espacios)")
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Contraseña", type="password")
            password_confirm = st.text_input("🔒 Confirmar contraseña", type="password")
            
            if st.button("Registrarse", use_container_width=True):
                if not all([nombre, username, email, password, password_confirm]):
                    st.warning("⚠️ Completa todos los campos")
                elif password != password_confirm:
                    st.warning("⚠️ Las contraseñas no coinciden")
                elif len(password) < 6:
                    st.warning("⚠️ La contraseña debe tener al menos 6 caracteres")
                elif ' ' in username:
                    st.warning("⚠️ El usuario no puede tener espacios")
                else:
                    usuario, error = register_user(nombre, username, email, password)
                    if usuario:
                        st.success("✅ ¡Registro exitoso! Ahora inicia sesión")
                        st.session_state.pagina = 'login'
                        st.rerun()
                    else:
                        st.error(f"❌ {error}")

# ============================================================
# PÁGINA DE INICIO - FEED
# ============================================================

elif st.session_state.pagina == 'inicio':
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión para ver el feed")
        st.stop()
    
    usuario = st.session_state.usuario
    
    # Cabecera
    st.markdown(f"""
    <div class="main-header">
        <h1>🏠 Bienvenido, {usuario['nombre']}!</h1>
        <p style="opacity: 0.8;">Comparte lo que estás pensando con la comunidad</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear post
    with st.container():
        st.markdown("### ✍️ Crear publicación")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            contenido = st.text_area("¿Qué estás pensando?", placeholder="Escribe algo interesante...", label_visibility="collapsed")
        with col2:
            st.write("")
            st.write("")
            publicar = st.button("📤 Publicar", use_container_width=True)
        
        if publicar and contenido:
            post = create_post(usuario['id'], contenido)
            if post:
                st.success("✅ ¡Publicación creada!")
                st.rerun()
            else:
                st.error("❌ Error al publicar")
    
    st.divider()
    
    # Mostrar posts
    st.markdown("### 📱 Feed de publicaciones")
    
    posts = get_all_posts()
    
    if not posts:
        st.info("📭 No hay publicaciones aún. ¡Sé el primero en publicar!")
    
    for post in posts:
        with st.container():
            # Información del autor
            col1, col2 = st.columns([1, 8])
            with col1:
                st.image(post['usuarios']['avatar'], width=50)
            with col2:
                st.markdown(f"""
                **{post['usuarios']['nombre']}**  
                <small>@{post['usuarios']['username']} • {post['created_at'][:16].replace('T', ' ')}</small>
                """, unsafe_allow_html=True)
            
            # Contenido
            st.markdown(f"<p style='font-size: 16px;'>{post['contenido']}</p>", unsafe_allow_html=True)
            
            if post.get('imagen'):
                st.image(post['imagen'], use_container_width=True)
            
            # Acciones
            likes_count = get_likes_count(post['id'])
            user_liked = user_liked_post(usuario['id'], post['id'])
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                like_text = "❤️" if user_liked else "🤍"
                if st.button(f"{like_text} {likes_count}", key=f"like_{post['id']}"):
                    result = like_post(usuario['id'], post['id'])
                    if result:
                        st.rerun()
            
            with col2:
                if st.button(f"💬 Comentar", key=f"comment_{post['id']}"):
                    # Mostrar campo de comentario
                    st.session_state[f'commenting_{post["id"]}'] = True
            
            with col3:
                if st.button("🔗 Compartir", key=f"share_{post['id']}"):
                    st.info("📋 Enlace copiado al portapapeles")
            
            # Comentarios
            if st.session_state.get(f'commenting_{post["id"]}'):
                comentario = st.text_input("Escribe un comentario...", key=f"comment_input_{post['id']}")
                if st.button("Enviar comentario", key=f"send_comment_{post['id']}"):
                    if comentario:
                        result = add_comment(usuario['id'], post['id'], comentario)
                        if result:
                            st.success("✅ Comentario añadido")
                            st.session_state[f'commenting_{post["id"]}'] = False
                            st.rerun()
            
            # Mostrar comentarios existentes
            comentarios = get_comments(post['id'])
            if comentarios:
                with st.expander(f"Ver {len(comentarios)} comentarios"):
                    for comentario in comentarios[:5]:
                        st.markdown(f"""
                        <div style="display: flex; gap: 10px; margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 8px;">
                            <img src="{comentario['usuarios']['avatar']}" style="width: 30px; height: 30px; border-radius: 50%;">
                            <div>
                                <strong>{comentario['usuarios']['nombre']}</strong>
                                <p style="margin: 0;">{comentario['contenido']}</p>
                                <small style="color: #666;">{comentario['created_at'][:16].replace('T', ' ')}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.divider()

# ============================================================
# PÁGINA DE PERFIL
# ============================================================

elif st.session_state.pagina == 'perfil':
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión para ver tu perfil")
        st.stop()
    
    usuario = st.session_state.usuario
    
    # Cabecera del perfil
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(usuario['avatar'], width=150)
    
    with col2:
        st.markdown(f"## {usuario['nombre']}")
        st.markdown(f"<p style='color: #666;'>@{usuario['username']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{usuario.get('bio', 'Sin biografía')}</p>", unsafe_allow_html=True)
        
        # Estadísticas
        mis_posts = get_user_posts(usuario['id'])
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"<div class='stat-box'><h3>{len(mis_posts)}</h3><p>Posts</p></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<div class='stat-box'><h3>0</h3><p>Seguidores</p></div>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<div class='stat-box'><h3>0</h3><p>Siguiendo</p></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Mis posts
    st.markdown("### 📝 Mis Publicaciones")
    
    if mis_posts:
        for post in mis_posts:
            with st.container():
                st.markdown(f"<p>{post['contenido']}</p>", unsafe_allow_html=True)
                if post.get('imagen'):
                    st.image(post['imagen'], use_container_width=True)
                st.caption(f"Publicado: {post['created_at'][:16].replace('T', ' ')}")
                st.divider()
    else:
        st.info("📭 No tienes publicaciones aún. ¡Comienza a compartir!")

# ============================================================
# PÁGINA DE EXPLORAR
# ============================================================

elif st.session_state.pagina == 'explorar':
    st.markdown('<div class="main-header"><h1>🔍 Explorar Comunidad</h1></div>', unsafe_allow_html=True)
    
    # Buscador
    busqueda = st.text_input("🔎 Buscar usuarios o publicaciones", placeholder="Escribe algo para buscar...")
    
    if busqueda:
        try:
            # Buscar usuarios
            usuarios = supabase.table('usuarios').select('*').ilike('nombre', f'%{busqueda}%').execute()
            
            if usuarios.data:
                st.markdown("### 👤 Usuarios encontrados")
                for user in usuarios.data:
                    col1, col2, col3 = st.columns([1, 4, 1])
                    with col1:
                        st.image(user['avatar'], width=50)
                    with col2:
                        st.markdown(f"**{user['nombre']}**  \n@{user['username']}")
                    with col3:
                        if st.button("Ver perfil", key=f"ver_{user['id']}"):
                            st.session_state.pagina = 'perfil_visitante'
                            st.session_state.perfil_visitante = user
                            st.rerun()
            
            # Buscar posts
            posts = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').ilike('contenido', f'%{busqueda}%').limit(10).execute()
            
            if posts.data:
                st.markdown("### 📝 Publicaciones encontradas")
                for post in posts.data:
                    with st.container():
                        st.markdown(f"""
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <img src="{post['usuarios']['avatar']}" style="width: 30px; height: 30px; border-radius: 50%;">
                            <strong>{post['usuarios']['nombre']}</strong>
                            <small>@{post['usuarios']['username']}</small>
                        </div>
                        <p>{post['contenido']}</p>
                        """, unsafe_allow_html=True)
                        if post.get('imagen'):
                            st.image(post['imagen'], use_container_width=True)
                        st.divider()
            
            if not usuarios.data and not posts.data:
                st.info("No se encontraron resultados")
                
        except Exception as e:
            st.error(f"Error en la búsqueda: {e}")
    else:
        # Mostrar posts recientes
        st.markdown("### 📰 Publicaciones recientes")
        posts = get_all_posts()
        if posts:
            for post in posts[:5]:
                with st.container():
                    st.markdown(f"""
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <img src="{post['usuarios']['avatar']}" style="width: 30px; height: 30px; border-radius: 50%;">
                        <strong>{post['usuarios']['nombre']}</strong>
                        <small>@{post['usuarios']['username']}</small>
                    </div>
                    <p>{post['contenido']}</p>
                    """, unsafe_allow_html=True)
                    st.divider()

# ============================================================
# PÁGINA DE ESTADÍSTICAS
# ============================================================

elif st.session_state.pagina == 'estadisticas':
    st.markdown('<div class="main-header"><h1>📊 Estadísticas</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.usuario:
        usuario = st.session_state.usuario
        mis_posts = get_user_posts(usuario['id'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Posts", len(mis_posts))
        
        with col2:
            # Total de likes en mis posts
            total_likes = 0
            for post in mis_posts:
                total_likes += get_likes_count(post['id'])
            st.metric("❤️ Likes Recibidos", total_likes)
        
        with col3:
            # Total de comentarios en mis posts
            total_comentarios = 0
            for post in mis_posts:
                total_comentarios += len(get_comments(post['id']))
            st.metric("💬 Comentarios", total_comentarios)
        
        with col4:
            st.metric("👥 Seguidores", 0)
        
        st.divider()
        
        # Gráfico de actividad (simplificado)
        st.markdown("### 📈 Actividad Reciente")
        
        if mis_posts:
            # Mostrar últimos 5 posts
            st.markdown("#### Últimas publicaciones:")
            for post in mis_posts[:5]:
                st.markdown(f"""
                <div style="padding: 10px; background: #f8f9fa; border-radius: 8px; margin: 5px 0;">
                    <p style="margin: 0;">{post['contenido'][:100]}...</p>
                    <small style="color: #666;">{post['created_at'][:16].replace('T', ' ')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay actividad para mostrar")

# ============================================================
# EJECUCIÓN
# ============================================================

# Si estás en modo desarrollo, ejecuta con:
# streamlit run app_streamlit.py
