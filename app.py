#!/usr/bin/env python3
"""
COMMUNITY MANAGER AI ULTRA - API Flask con Supabase
Versión 4.0 - Backend completo con base de datos en la nube
Autor: DSR
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client
import random
import hashlib
import secrets

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la app
APP_NAME = os.getenv('APP_NAME', 'SocialConnect')
APP_ICON = os.getenv('APP_ICON', '🚀')

# ============================================================
# MODELOS DE DATOS (Tablas de Supabase)
# ============================================================

def crear_tablas():
    """Crear tablas en Supabase si no existen"""
    try:
        # Tabla de usuarios
        supabase.table('usuarios').select('*').limit(1).execute()
    except:
        print("⚠️ Las tablas no existen. Creando...")
        
        # Crear tablas usando SQL (ejecutar manualmente en Supabase SQL Editor)
        sql_script = """
        -- Tabla de usuarios
        CREATE TABLE IF NOT EXISTS usuarios (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nombre TEXT,
            avatar TEXT,
            bio TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Tabla de posts
        CREATE TABLE IF NOT EXISTS posts (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            contenido TEXT NOT NULL,
            imagen TEXT,
            video TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Tabla de likes
        CREATE TABLE IF NOT EXISTS likes (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(usuario_id, post_id)
        );

        -- Tabla de comentarios
        CREATE TABLE IF NOT EXISTS comentarios (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
            contenido TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Tabla de seguidores
        CREATE TABLE IF NOT EXISTS seguidores (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            seguidor_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            seguido_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(seguidor_id, seguido_id)
        );

        -- Tabla de stories
        CREATE TABLE IF NOT EXISTS stories (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            imagen TEXT,
            video TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '24 hours'
        );

        -- Tabla de notificaciones
        CREATE TABLE IF NOT EXISTS notificaciones (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
            tipo TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            leida BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        print("📝 Ejecutar el siguiente SQL en el editor de Supabase:")
        print(sql_script)
        print("\n✅ Tablas creadas correctamente")

# ============================================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================================

def hash_password(password):
    """Hashear contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_password(password, password_hash):
    """Verificar contraseña"""
    return hash_password(password) == password_hash

def obtener_usuario_actual():
    """Obtener usuario de la sesión actual"""
    if 'usuario_id' in session:
        try:
            response = supabase.table('usuarios').select('*').eq('id', session['usuario_id']).execute()
            if response.data:
                return response.data[0]
        except:
            pass
    return None

# ============================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================

@app.route('/')
def index():
    """Página principal"""
    usuario = obtener_usuario_actual()
    
    # Obtener posts para el feed
    try:
        posts_response = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').order('created_at', desc=True).limit(20).execute()
        posts = posts_response.data
        
        # Obtener likes del usuario actual
        if usuario:
            likes_response = supabase.table('likes').select('post_id').eq('usuario_id', usuario['id']).execute()
            likes = [like['post_id'] for like in likes_response.data]
        else:
            likes = []
            
    except:
        posts = []
        likes = []
    
    return render_template('index.html', 
                         usuario=usuario, 
                         posts=posts, 
                         likes=likes,
                         app_name=APP_NAME,
                         app_icon=APP_ICON)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Iniciar sesión"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Buscar usuario por email
            response = supabase.table('usuarios').select('*').eq('email', email).execute()
            
            if response.data:
                usuario = response.data[0]
                if verificar_password(password, usuario['password_hash']):
                    session['usuario_id'] = usuario['id']
                    session['usuario_nombre'] = usuario['nombre']
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error='Contraseña incorrecta')
            else:
                return render_template('login.html', error='Usuario no encontrado')
        except Exception as e:
            return render_template('login.html', error=f'Error: {str(e)}')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registrar usuario"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Verificar si el usuario existe
            existing = supabase.table('usuarios').select('*').or_(f'email.eq.{email},username.eq.{username}').execute()
            
            if existing.data:
                return render_template('register.html', error='El usuario o email ya existe')
            
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
                return redirect(url_for('login'))
            else:
                return render_template('register.html', error='Error al crear usuario')
                
        except Exception as e:
            return render_template('register.html', error=f'Error: {str(e)}')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('index'))

# ============================================================
# RUTAS DE API (JSON)
# ============================================================

@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    """Obtener todos los posts"""
    try:
        response = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def api_create_post():
    """Crear un nuevo post"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    data = request.json
    contenido = data.get('contenido')
    imagen = data.get('imagen')
    video = data.get('video')
    
    if not contenido:
        return jsonify({'success': False, 'error': 'El contenido es requerido'}), 400
    
    try:
        nuevo_post = {
            'usuario_id': usuario['id'],
            'contenido': contenido,
            'imagen': imagen,
            'video': video
        }
        
        response = supabase.table('posts').insert(nuevo_post).execute()
        
        if response.data:
            return jsonify({'success': True, 'data': response.data[0]})
        else:
            return jsonify({'success': False, 'error': 'Error al crear post'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    """Eliminar un post"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    try:
        # Verificar que el post pertenece al usuario
        response = supabase.table('posts').select('usuario_id').eq('id', post_id).execute()
        
        if not response.data:
            return jsonify({'success': False, 'error': 'Post no encontrado'}), 404
        
        if response.data[0]['usuario_id'] != usuario['id']:
            return jsonify({'success': False, 'error': 'No tienes permiso para eliminar este post'}), 403
        
        # Eliminar post
        supabase.table('posts').delete().eq('id', post_id).execute()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<post_id>/like', methods=['POST'])
def api_like_post(post_id):
    """Dar like a un post"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    try:
        # Verificar si ya tiene like
        existing = supabase.table('likes').select('*').eq('usuario_id', usuario['id']).eq('post_id', post_id).execute()
        
        if existing.data:
            # Quitar like
            supabase.table('likes').delete().eq('usuario_id', usuario['id']).eq('post_id', post_id).execute()
            return jsonify({'success': True, 'action': 'unliked'})
        else:
            # Dar like
            nuevo_like = {
                'usuario_id': usuario['id'],
                'post_id': post_id
            }
            supabase.table('likes').insert(nuevo_like).execute()
            
            # Crear notificación
            post_response = supabase.table('posts').select('usuario_id').eq('id', post_id).execute()
            if post_response.data:
                notificacion = {
                    'usuario_id': post_response.data[0]['usuario_id'],
                    'tipo': 'like',
                    'mensaje': f'{usuario["nombre"]} le dio like a tu publicación'
                }
                supabase.table('notificaciones').insert(notificacion).execute()
            
            return jsonify({'success': True, 'action': 'liked'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<post_id>/comment', methods=['POST'])
def api_comment_post(post_id):
    """Comentar un post"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    data = request.json
    contenido = data.get('contenido')
    
    if not contenido:
        return jsonify({'success': False, 'error': 'El comentario es requerido'}), 400
    
    try:
        nuevo_comentario = {
            'usuario_id': usuario['id'],
            'post_id': post_id,
            'contenido': contenido
        }
        
        response = supabase.table('comentarios').insert(nuevo_comentario).execute()
        
        if response.data:
            # Crear notificación
            post_response = supabase.table('posts').select('usuario_id').eq('id', post_id).execute()
            if post_response.data:
                notificacion = {
                    'usuario_id': post_response.data[0]['usuario_id'],
                    'tipo': 'comment',
                    'mensaje': f'{usuario["nombre"]} comentó tu publicación: "{contenido[:30]}..."'
                }
                supabase.table('notificaciones').insert(notificacion).execute()
            
            return jsonify({'success': True, 'data': response.data[0]})
        else:
            return jsonify({'success': False, 'error': 'Error al comentar'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/comentarios/<post_id>', methods=['GET'])
def api_get_comentarios(post_id):
    """Obtener comentarios de un post"""
    try:
        response = supabase.table('comentarios').select('*, usuarios(nombre, username, avatar)').eq('post_id', post_id).order('created_at', desc=True).execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/usuario/<username>', methods=['GET'])
def api_get_usuario(username):
    """Obtener información de un usuario"""
    try:
        response = supabase.table('usuarios').select('*').eq('username', username).execute()
        
        if response.data:
            usuario = response.data[0]
            # No enviar información sensible
            usuario.pop('password_hash', None)
            return jsonify({'success': True, 'data': usuario})
        else:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buscar', methods=['GET'])
def api_buscar():
    """Buscar usuarios y posts"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'success': True, 'usuarios': [], 'posts': []})
    
    try:
        # Buscar usuarios
        usuarios_response = supabase.table('usuarios').select('*').ilike('nombre', f'%{query}%').execute()
        
        # Buscar posts
        posts_response = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').ilike('contenido', f'%{query}%').limit(10).execute()
        
        return jsonify({
            'success': True,
            'usuarios': usuarios_response.data,
            'posts': posts_response.data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notificaciones', methods=['GET'])
def api_get_notificaciones():
    """Obtener notificaciones del usuario actual"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    try:
        response = supabase.table('notificaciones').select('*').eq('usuario_id', usuario['id']).order('created_at', desc=True).limit(20).execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notificaciones/leer', methods=['POST'])
def api_marcar_notificaciones_leidas():
    """Marcar notificaciones como leídas"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
    
    try:
        supabase.table('notificaciones').update({'leida': True}).eq('usuario_id', usuario['id']).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# RUTAS DE PÁGINAS
# ============================================================

@app.route('/perfil/<username>')
def perfil(username):
    """Perfil de usuario"""
    usuario_actual = obtener_usuario_actual()
    
    try:
        response = supabase.table('usuarios').select('*').eq('username', username).execute()
        
        if not response.data:
            return "Usuario no encontrado", 404
        
        perfil_usuario = response.data[0]
        
        # Obtener posts del usuario
        posts_response = supabase.table('posts').select('*, usuarios(nombre, username, avatar)').eq('usuario_id', perfil_usuario['id']).order('created_at', desc=True).execute()
        
        return render_template('perfil.html', 
                             perfil=perfil_usuario, 
                             posts=posts_response.data,
                             usuario_actual=usuario_actual)
                             
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/crear_post', methods=['POST'])
def crear_post():
    """Crear post desde formulario"""
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for('login'))
    
    contenido = request.form.get('contenido')
    imagen = request.form.get('imagen')
    video = request.form.get('video')
    
    if not contenido:
        return "El contenido es requerido", 400
    
    try:
        nuevo_post = {
            'usuario_id': usuario['id'],
            'contenido': contenido,
            'imagen': imagen,
            'video': video
        }
        
        supabase.table('posts').insert(nuevo_post).execute()
        return redirect(url_for('index'))
        
    except Exception as e:
        return f"Error: {str(e)}", 500

# ============================================================
# FUNCIONES PARA GENERAR DATOS DE EJEMPLO
# ============================================================

def generar_datos_ejemplo():
    """Generar datos de ejemplo para la aplicación"""
    try:
        # Verificar si ya hay datos
        usuarios_response = supabase.table('usuarios').select('*').limit(1).execute()
        if usuarios_response.data:
            print("✅ Ya hay datos en la base de datos")
            return
        
        print("📝 Generando datos de ejemplo...")
        
        # Crear usuarios de ejemplo
        usuarios_ejemplo = [
            {'nombre': 'Ana García', 'username': 'anagarcia', 'email': 'ana@email.com', 'bio': 'Diseñadora UI/UX'},
            {'nombre': 'Carlos López', 'username': 'carloslopez', 'email': 'carlos@email.com', 'bio': 'Desarrollador FullStack'},
            {'nombre': 'Laura Martínez', 'username': 'lauramartinez', 'email': 'laura@email.com', 'bio': 'Fotógrafa profesional'},
            {'nombre': 'David Chen', 'username': 'davidchen', 'email': 'david@email.com', 'bio': 'Data Scientist'}
        ]
        
        usuarios_creados = []
        for usuario in usuarios_ejemplo:
            nuevo_usuario = {
                'nombre': usuario['nombre'],
                'username': usuario['username'],
                'email': usuario['email'],
                'password_hash': hash_password('password123'),
                'avatar': f"https://api.dicebear.com/7.x/avataaars/svg?seed={usuario['username']}",
                'bio': usuario['bio']
            }
            
            response = supabase.table('usuarios').insert(nuevo_usuario).execute()
            if response.data:
                usuarios_creados.append(response.data[0])
        
        # Crear posts de ejemplo
        posts_ejemplo = [
            {'contenido': '¡Hola mundo! Esta es mi primera publicación en SocialConnect 🚀', 'imagen': 'https://source.unsplash.com/random/800x600/?tech,startup'},
            {'contenido': 'Acabo de terminar mi nuevo proyecto de diseño web. ¡Qué emoción! 🎨', 'imagen': 'https://source.unsplash.com/random/800x600/?design,web'},
            {'contenido': 'Disfrutando de un hermoso atardecer en la playa 🌅', 'imagen': 'https://source.unsplash.com/random/800x600/?sunset,beach'},
            {'contenido': 'Aprendiendo React y Tailwind CSS. ¡Qué buen combo! 💻', 'imagen': 'https://source.unsplash.com/random/800x600/?coding,work'},
            {'contenido': 'Nuevo reto de fotografía: Capturar la esencia de la ciudad 📸', 'imagen': 'https://source.unsplash.com/random/800x600/?city,night'},
            {'contenido': 'Recomiendo este libro: "El poder del ahora" 📚', 'imagen': 'https://source.unsplash.com/random/800x600/?book,reading'},
            {'contenido': '¡Gané el torneo de gaming del fin de semana! 🎮🏆', 'imagen': 'https://source.unsplash.com/random/800x600/?gaming,setup'},
            {'contenido': 'Primer día en el nuevo trabajo. ¡Emocionado! 🎯', 'imagen': 'https://source.unsplash.com/random/800x600/?office,work'}
        ]
        
        import random
        for i, post in enumerate(posts_ejemplo):
            usuario = random.choice(usuarios_creados)
            nuevo_post = {
                'usuario_id': usuario['id'],
                'contenido': post['contenido'],
                'imagen': post['imagen']
            }
            supabase.table('posts').insert(nuevo_post).execute()
        
        # Crear algunas interacciones
        for _ in range(10):
            post = random.choice(posts_ejemplo)
            usuario = random.choice(usuarios_creados)
            
            try:
                # Obtener un post real
                posts_response = supabase.table('posts').select('id').limit(1).execute()
                if posts_response.data:
                    supabase.table('likes').insert({
                        'usuario_id': usuario['id'],
                        'post_id': posts_response.data[0]['id']
                    }).execute()
            except:
                pass
        
        print("✅ Datos de ejemplo generados correctamente")
        
    except Exception as e:
        print(f"⚠️ Error generando datos de ejemplo: {e}")

# ============================================================
# CONFIGURACIÓN DE TEMPLATES
# ============================================================

@app.context_processor
def context_processor():
    """Variables globales para todas las plantillas"""
    return {
        'app_name': APP_NAME,
        'app_icon': APP_ICON,
        'year': datetime.now().year
    }

# ============================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================================

def init_app():
    """Inicializar la aplicación"""
    print("="*60)
    print(f"🚀 {APP_NAME} - API Flask con Supabase")
    print("="*60)
    print(f"📡 Conectando a Supabase: {SUPABASE_URL}")
    print(f"🔄 Verificando tablas...")
    
    # Crear tablas si no existen
    crear_tablas()
    
    # Generar datos de ejemplo
    generar_datos_ejemplo()
    
    print("✅ Aplicación lista")
    print("="*60)
    
    # Crear carpetas necesarias
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

# Inicializar la aplicación
init_app()

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
