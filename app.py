#!/usr/bin/env python3
"""
COMMUNITY MANAGER AI ULTRA - Generador de Redes Sociales Inteligente
Versión 3.0 - Optimizada para DSR
Con solo 3 preguntas crea una red social completa con backend y frontend
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import random
import webbrowser

class CommunityManagerAIUltra:
    def __init__(self):
        self.config = {}
        self.respuestas = {}
        self.templates = self.cargar_templates()
        self.assets_creados = 0
        
    def cargar_templates(self):
        """Cargar plantillas mejoradas"""
        return {
            'estilos': {
                'moderno': self.template_moderno(),
                'minimalista': self.template_minimalista(),
                'colorido': self.template_colorido(),
                'oscuro': self.template_oscuro()
            },
            'efectos': {
                'suaves': self.efectos_suaves(),
                'energeticos': self.efectos_energeticos(),
                'elegantes': self.efectos_elegantes()
            },
            'componentes': {
                'navbar': self.componente_navbar(),
                'sidebar': self.componente_sidebar(),
                'post': self.componente_post(),
                'carrusel': self.componente_carrusel()
            }
        }
    
    def template_moderno(self):
        return '''
/* Estilo Moderno Ultra */
:root {
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
}

body {
    background: var(--gradient-primary);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
}

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
}

.navbar {
    background: var(--glass-bg);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid var(--glass-border);
}
'''
    
    def template_minimalista(self):
        return '''
/* Estilo Minimalista Ultra */
:root {
    --color-bg: #ffffff;
    --color-surface: #f8f9fa;
    --color-border: #e0e0e0;
    --color-text: #1a1a1a;
}

body {
    background: var(--color-bg);
    color: var(--color-text);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}
'''
    
    def efectos_suaves(self):
        return '''
/* Efectos Suaves Ultra */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    33% { transform: translateY(-10px) rotate(2deg); }
    66% { transform: translateY(5px) rotate(-2deg); }
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes heartBeat {
    0% { transform: scale(1); }
    14% { transform: scale(1.3); }
    28% { transform: scale(1); }
    42% { transform: scale(1.3); }
    70% { transform: scale(1); }
}

@keyframes bounceIn {
    0% { opacity: 0; transform: scale(0.3); }
    50% { opacity: 1; transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.animate-fade-in {
    animation: fadeIn 0.6s ease-out;
}

.animate-slide-left {
    animation: slideInLeft 0.8s ease-out;
}

.animate-slide-right {
    animation: slideInRight 0.8s ease-out;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

.animate-spin {
    animation: spin 1s linear infinite;
}

.animate-typing {
    animation: typing 3.5s steps(40, end), blink .75s step-end infinite;
}

.animate-gradient {
    background-size: 200% 200%;
    animation: gradientFlow 3s ease infinite;
}

.animate-shimmer {
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,0.3) 50%,
        transparent 100%
    );
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
}
'''
    
    def componente_navbar(self):
        return '''
<!-- Navbar Ultra Moderno -->
<nav class="navbar">
    <div class="nav-container">
        <!-- Logo y marca -->
        <div class="nav-brand">
            <div class="logo-container">
                <i class="logo-icon"></i>
                <div class="logo-text">
                    <h1 class="logo-title">{{NOMBRE}}</h1>
                    <p class="logo-subtitle">{{ESLOGAN}}</p>
                </div>
            </div>
        </div>
        
        <!-- Búsqueda inteligente -->
        <div class="nav-search">
            <div class="search-container">
                <i class="search-icon"></i>
                <input type="text" class="search-input" placeholder="Buscar personas, posts, comunidades...">
                <div class="search-suggestions">
                    <!-- Sugerencias dinámicas -->
                </div>
            </div>
        </div>
        
        <!-- Navegación principal -->
        <div class="nav-main">
            <a href="#" class="nav-item active" data-tooltip="Inicio">
                <i class="nav-icon home"></i>
                <span class="nav-text">Inicio</span>
            </a>
            <a href="#" class="nav-item" data-tooltip="Explorar">
                <i class="nav-icon explore"></i>
                <span class="nav-text">Explorar</span>
            </a>
            <a href="#" class="nav-item" data-tooltip="Notificaciones">
                <i class="nav-icon notifications"></i>
                <span class="nav-badge">3</span>
            </a>
            <a href="#" class="nav-item" data-tooltip="Mensajes">
                <i class="nav-icon messages"></i>
                <span class="nav-badge">5</span>
            </a>
            <a href="#" class="nav-item" data-tooltip="Perfil">
                <i class="nav-icon profile"></i>
            </a>
        </div>
        
        <!-- Acciones rápidas -->
        <div class="nav-actions">
            <button class="btn-create" onclick="openCreateModal()">
                <i class="create-icon"></i>
                <span>Crear</span>
            </button>
            
            <!-- Menú usuario -->
            <div class="user-menu">
                <div class="user-avatar" onclick="toggleUserMenu()">
                    <img src="{{AVATAR}}" alt="Usuario">
                </div>
                <div class="user-dropdown">
                    <a href="#"><i class="dropdown-icon profile"></i> Mi Perfil</a>
                    <a href="#"><i class="dropdown-icon settings"></i> Configuración</a>
                    <a href="#"><i class="dropdown-icon help"></i> Ayuda</a>
                    <div class="dropdown-divider"></div>
                    <a href="#" class="logout"><i class="dropdown-icon logout"></i> Cerrar Sesión</a>
                </div>
            </div>
        </div>
    </div>
</nav>
'''
    
    def mostrar_banner(self):
        """Mostrar banner de inicio"""
        banner = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🚀 COMMUNITY MANAGER AI ULTRA - VERSIÓN 3.0              ║
║     🎯 Creado especialmente para DSR                         ║
║     ⚡ Con solo 3 preguntas, crea redes sociales completas   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("\n" + "="*70)
        print("🤖 INTELLIGENT SOCIAL NETWORK GENERATOR")
        print("="*70)
    
    def hacer_3_preguntas_mejoradas(self):
        """Preguntas mejoradas con más opciones"""
        self.mostrar_banner()
        print("\n📋 Vamos a personalizar tu red social en 3 simples pasos:\n")
        
        # PREGUNTA 1 MEJORADA
        print("1️⃣ ¿QUÉ TIPO DE COMUNIDAD VAS A CREAR?")
        print("   ┌─────────────────────────────────────────────────────────┐")
        print("   │ [1] 📱 Red Social General     (Facebook/Twitter style) │")
        print("   │ [2] 📸 Comunidad Fotografía   (Instagram/Pinterest)    │")
        print("   │ [3] 💬 Foro de Discusión      (Reddit/Quora style)     │")
        print("   │ [4] 💼 Red Profesional        (LinkedIn style)         │")
        print("   │ [5] 🎬 Plataforma de Contenido(YouTube/Twitch style)   │")
        print("   │ [6] 🎮 Comunidad Gaming        (Discord style)          │")
        print("   │ [7] 🎨 Comunidad Creativa      (Behance/Dribbble)       │")
        print("   │ [8] 🛒 Marketplace Social      (Depop/Etsy style)       │")
        print("   └─────────────────────────────────────────────────────────┘")
        
        while True:
            tipo = input("\n   🔹 Selecciona una opción (1-8): ").strip()
            tipos = {
                '1': {'id': 'general', 'nombre': 'Red Social General', 'emoji': '📱'},
                '2': {'id': 'fotografia', 'nombre': 'Comunidad de Fotografía', 'emoji': '📸'},
                '3': {'id': 'foro', 'nombre': 'Foro de Discusión', 'emoji': '💬'},
                '4': {'id': 'profesional', 'nombre': 'Red Profesional', 'emoji': '💼'},
                '5': {'id': 'contenido', 'nombre': 'Plataforma de Contenido', 'emoji': '🎬'},
                '6': {'id': 'gaming', 'nombre': 'Comunidad Gaming', 'emoji': '🎮'},
                '7': {'id': 'creativa', 'nombre': 'Comunidad Creativa', 'emoji': '🎨'},
                '8': {'id': 'marketplace', 'nombre': 'Marketplace Social', 'emoji': '🛒'}
            }
            
            if tipo in tipos:
                self.respuestas['tipo'] = tipos[tipo]
                print(f"   ✅ Seleccionado: {tipos[tipo]['emoji']} {tipos[tipo]['nombre']}")
                break
            else:
                print("   ❌ Opción inválida. Por favor, selecciona del 1 al 8.")
        
        # PREGUNTA 2 MEJORADA
        print("\n2️⃣ 🎨 ELIGE EL ESTILO VISUAL DE TU RED SOCIAL:")
        print("   ┌─────────────────────────────────────────────────────────┐")
        print("   │ [1] 🪐 Moderno Futurista     (Efectos de cristal)      │")
        print("   │ [2] 🧊 Minimalista Limpio    (Diseño simple y claro)   │")
        print("   │ [3] 🌈 Colorido Vibrante     (Gradientes y animaciones)│")
        print("   │ [4] 🌙 Oscuro Elegante       (Modo noche premium)      │")
        print("   │ [5] 🌿 Naturaleza Orgánico   (Colores tierra)          │")
        print("   │ [6] 🏙️ Urbano Industrial      (Estilo metálico)        │")
        print("   └─────────────────────────────────────────────────────────┘")
        
        while True:
            estilo = input("\n   🎨 Selecciona un estilo (1-6): ").strip()
            estilos = {
                '1': {'id': 'futurista', 'nombre': 'Moderno Futurista', 'emoji': '🪐'},
                '2': {'id': 'minimalista', 'nombre': 'Minimalista Limpio', 'emoji': '🧊'},
                '3': {'id': 'colorido', 'nombre': 'Colorido Vibrante', 'emoji': '🌈'},
                '4': {'id': 'oscuro', 'nombre': 'Oscuro Elegante', 'emoji': '🌙'},
                '5': {'id': 'organico', 'nombre': 'Naturaleza Orgánico', 'emoji': '🌿'},
                '6': {'id': 'urbano', 'nombre': 'Urbano Industrial', 'emoji': '🏙️'}
            }
            
            if estilo in estilos:
                self.respuestas['estilo'] = estilos[estilo]
                print(f"   ✅ Seleccionado: {estilos[estilo]['emoji']} {estilos[estilo]['nombre']}")
                break
            else:
                print("   ❌ Opción inválida. Por favor, selecciona del 1 al 6.")
        
        # PREGUNTA 3 MEJORADA
        print("\n3️⃣ ⚡ ¿QUÉ CARACTERÍSTICAS PRINCIPALES QUIERES?")
        print("   ┌─────────────────────────────────────────────────────────┐")
        print("   │ [1] ✨ Animaciones Avanzadas  (Efectos visuales)       │")
        print("   │ [2] 🎠 Carruseles Inteligentes(Galerías automáticas)   │")
        print("   │ [3] 💝 Sistema de Interacción (Likes, comentarios)     │")
        print("   │ [4] 💬 Chat en Tiempo Real    (Mensajería instantánea) │")
        print("   │ [5] 🤖 Recomendaciones AI     (Contenido personalizado)│")
        print("   │ [6] 🎮 Gamificación           (Logros y recompensas)   │")
        print("   │ [7] 📊 Analytics Avanzado     (Estadísticas detalladas)│")
        print("   │ [8] 🔐 Seguridad Premium      (Encriptación y privacidad)│")
        print("   └─────────────────────────────────────────────────────────┘")
        
        while True:
            caracteristica = input("\n   ⚡ Selecciona la característica principal (1-8): ").strip()
            caracteristicas = {
                '1': {'id': 'animaciones', 'nombre': 'Animaciones Avanzadas', 'emoji': '✨'},
                '2': {'id': 'carruseles', 'nombre': 'Carruseles Inteligentes', 'emoji': '🎠'},
                '3': {'id': 'interacciones', 'nombre': 'Sistema de Interacción', 'emoji': '💝'},
                '4': {'id': 'chat', 'nombre': 'Chat en Tiempo Real', 'emoji': '💬'},
                '5': {'id': 'ai', 'nombre': 'Recomendaciones AI', 'emoji': '🤖'},
                '6': {'id': 'gamificacion', 'nombre': 'Gamificación', 'emoji': '🎮'},
                '7': {'id': 'analytics', 'nombre': 'Analytics Avanzado', 'emoji': '📊'},
                '8': {'id': 'seguridad', 'nombre': 'Seguridad Premium', 'emoji': '🔐'}
            }
            
            if caracteristica in caracteristicas:
                self.respuestas['caracteristica'] = caracteristicas[caracteristica]
                print(f"   ✅ Seleccionado: {caracteristicas[caracteristica]['emoji']} {caracteristicas[caracteristica]['nombre']}")
                break
            else:
                print("   ❌ Opción inválida. Por favor, selecciona del 1 al 8.")
        
        print("\n" + "="*70)
        print("🎯 RESUMEN DE TU SELECCIÓN:")
        print("="*70)
        print(f"   📌 Tipo: {self.respuestas['tipo']['emoji']} {self.respuestas['tipo']['nombre']}")
        print(f"   🎨 Estilo: {self.respuestas['estilo']['emoji']} {self.respuestas['estilo']['nombre']}")
        print(f"   ⚡ Característica: {self.respuestas['caracteristica']['emoji']} {self.respuestas['caracteristica']['nombre']}")
        print("="*70)
        
        return True
    
    def generar_configuracion_mejorada(self):
        """Configuración mejorada con más opciones"""
        tipo = self.respuestas['tipo']['id']
        estilo = self.respuestas['estilo']['id']
        caracteristica = self.respuestas['caracteristica']['id']
        
        # Paleta de colores por estilo
        paletas_colores = {
            'futurista': ['#667eea', '#764ba2', '#00d2ff', '#3a7bd5'],
            'minimalista': ['#ffffff', '#f8f9fa', '#6c757d', '#212529'],
            'colorido': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'],
            'oscuro': ['#121212', '#1e1e1e', '#bb86fc', '#03dac6'],
            'organico': ['#556b2f', '#8fbc8f', '#deb887', '#f5deb3'],
            'urbano': ['#2c3e50', '#34495e', '#e74c3c', '#f39c12']
        }
        
        # Configuraciones por tipo
        config_base = {
            'general': {
                'nombre': 'ConnectHub',
                'eslogan': 'Conecta con el mundo que te rodea',
                'descripcion': 'La red social donde todas las conversaciones importan',
                'icono': '🌐',
                'caracteristicas': ['Perfiles personalizados', 'Grupos temáticos', 'Eventos locales', 'Marketplace integrado']
            },
            'fotografia': {
                'nombre': 'PixelWave',
                'eslogan': 'Captura y comparte tu perspectiva única',
                'descripcion': 'Comunidad de fotógrafos y amantes de la imagen',
                'icono': '📸',
                'caracteristicas': ['Galería infinita', 'Filtros profesionales', 'Retos fotográficos', 'Portfolios']
            },
            'foro': {
                'nombre': 'DebateSphere',
                'eslogan': 'Donde las ideas encuentran voz',
                'descripcion': 'Plataforma de discusión y debate inteligente',
                'icono': '💭',
                'caracteristicas': ['Subforos temáticos', 'Sistema de votación', 'Debates en vivo', 'Encuestas']
            },
            'profesional': {
                'nombre': 'CareerLink Pro',
                'eslogan': 'Tu red profesional, tu futuro',
                'descripcion': 'Conecta con profesionales y oportunidades',
                'icono': '💼',
                'caracteristicas': ['CV interactivo', 'Búsqueda de empleo', 'Networking', 'Cursos profesionales']
            },
            'gaming': {
                'nombre': 'GameVerse',
                'eslogan': 'Play together, grow together',
                'descripcion': 'El hogar de la comunidad gamer',
                'icono': '🎮',
                'caracteristicas': ['Servidores por juego', 'Streaming integrado', 'Torneos', 'Logros']
            },
            'creativa': {
                'nombre': 'CreativeFlow',
                'eslogan': 'Donde la creatividad fluye libre',
                'descripcion': 'Comunidad para artistas y creadores',
                'icono': '🎨',
                'caracteristicas': ['Portfolios', 'Colaboraciones', 'Retos creativos', 'Tienda de arte']
            },
            'marketplace': {
                'nombre': 'SocialMarket',
                'eslogan': 'Compra, vende, conecta',
                'descripcion': 'Marketplace social con comunidad integrada',
                'icono': '🛒',
                'caracteristicas': ['Tiendas personales', 'Sistema de reviews', 'Subastas', 'Entrega local']
            }
        }
        
        # Combinar configuración
        self.config = {
            **config_base.get(tipo, config_base['general']),
            'tipo': tipo,
            'estilo': estilo,
            'caracteristica_principal': caracteristica,
            'colores_primarios': paletas_colores.get(estilo, ['#667eea', '#764ba2', '#00d2ff']),
            'fecha_creacion': datetime.now().isoformat(),
            'version': '3.0.0',
            'autor': 'DSR',
            'features': {
                'animaciones_avanzadas': caracteristica in ['animaciones', 'gamificacion'],
                'carruseles_inteligentes': caracteristica in ['carruseles', 'ai'],
                'sistema_interaccion': caracteristica in ['interacciones', 'gamificacion'],
                'chat_tiempo_real': caracteristica == 'chat',
                'recomendaciones_ai': caracteristica == 'ai',
                'gamificacion': caracteristica == 'gamificacion',
                'analytics': caracteristica == 'analytics',
                'seguridad_premium': caracteristica == 'seguridad'
            },
            'apis': {
                'avatares': 'https://api.dicebear.com/7.x/avataaars/svg',
                'imagenes': 'https://source.unsplash.com/random',
                'iconos': 'https://cdn.jsdelivr.net/npm/remixicon/icons'
            },
            'configuracion_avanzada': {
                'pwa': True,
                'offline': True,
                'notificaciones_push': True,
                'indexacion_seo': True,
                'performance_score': 95
            }
        }
        
        # Guardar configuración
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración guardada: config.json")
        return self.config
    
    def generar_estructura_proyecto(self):
        """Crear estructura completa del proyecto"""
        estructura = {
            'assets': ['css', 'js', 'images', 'fonts', 'icons'],
            'components': ['navbar', 'sidebar', 'posts', 'stories', 'modal'],
            'pages': ['index.html', 'explore.html', 'profile.html', 'messages.html'],
            'data': ['posts.json', 'users.json', 'config.json', 'analytics.json']
        }
        
        print("\n📁 CREANDO ESTRUCTURA DEL PROYECTO...")
        print("="*50)
        
        # Crear carpetas
        for carpeta in estructura['assets']:
            Path(f'assets/{carpeta}').mkdir(parents=True, exist_ok=True)
            print(f"   📂 assets/{carpeta}/")
        
        for carpeta in estructura['components']:
            Path(f'components/{carpeta}').mkdir(parents=True, exist_ok=True)
            print(f"   📂 components/{carpeta}/")
        
        print("\n✅ Estructura de carpetas creada")
        return estructura
    
    def generar_archivo_principal(self):
        """Generar HTML principal con todas las características"""
        print("\n🛠️ GENERANDO ARCHIVOS PRINCIPALES...")
        print("="*50)
        
        # 1. HTML Principal
        html_content = self.crear_html_template()
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("   ✅ index.html")
        
        # 2. CSS Principal
        css_content = self.crear_css_completo()
        with open('assets/css/main.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("   ✅ assets/css/main.css")
        
        # 3. JavaScript Principal
        js_content = self.crear_javascript_completo()
        with open('assets/js/app.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("   ✅ assets/js/app.js")
        
        # 4. Componentes
        self.generar_componentes()
        
        # 5. Datos de ejemplo
        self.generar_datos_ejemplo()
        
        # 6. Documentación
        self.generar_documentacion()
        
        return True
    
    def crear_html_template(self):
        """Crear template HTML completo"""
        config = self.config
        colores = config['colores_primarios']
        
        return f'''<!DOCTYPE html>
<html lang="es" data-theme="{self.respuestas['estilo']['id']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['nombre']} - {config['eslogan']}</title>
    <meta name="description" content="{config['descripcion']}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{config['icono']}</text></svg>">
    
    <!-- Estilos -->
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- PWA -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="{colores[0]}">
    
    <!-- SEO -->
    <meta property="og:title" content="{config['nombre']}">
    <meta property="og:description" content="{config['descripcion']}">
    <meta property="og:image" content="https://source.unsplash.com/random/1200x630/?social,network">
    <meta property="og:url" content="https://{config['nombre'].lower()}.com">
    <meta name="twitter:card" content="summary_large_image">
</head>
<body>
    <!-- Preloader -->
    <div class="preloader">
        <div class="preloader-content">
            <div class="logo-spinner">
                <div class="spinner-circle"></div>
                <div class="logo-text">{config['icono']}</div>
            </div>
            <h2 class="loading-text">Cargando {config['nombre']}...</h2>
            <div class="loading-bar">
                <div class="loading-progress"></div>
            </div>
        </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar glass-effect" id="mainNavbar">
        <div class="container nav-container">
            <!-- Logo -->
            <div class="nav-brand">
                <a href="#" class="logo">
                    <span class="logo-icon">{config['icono']}</span>
                    <div class="logo-text">
                        <h1 class="logo-title">{config['nombre']}</h1>
                        <p class="logo-subtitle">{config['eslogan']}</p>
                    </div>
                </a>
            </div>

            <!-- Búsqueda -->
            <div class="nav-search">
                <div class="search-wrapper">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" class="search-input" placeholder="Buscar en {config['nombre']}...">
                    <div class="search-results" id="searchResults"></div>
                </div>
            </div>

            <!-- Navegación -->
            <div class="nav-menu">
                <a href="#" class="nav-link active" data-tooltip="Inicio">
                    <i class="fas fa-home"></i>
                    <span class="nav-text">Inicio</span>
                </a>
                <a href="#" class="nav-link" data-tooltip="Explorar">
                    <i class="fas fa-compass"></i>
                    <span class="nav-text">Explorar</span>
                </a>
                <a href="#" class="nav-link" data-tooltip="Notificaciones">
                    <i class="fas fa-bell"></i>
                    <span class="badge">3</span>
                </a>
                <a href="#" class="nav-link" data-tooltip="Mensajes">
                    <i class="fas fa-envelope"></i>
                    <span class="badge">5</span>
                </a>
                
                <!-- Perfil -->
                <div class="user-dropdown">
                    <button class="user-btn" id="userMenuBtn">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={config['nombre']}" 
                             alt="Usuario" class="user-avatar">
                    </button>
                    <div class="dropdown-menu" id="userDropdown">
                        <div class="dropdown-header">
                            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={config['nombre']}" 
                                 alt="Usuario" class="dropdown-avatar">
                            <div class="dropdown-user-info">
                                <h4>Usuario Demo</h4>
                                <p>@demo_user</p>
                            </div>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item"><i class="fas fa-user"></i> Mi Perfil</a>
                        <a href="#" class="dropdown-item"><i class="fas fa-cog"></i> Configuración</a>
                        <a href="#" class="dropdown-item"><i class="fas fa-moon"></i> Modo Oscuro</a>
                        <div class="dropdown-divider"></div>
                        <a href="#" class="dropdown-item logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</a>
                    </div>
                </div>

                <!-- Botón crear -->
                <button class="btn-create-post" onclick="openCreateModal()">
                    <i class="fas fa-plus"></i>
                    <span>Crear</span>
                </button>
            </div>
            
            <!-- Menú móvil -->
            <button class="menu-toggle" id="menuToggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <!-- Modal de creación -->
    <div class="modal" id="createModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Crear nueva publicación</h3>
                <button class="modal-close" onclick="closeCreateModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="create-post-form">
                    <div class="post-author">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Usuario" alt="Tú" class="author-avatar">
                        <div class="author-info">
                            <h4>Tú</h4>
                            <select class="post-audience">
                                <option value="public">🌍 Público</option>
                                <option value="friends">👥 Amigos</option>
                                <option value="private">🔒 Solo yo</option>
                            </select>
                        </div>
                    </div>
                    <textarea class="post-content-input" placeholder="¿Qué estás pensando?" rows="4"></textarea>
                    <div class="post-options">
                        <button class="post-option-btn" onclick="addPhoto()">
                            <i class="fas fa-image"></i> Foto/Video
                        </button>
                        <button class="post-option-btn" onclick="addTag()">
                            <i class="fas fa-user-tag"></i> Etiquetar
                        </button>
                        <button class="post-option-btn" onclick="addFeeling()">
                            <i class="fas fa-smile"></i> Sentimiento
                        </button>
                        <button class="post-option-btn" onclick="addLocation()">
                            <i class="fas fa-map-marker-alt"></i> Ubicación
                        </button>
                    </div>
                    <div class="post-preview" id="postPreview"></div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeCreateModal()">Cancelar</button>
                <button class="btn btn-primary" onclick="submitPost()">Publicar</button>
            </div>
        </div>
    </div>

    <!-- Contenido principal -->
    <main class="main-container">
        <div class="container grid-container">
            <!-- Sidebar izquierda -->
            <aside class="sidebar left-sidebar">
                <div class="user-card glass-effect animate-fade-in">
                    <div class="user-card-header">
                        <div class="cover-photo"></div>
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Usuario123" 
                             alt="Usuario" class="user-avatar-large">
                    </div>
                    <div class="user-card-body">
                        <h3 class="user-name">Usuario Demo</h3>
                        <p class="user-username">@demo_user</p>
                        <p class="user-bio">Apasionado de la tecnología y las redes sociales</p>
                        
                        <div class="user-stats">
                            <div class="stat">
                                <strong id="postCount">0</strong>
                                <span>Posts</span>
                            </div>
                            <div class="stat">
                                <strong id="followerCount">0</strong>
                                <span>Seguidores</span>
                            </div>
                            <div class="stat">
                                <strong id="followingCount">0</strong>
                                <span>Siguiendo</span>
                            </div>
                        </div>
                        
                        <button class="btn-edit-profile">Editar perfil</button>
                    </div>
                </div>

                <!-- Trending -->
                <div class="trending-card glass-effect">
                    <h4><i class="fas fa-fire"></i> Tendencias ahora</h4>
                    <div class="trending-list">
                        <div class="trending-item">
                            <span class="trend-rank">1</span>
                            <div class="trend-content">
                                <h5>#NuevaActualización</h5>
                                <p>1.2K posts</p>
                            </div>
                        </div>
                        <div class="trending-item">
                            <span class="trend-rank">2</span>
                            <div class="trend-content">
                                <h5>#TechNews</h5>
                                <p>890 posts</p>
                            </div>
                        </div>
                        <div class="trending-item">
                            <span class="trend-rank">3</span>
                            <div class="trend-content">
                                <h5>#ComunidadDSR</h5>
                                <p>567 posts</p>
                            </div>
                        </div>
                        <div class="trending-item">
                            <span class="trend-rank">4</span>
                            <div class="trend-content">
                                <h5>#DesarrolloWeb</h5>
                                <p>432 posts</p>
                            </div>
                        </div>
                    </div>
                    <a href="#" class="show-more">Mostrar más</a>
                </div>

                <!-- Eventos -->
                <div class="events-card glass-effect">
                    <h4><i class="fas fa-calendar-alt"></i> Próximos eventos</h4>
                    <div class="events-list">
                        <div class="event-item">
                            <div class="event-date">
                                <span class="event-day">HOY</span>
                                <span class="event-time">18:00</span>
                            </div>
                            <div class="event-details">
                                <h5>Live: Creando redes sociales</h5>
                                <p>Con DSR</p>
                            </div>
                        </div>
                        <div class="event-item">
                            <div class="event-date">
                                <span class="event-day">MAÑ</span>
                                <span class="event-time">10:00</span>
                            </div>
                            <div class="event-details">
                                <h5>Workshop Python</h5>
                                <p>Para principiantes</p>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

            <!-- Feed central -->
            <section class="feed-section">
                <!-- Crear post -->
                <div class="create-post-card glass-effect animate-slide-up">
                    <div class="create-post-header">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Tú" alt="Tú" class="create-post-avatar">
                        <input type="text" class="create-post-input" placeholder="¿Qué estás pensando?" 
                               onclick="openCreateModal()">
                    </div>
                    <div class="create-post-actions">
                        <button class="action-btn" onclick="openCreateModal('photo')">
                            <i class="fas fa-image text-primary"></i> <span>Foto/Video</span>
                        </button>
                        <button class="action-btn" onclick="openCreateModal('live')">
                            <i class="fas fa-video text-danger"></i> <span>En vivo</span>
                        </button>
                        <button class="action-btn" onclick="openCreateModal('event')">
                            <i class="fas fa-calendar text-success"></i> <span>Evento</span>
                        </button>
                        <button class="action-btn" onclick="openCreateModal('poll')">
                            <i class="fas fa-chart-bar text-warning"></i> <span>Encuesta</span>
                        </button>
                    </div>
                </div>

                <!-- Historias -->
                <div class="stories-section glass-effect">
                    <div class="stories-header">
                        <h4>Historias</h4>
                        <div class="stories-nav">
                            <button class="story-nav-btn prev" onclick="scrollStories(-1)">
                                <i class="fas fa-chevron-left"></i>
                            </button>
                            <button class="story-nav-btn next" onclick="scrollStories(1)">
                                <i class="fas fa-chevron-right"></i>
                            </button>
                        </div>
                    </div>
                    <div class="stories-container" id="storiesContainer">
                        <!-- Historias se cargan dinámicamente -->
                    </div>
                </div>

                <!-- Posts -->
                <div class="posts-container" id="postsContainer">
                    <!-- Posts se cargan dinámicamente -->
                </div>

                <!-- Cargar más -->
                <div class="load-more-container">
                    <button class="btn-load-more" onclick="loadMorePosts()">
                        <i class="fas fa-sync-alt"></i> Cargar más posts
                    </button>
                </div>
            </section>

            <!-- Sidebar derecha -->
            <aside class="sidebar right-sidebar">
                <!-- Sugerencias -->
                <div class="suggestions-card glass-effect">
                    <h4><i class="fas fa-user-plus"></i> Sugerencias para ti</h4>
                    <div class="suggestions-list">
                        <div class="suggestion-item">
                            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Usuario1" 
                                 alt="Usuario" class="suggestion-avatar">
                            <div class="suggestion-info">
                                <h5>Ana García</h5>
                                <p>Diseñadora UI/UX</p>
                                <p class="suggestion-mutual">3 amigos en común</p>
                            </div>
                            <button class="btn-follow" onclick="followUser(1)">Seguir</button>
                        </div>
                        <div class="suggestion-item">
                            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Usuario2" 
                                 alt="Usuario" class="suggestion-avatar">
                            <div class="suggestion-info">
                                <h5>Carlos López</h5>
                                <p>Desarrollador FullStack</p>
                                <p class="suggestion-mutual">5 amigos en común</p>
                            </div>
                            <button class="btn-follow" onclick="followUser(2)">Seguir</button>
                        </div>
                    </div>
                </div>

                <!-- Anuncios -->
                <div class="ads-card glass-effect">
                    <h4><i class="fas fa-ad"></i> Patrocinado</h4>
                    <div class="ad-content">
                        <img src="https://source.unsplash.com/random/300x200/?technology" 
                             alt="Anuncio" class="ad-image">
                        <div class="ad-text">
                            <h5>¡Mejora tus skills!</h5>
                            <p>Cursos de programación con 50% de descuento</p>
                            <button class="btn-ad">Ver oferta</button>
                        </div>
                    </div>
                </div>

                <!-- Footer rápido -->
                <div class="quick-links">
                    <a href="#">Términos</a> • 
                    <a href="#">Privacidad</a> • 
                    <a href="#">Cookies</a> • 
                    <a href="#">Ayuda</a>
                    <p class="copyright">© {datetime.now().year} {config['nombre']}. Todos los derechos reservados.</p>
                </div>
            </aside>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-logo">
                        <span class="logo-icon">{config['icono']}</span>
                        <h3>{config['nombre']}</h3>
                    </div>
                    <p class="footer-description">{config['descripcion']}</p>
                    <div class="footer-social">
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-facebook"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-linkedin"></i></a>
                        <a href="#"><i class="fab fa-github"></i></a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h4>Producto</h4>
                    <ul>
                        <li><a href="#">Características</a></li>
                        <li><a href="#">Precios</a></li>
                        <li><a href="#">API</a></li>
                        <li><a href="#">Documentación</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Compañía</h4>
                    <ul>
                        <li><a href="#">Sobre nosotros</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Carreras</a></li>
                        <li><a href="#">Contacto</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Legal</h4>
                    <ul>
                        <li><a href="#">Términos</a></li>
                        <li><a href="#">Privacidad</a></li>
                        <li><a href="#">Cookies</a></li>
                        <li><a href="#">GDPR</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {config['nombre']}. Generado con ❤️ por Community Manager AI Ultra para DSR.</p>
                <p>Versión {config['version']} • Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
        </div>
    </footer>

    <!-- Botones flotantes -->
    <div class="floating-buttons">
        <button class="fab btn-chat" onclick="openChat()" data-tooltip="Chat">
            <i class="fas fa-comment-dots"></i>
        </button>
        <button class="fab btn-theme" onclick="toggleTheme()" data-tooltip="Cambiar tema">
            <i class="fas fa-moon"></i>
        </button>
        <button class="fab btn-scroll-top" onclick="scrollToTop()" data-tooltip="Ir arriba">
            <i class="fas fa-arrow-up"></i>
        </button>
        <button class="fab btn-create-fab" onclick="openCreateModal()" data-tooltip="Crear post">
            <i class="fas fa-plus"></i>
        </button>
    </div>

    <!-- Toast notifications -->
    <div class="toast-container" id="toastContainer"></div>

    <!-- Scripts -->
    <script src="assets/js/app.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    
    <!-- Efecto de bienvenida -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Preloader
            setTimeout(() => {{
                document.querySelector('.preloader').style.opacity = '0';
                setTimeout(() => {{
                    document.querySelector('.preloader').style.display = 'none';
                }}, 500);
            }}, 1500);
            
            // Efecto de confeti
            setTimeout(createWelcomeConfetti, 1000);
            
            // Cargar datos iniciales
            loadInitialData();
            
            // Mostrar toast de bienvenida
            showToast('¡Bienvenido a {config['nombre']}! 🎉', 'success');
        }});
        
        function createWelcomeConfetti() {{
            // Tu código de confeti aquí
        }}
    </script>
</body>
</html>
'''
    
    def crear_css_completo(self):
        """Crear CSS completo con todas las características"""
        config = self.config
        colores = config['colores_primarios']
        
        return f'''
/* ====================================================
   {config['nombre'].upper()} - ESTILOS PRINCIPALES
   Generado por Community Manager AI Ultra v{config['version']}
   Estilo: {self.respuestas['estilo']['nombre']}
   Tipo: {self.respuestas['tipo']['nombre']}
   ==================================================== */

/* VARIABLES CSS DINÁMICAS */
:root {{
    /* Colores principales */
    --color-primary: {colores[0]};
    --color-secondary: {colores[1] if len(colores) > 1 else '#764ba2'};
    --color-accent: {colores[2] if len(colores) > 2 else '#00d2ff'};
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    --color-info: #3b82f6;
    
    /* Sistema de colores */
    --color-bg: #ffffff;
    --color-surface: #f8f9fa;
    --color-border: #e5e7eb;
    --color-text: #1f2937;
    --color-text-secondary: #6b7280;
    
    /* Tamaños y espacios */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;
    
    /* Sombras */
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1);
    
    /* Transiciones */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Tipografía */
    --font-primary: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'SF Mono', Monaco, Consolas, monospace;
}}

/* Modo oscuro */
[data-theme="dark"] {{
    --color-bg: #121212;
    --color-surface: #1e1e1e;
    --color-border: #333333;
    --color-text: #ffffff;
    --color-text-secondary: #a0a0a0;
}}

/* RESET Y BASE */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: var(--font-primary);
    background: var(--color-bg);
    color: var(--color-text);
    line-height: 1.6;
    overflow-x: hidden;
    min-height: 100vh;
    position: relative;
}}

/* TIPOGRAFÍA */
h1, h2, h3, h4, h5, h6 {{
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}}

h1 {{ font-size: 2.5rem; }}
h2 {{ font-size: 2rem; }}
h3 {{ font-size: 1.5rem; }}
h4 {{ font-size: 1.25rem; }}
h5 {{ font-size: 1rem; }}
h6 {{ font-size: 0.875rem; }}

p {{
    margin-bottom: 1rem;
}}

a {{
    color: var(--color-primary);
    text-decoration: none;
    transition: color var(--transition-fast);
}}

a:hover {{
    color: var(--color-secondary);
}}

/* UTILIDADES */
.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 1rem;
}}

.text-center {{ text-align: center; }}
.text-right {{ text-align: right; }}
.text-left {{ text-align: left; }}

/* GRID SYSTEM */
.grid-container {{
    display: grid;
    grid-template-columns: 280px 1fr 280px;
    gap: 2rem;
    padding: 2rem 0;
}}

@media (max-width: 1200px) {{
    .grid-container {{
        grid-template-columns: 240px 1fr 240px;
    }}
}}

@media (max-width: 992px) {{
    .grid-container {{
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }}
}}

/* COMPONENTES REUTILIZABLES */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-weight: 500;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all var(--transition-fast);
    gap: 0.5rem;
}}

.btn-primary {{
    background: var(--color-primary);
    color: white;
}}

.btn-primary:hover {{
    background: var(--color-secondary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}}

.btn-secondary {{
    background: var(--color-surface);
    color: var(--color-text);
    border: 1px solid var(--color-border);
}}

.btn-secondary:hover {{
    background: var(--color-bg);
    border-color: var(--color-primary);
}}

.btn-sm {{ padding: 0.5rem 1rem; font-size: 0.75rem; }}
.btn-lg {{ padding: 1rem 2rem; font-size: 1rem; }}

/* CARD */
.card {{
    background: var(--color-surface);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}}

.card:hover {{
    box-shadow: var(--shadow-md);
    transform: translateY(-4px);
}}

/* PRELOADER */
.preloader {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--color-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: opacity var(--transition-slow);
}}

.preloader-content {{
    text-align: center;
    max-width: 400px;
}}

.logo-spinner {{
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto 2rem;
}}

.spinner-circle {{
    position: absolute;
    width: 100%;
    height: 100%;
    border: 4px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}}

.logo-text {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 2.5rem;
}}

.loading-text {{
    margin-bottom: 1rem;
    font-weight: 500;
}}

.loading-bar {{
    width: 100%;
    height: 4px;
    background: var(--color-border);
    border-radius: var(--radius-full);
    overflow: hidden;
}}

.loading-progress {{
    width: 0%;
    height: 100%;
    background: var(--color-primary);
    animation: loading 1.5s ease-in-out infinite;
}}

@keyframes loading {{
    0% {{ width: 0%; }}
    50% {{ width: 100%; }}
    100% {{ width: 0%; }}
}}

/* NAVBAR */
.navbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    background: var(--color-bg);
    border-bottom: 1px solid var(--color-border);
    padding: 1rem 0;
    backdrop-filter: blur(10px);
    background: rgba(var(--color-bg-rgb), 0.8);
}}

.nav-container {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
}}

.nav-brand .logo {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
}}

.logo-icon {{
    font-size: 2rem;
    line-height: 1;
}}

.logo-text {{
    display: flex;
    flex-direction: column;
}}

.logo-title {{
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0;
    line-height: 1.2;
}}

.logo-subtitle {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
}}

.nav-search {{
    flex: 1;
    max-width: 600px;
}}

.search-wrapper {{
    position: relative;
}}

.search-icon {{
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-secondary);
}}

.search-input {{
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text);
    transition: all var(--transition-fast);
}}

.search-input:focus {{
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.1);
}}

.search-results {{
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-top: 0.5rem;
    box-shadow: var(--shadow-lg);
    display: none;
    z-index: 100;
}}

.search-input:focus + .search-results {{
    display: block;
}}

.nav-menu {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.nav-link {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5rem;
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color var(--transition-fast);
    min-width: 56px;
}}

.nav-link.active {{
    color: var(--color-primary);
}}

.nav-link i {{
    font-size: 1.25rem;
    margin-bottom: 0.25rem;
}}

.nav-text {{
    font-size: 0.75rem;
}}

.badge {{
    position: absolute;
    top: 0;
    right: 0;
    background: var(--color-danger);
    color: white;
    font-size: 0.625rem;
    font-weight: 600;
    min-width: 18px;
    height: 18px;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 0.25rem;
}}

.user-dropdown {{
    position: relative;
}}

.user-btn {{
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}}

.user-avatar {{
    width: 40px;
    height: 40px;
    border-radius: var(--radius-full);
    border: 2px solid var(--color-primary);
    object-fit: cover;
}}

.dropdown-menu {{
    position: absolute;
    top: 100%;
    right: 0;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    min-width: 200px;
    margin-top: 0.5rem;
    display: none;
    z-index: 100;
}}

.user-dropdown:hover .dropdown-menu {{
    display: block;
}}

.dropdown-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
}}

.dropdown-avatar {{
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
    object-fit: cover;
}}

.dropdown-user-info h4 {{
    font-size: 0.875rem;
    margin: 0;
    line-height: 1.2;
}}

.dropdown-user-info p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
}}

.dropdown-divider {{
    height: 1px;
    background: var(--color-border);
    margin: 0.5rem 0;
}}

.dropdown-item {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: var(--color-text);
    text-decoration: none;
    transition: background var(--transition-fast);
    font-size: 0.875rem;
}}

.dropdown-item:hover {{
    background: var(--color-surface);
}}

.dropdown-item i {{
    width: 20px;
    text-align: center;
    color: var(--color-text-secondary);
}}

.dropdown-item.logout {{
    color: var(--color-danger);
}}

.dropdown-item.logout:hover {{
    background: rgba(var(--color-danger-rgb), 0.1);
}}

.btn-create-post {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-full);
    font-family: var(--font-primary);
    font-weight: 500;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.btn-create-post:hover {{
    background: var(--color-secondary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}}

.menu-toggle {{
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}}

.menu-toggle span {{
    display: block;
    width: 24px;
    height: 2px;
    background: var(--color-text);
    transition: transform var(--transition-fast);
}}

/* MODAL */
.modal {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    opacity: 0;
    visibility: hidden;
    transition: all var(--transition-normal);
}}

.modal.show {{
    opacity: 1;
    visibility: visible;
}}

.modal-content {{
    background: var(--color-bg);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: var(--shadow-xl);
    animation: modalSlideIn 0.3s ease-out;
}}

@keyframes modalSlideIn {{
    from {{
        opacity: 0;
        transform: translateY(-20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.modal-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-bottom: 1px solid var(--color-border);
}}

.modal-header h3 {{
    margin: 0;
    font-size: 1.25rem;
}}

.modal-close {{
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--color-text-secondary);
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-full);
    transition: background var(--transition-fast);
}}

.modal-close:hover {{
    background: var(--color-surface);
}}

.modal-body {{
    padding: 1.5rem;
}}

.modal-footer {{
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid var(--color-border);
}}

/* CREATE POST FORM */
.create-post-form {{}}

.post-author {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.author-avatar {{
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
    object-fit: cover;
}}

.author-info {{
    flex: 1;
}}

.author-info h4 {{
    margin: 0 0 0.25rem;
    font-size: 1rem;
}}

.post-audience {{
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 0.25rem 0.5rem;
    font-family: var(--font-primary);
    font-size: 0.75rem;
    color: var(--color-text);
}}

.post-content-input {{
    width: 100%;
    min-height: 100px;
    padding: 1rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-size: 1rem;
    color: var(--color-text);
    resize: vertical;
    transition: border-color var(--transition-fast);
}}

.post-content-input:focus {{
    outline: none;
    border-color: var(--color-primary);
}}

.post-options {{
    display: flex;
    gap: 0.5rem;
    margin: 1rem 0;
}}

.post-option-btn {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.post-option-btn:hover {{
    background: var(--color-bg);
    border-color: var(--color-primary);
}}

.post-preview {{
    margin-top: 1rem;
    padding: 1rem;
    background: var(--color-surface);
    border-radius: var(--radius-md);
    border: 1px dashed var(--color-border);
    display: none;
}}

.post-preview.has-content {{
    display: block;
}}

/* MAIN CONTENT */
.main-container {{
    min-height: calc(100vh - 140px);
}}

/* SIDEBAR */
.sidebar {{
    position: sticky;
    top: 80px;
    height: calc(100vh - 100px);
    overflow-y: auto;
}}

.sidebar::-webkit-scrollbar {{
    width: 4px;
}}

.sidebar::-webkit-scrollbar-track {{
    background: transparent;
}}

.sidebar::-webkit-scrollbar-thumb {{
    background: var(--color-border);
    border-radius: var(--radius-full);
}}

.user-card {{
    margin-bottom: 1.5rem;
}}

.user-card-header {{
    position: relative;
    height: 80px;
    margin-bottom: 40px;
}}

.cover-photo {{
    height: 100%;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}}

.user-avatar-large {{
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 80px;
    border-radius: var(--radius-full);
    border: 4px solid var(--color-bg);
    object-fit: cover;
}}

.user-card-body {{
    text-align: center;
    padding: 0 1rem 1rem;
}}

.user-name {{
    font-size: 1.25rem;
    margin: 0.5rem 0 0.25rem;
}}

.user-username {{
    color: var(--color-text-secondary);
    font-size: 0.875rem;
    margin: 0 0 0.5rem;
}}

.user-bio {{
    font-size: 0.875rem;
    color: var(--color-text);
    margin: 0 0 1rem;
    line-height: 1.5;
}}

.user-stats {{
    display: flex;
    justify-content: space-around;
    margin: 1rem 0;
    padding: 1rem 0;
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
}}

.stat {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.stat strong {{
    font-size: 1.25rem;
    color: var(--color-text);
    line-height: 1;
}}

.stat span {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin-top: 0.25rem;
}}

.btn-edit-profile {{
    width: 100%;
    margin-top: 1rem;
}}

.trending-card, .events-card, .suggestions-card, .ads-card {{
    margin-bottom: 1.5rem;
}}

.trending-card h4, .events-card h4, .suggestions-card h4, .ads-card h4 {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}}

.trending-list, .events-list, .suggestions-list {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}}

.trending-item {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem;
    border-radius: var(--radius-md);
    transition: background var(--transition-fast);
}}

.trending-item:hover {{
    background: var(--color-surface);
}}

.trend-rank {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: var(--color-primary);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: var(--radius-full);
}}

.trend-content h5 {{
    font-size: 0.875rem;
    margin: 0;
    line-height: 1.2;
}}

.trend-content p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
}}

.show-more {{
    display: block;
    text-align: center;
    font-size: 0.875rem;
    color: var(--color-primary);
    padding: 0.5rem;
    margin-top: 0.5rem;
    border-radius: var(--radius-md);
    transition: background var(--transition-fast);
}}

.show-more:hover {{
    background: var(--color-surface);
}}

.event-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem;
    border-radius: var(--radius-md);
    transition: background var(--transition-fast);
}}

.event-item:hover {{
    background: var(--color-surface);
}}

.event-date {{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
}}

.event-day {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--color-text);
}}

.event-time {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}}

.event-details h5 {{
    font-size: 0.875rem;
    margin: 0 0 0.25rem;
    line-height: 1.2;
}}

.event-details p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
}}

/* FEED SECTION */
.feed-section {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.create-post-card {{
    padding: 1.5rem;
}}

.create-post-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}}

.create-post-avatar {{
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
    object-fit: cover;
}}

.create-post-input {{
    flex: 1;
    padding: 0.75rem 1rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.create-post-input:hover {{
    background: var(--color-bg);
    border-color: var(--color-primary);
}}

.create-post-actions {{
    display: flex;
    gap: 0.5rem;
}}

.action-btn {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.action-btn:hover {{
    background: var(--color-bg);
    border-color: var(--color-primary);
}}

.action-btn i.text-primary {{ color: var(--color-primary); }}
.action-btn i.text-danger {{ color: var(--color-danger); }}
.action-btn i.text-success {{ color: var(--color-success); }}
.action-btn i.text-warning {{ color: var(--color-warning); }}

.stories-section {{
    padding: 1.5rem;
}}

.stories-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}}

.stories-header h4 {{
    font-size: 1.125rem;
    margin: 0;
}}

.stories-nav {{
    display: flex;
    gap: 0.5rem;
}}

.story-nav-btn {{
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    color: var(--color-text);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.story-nav-btn:hover {{
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}}

.stories-container {{
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding: 0.5rem 0;
    scrollbar-width: none;
}}

.stories-container::-webkit-scrollbar {{
    display: none;
}}

.story-item {{
    flex: 0 0 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}}

.story-avatar {{
    width: 80px;
    height: 80px;
    border-radius: var(--radius-full);
    border: 3px solid var(--color-primary);
    padding: 3px;
    background: var(--color-bg);
    object-fit: cover;
}}

.story-username {{
    font-size: 0.75rem;
    color: var(--color-text);
    text-align: center;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.posts-container {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.post-card {{
    padding: 1.5rem;
}}

.post-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}}

.post-author {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.post-avatar {{
    width: 40px;
    height: 40px;
    border-radius: var(--radius-full);
    object-fit: cover;
}}

.post-author-info h5 {{
    font-size: 0.875rem;
    margin: 0 0 0.125rem;
    line-height: 1.2;
}}

.post-author-info p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
}}

.post-time {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}}

.post-content {{
    margin-bottom: 1rem;
}}

.post-text {{
    font-size: 0.875rem;
    line-height: 1.6;
    margin-bottom: 1rem;
}}

.post-image {{
    width: 100%;
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
    max-height: 500px;
    object-fit: cover;
    cursor: pointer;
}}

.post-actions {{
    display: flex;
    gap: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-border);
}}

.post-action-btn {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: none;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.post-action-btn:hover {{
    background: var(--color-surface);
    color: var(--color-primary);
}}

.post-action-btn.liked {{
    color: var(--color-primary);
    font-weight: 500;
}}

.load-more-container {{
    text-align: center;
    padding: 2rem 0;
}}

.btn-load-more {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-full);
    font-family: var(--font-primary);
    font-size: 0.875rem;
    color: var(--color-text);
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.btn-load-more:hover {{
    background: var(--color-bg);
    border-color: var(--color-primary);
    transform: translateY(-2px);
}}

/* SUGGESTIONS */
.suggestion-item {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: var(--radius-md);
    transition: background var(--transition-fast);
}}

.suggestion-item:hover {{
    background: var(--color-surface);
}}

.suggestion-avatar {{
    width: 40px;
    height: 40px;
    border-radius: var(--radius-full);
    object-fit: cover;
}}

.suggestion-info {{
    flex: 1;
}}

.suggestion-info h5 {{
    font-size: 0.875rem;
    margin: 0 0 0.125rem;
    line-height: 1.2;
}}

.suggestion-info p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0 0 0.125rem;
}}

.suggestion-mutual {{
    font-size: 0.75rem;
    color: var(--color-primary);
}}

.btn-follow {{
    padding: 0.375rem 0.75rem;
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-full);
    font-family: var(--font-primary);
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
}}

.btn-follow:hover {{
    background: var(--color-secondary);
}}

/* ADS */
.ad-content {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.ad-image {{
    width: 100%;
    height: 150px;
    border-radius: var(--radius-md);
    object-fit: cover;
}}

.ad-text h5 {{
    font-size: 0.875rem;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}}

.ad-text p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0 0 1rem;
    line-height: 1.5;
}}

.btn-ad {{
    width: 100%;
    padding: 0.5rem;
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    font-size: 0.75rem;
    font-weight: 500;
    cursor: pointer;
    transition: background var(--transition-fast);
}}

.btn-ad:hover {{
    background: var(--color-secondary);
}}

.quick-links {{
    text-align: center;
    padding: 1rem;
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}}

.quick-links a {{
    color: var(--color-text-secondary);
    text-decoration: none;
}}

.quick-links a:hover {{
    color: var(--color-primary);
    text-decoration: underline;
}}

.copyright {{
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}}

/* FOOTER */
.footer {{
    background: var(--color-surface);
    border-top: 1px solid var(--color-border);
    padding: 3rem 0 1.5rem;
    margin-top: 3rem;
}}

.footer-content {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}}

.footer-logo {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}}

.footer-logo .logo-icon {{
    font-size: 2rem;
}}

.footer-logo h3 {{
    font-size: 1.5rem;
    margin: 0;
}}

.footer-description {{
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
    line-height: 1.6;
}}

.footer-social {{
    display: flex;
    gap: 1rem;
}}

.footer-social a {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: var(--color-bg);
    border-radius: var(--radius-full);
    color: var(--color-text);
    text-decoration: none;
    transition: all var(--transition-fast);
}}

.footer-social a:hover {{
    background: var(--color-primary);
    color: white;
    transform: translateY(-2px);
}}

.footer-section h4 {{
    font-size: 1rem;
    margin-bottom: 1rem;
    color: var(--color-text);
}}

.footer-section ul {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.footer-section li {{
    margin-bottom: 0.5rem;
}}

.footer-section a {{
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color var(--transition-fast);
}}

.footer-section a:hover {{
    color: var(--color-primary);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid var(--color-border);
}}

.footer-bottom p {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0.25rem 0;
}}

/* FLOATING BUTTONS */
.floating-buttons {{
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    z-index: 999;
}}

.fab {{
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-full);
    box-shadow: var(--shadow-lg);
    cursor: pointer;
    transition: all var(--transition-fast);
    position: relative;
}}

.fab:hover {{
    background: var(--color-secondary);
    transform: translateY(-2px) scale(1.05);
    box-shadow: var(--shadow-xl);
}}

.fab i {{
    font-size: 1.25rem;
}}

.fab[data-tooltip]::before {{
    content: attr(data-tooltip);
    position: absolute;
    right: calc(100% + 10px);
    top: 50%;
    transform: translateY(-50%);
    background: var(--color-text);
    color: var(--color-bg);
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all var(--transition-fast);
    pointer-events: none;
}}

.fab[data-tooltip]:hover::before {{
    opacity: 1;
    visibility: visible;
}}

.btn-chat {{}}
.btn-theme {{ background: var(--color-surface); color: var(--color-text); }}
.btn-scroll-top {{ background: var(--color-text-secondary); }}
.btn-create-fab {{ background: var(--color-primary); }}

/* TOAST */
.toast-container {{
    position: fixed;
    bottom: 2rem;
    left: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 9999;
}}

.toast {{
    min-width: 300px;
    padding: 1rem;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    animation: toastSlideIn 0.3s ease-out;
}}

@keyframes toastSlideIn {{
    from {{
        opacity: 0;
        transform: translateX(-100%);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.toast.success {{
    border-left: 4px solid var(--color-success);
}}

.toast.error {{
    border-left: 4px solid var(--color-danger);
}}

.toast.warning {{
    border-left: 4px solid var(--color-warning);
}}

.toast.info {{
    border-left: 4px solid var(--color-info);
}}

.toast-icon {{
    font-size: 1.25rem;
}}

.toast.success .toast-icon {{ color: var(--color-success); }}
.toast.error .toast-icon {{ color: var(--color-danger); }}
.toast.warning .toast-icon {{ color: var(--color-warning); }}
.toast.info .toast-icon {{ color: var(--color-info); }}

.toast-content {{
    flex: 1;
}}

.toast-title {{
    font-size: 0.875rem;
    font-weight: 600;
    margin: 0 0 0.25rem;
}}

.toast-message {{
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin: 0;
    line-height: 1.4;
}}

.toast-close {{
    background: none;
    border: none;
    color: var(--color-text-secondary);
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-full);
    transition: background var(--transition-fast);
}}

.toast-close:hover {{
    background: var(--color-surface);
}}

/* RESPONSIVE */
@media (max-width: 768px) {{
    .nav-search {{
        display: none;
    }}
    
    .nav-menu .nav-text {{
        display: none;
    }}
    
    .menu-toggle {{
        display: flex;
    }}
    
    .nav-menu:not(.mobile-open) {{
        display: none;
    }}
    
    .nav-menu.mobile-open {{
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        background: var(--color-bg);
        border-top: 1px solid var(--color-border);
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0;
    }}
    
    .nav-menu.mobile-open .nav-link {{
        flex-direction: row;
        justify-content: flex-start;
        padding: 1rem;
        border-radius: var(--radius-md);
    }}
    
    .nav-menu.mobile-open .nav-link:hover {{
        background: var(--color-surface);
    }}
    
    .nav-menu.mobile-open .nav-text {{
        display: block;
        font-size: 0.875rem;
        margin: 0;
    }}
    
    .grid-container {{
        grid-template-columns: 1fr;
        gap: 1rem;
        padding: 1rem 0;
    }}
    
    .sidebar {{
        position: static;
        height: auto;
    }}
    
    .user-card {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}
    
    .user-card-header {{
        width: 100%;
    }}
    
    .user-avatar-large {{
        position: static;
        transform: none;
        margin: -40px auto 1rem;
    }}
    
    .create-post-actions {{
        flex-wrap: wrap;
    }}
    
    .action-btn {{
        min-width: calc(50% - 0.25rem);
    }}
    
    .floating-buttons {{
        bottom: 1rem;
        right: 1rem;
    }}
    
    .fab {{
        width: 48px;
        height: 48px;
    }}
    
    .fab[data-tooltip]::before {{
        display: none;
    }}
    
    .toast-container {{
        left: 1rem;
        right: 1rem;
        bottom: 1rem;
    }}
    
    .toast {{
        min-width: auto;
        width: 100%;
    }}
}}

@media (max-width: 480px) {{
    .container {{
        padding: 0 0.5rem;
    }}
    
    .btn {{
        padding: 0.5rem 1rem;
        font-size: 0.75rem;
    }}
    
    .card, .create-post-card, .stories-section, .post-card {{
        padding: 1rem;
    }}
    
    .create-post-actions {{
        flex-direction: column;
    }}
    
    .action-btn {{
        width: 100%;
        min-width: auto;
    }}
    
    .post-actions {{
        flex-wrap: wrap;
    }}
    
    .post-action-btn {{
        min-width: calc(33.333% - 0.333rem);
    }}
}}

/* ANIMACIONES ESPECIALES */
@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
}}

@keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(var(--color-primary-rgb), 0.7); }}
    50% {{ box-shadow: 0 0 0 10px rgba(var(--color-primary-rgb), 0); }}
}}

@keyframes shimmer {{
    0% {{ background-position: -200% center; }}
    100% {{ background-position: 200% center; }}
}}

.animate-float {{ animation: float 3s ease-in-out infinite; }}
.animate-pulse-glow {{ animation: pulse-glow 2s infinite; }}
.animate-shimmer {{ 
    background: linear-gradient(
        90deg,
        var(--color-surface) 0%,
        rgba(var(--color-primary-rgb), 0.1) 50%,
        var(--color-surface) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
}}

/* EFECTOS GLASS */
.glass-effect {{
    background: rgba(var(--color-bg-rgb), 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(var(--color-border-rgb), 0.2);
}}

/* EFECTOS GRADIENT */
.gradient-text {{
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.gradient-border {{
    position: relative;
    border-radius: var(--radius-lg);
}}

.gradient-border::before {{
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    border-radius: calc(var(--radius-lg) + 2px);
    z-index: -1;
}}

/* UTILIDADES DE ANIMACIÓN */
.delay-100 {{ animation-delay: 100ms; }}
.delay-200 {{ animation-delay: 200ms; }}
.delay-300 {{ animation-delay: 300ms; }}
.delay-500 {{ animation-delay: 500ms; }}
.delay-700 {{ animation-delay: 700ms; }}
.delay-1000 {{ animation-delay: 1000ms; }}

/* ESTILOS ESPECÍFICOS POR TEMA */
[data-theme="futurista"] .glass-effect {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

[data-theme="organico"] {{
    --color-primary: #556b2f;
    --color-secondary: #8fbc8f;
    --color-accent: #deb887;
}}

[data-theme="organico"] .card {{
    background: linear-gradient(135deg, #f5f5dc, #f0fff0);
}}

[data-theme="urbano"] {{
    --color-primary: #2c3e50;
    --color-secondary: #34495e;
    --color-accent: #e74c3c;
}}

[data-theme="urbano"] .card {{
    background: linear-gradient(135deg, #ecf0f1, #bdc3c7);
}}

/* EFECTOS HOVER ESPECIALES */
.hover-lift {{ transition: transform var(--transition-normal); }}
.hover-lift:hover {{ transform: translateY(-8px); }}

.hover-glow {{ transition: box-shadow var(--transition-normal); }}
.hover-glow:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); }}

.hover-scale {{ transition: transform var(--transition-normal); }}
.hover-scale:hover {{ transform: scale(1.05); }}

/* SCROLLBAR PERSONALIZADO */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--color-surface);
    border-radius: var(--radius-full);
}}

::-webkit-scrollbar-thumb {{
    background: var(--color-border);
    border-radius: var(--radius-full);
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--color-text-secondary);
}}

/* SELECTION */
::selection {{
    background: rgba(var(--color-primary-rgb), 0.3);
    color: var(--color-text);
}}

/* FOCUS VISIBLE */
:focus-visible {{
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}}

/* PRINT STYLES */
@media print {{
    .navbar,
    .sidebar,
    .floating-buttons,
    .btn-create-post,
    .post-actions,
    .footer {{
        display: none !important;
    }}
    
    body {{
        background: white !important;
        color: black !important;
    }}
    
    .main-container {{
        margin: 0;
        padding: 0;
    }}
    
    .grid-container {{
        grid-template-columns: 1fr;
        gap: 0;
    }}
    
    .card {{
        box-shadow: none !important;
        border: 1px solid #ddd !important;
        page-break-inside: avoid;
    }}
}}
'''
    
    def crear_javascript_completo(self):
        """Crear JavaScript completo con todas las funcionalidades"""
        config = self.config
        
        return f'''
// ====================================================
// {config['nombre'].upper()} - APLICACIÓN JAVASCRIPT
// Generado por Community Manager AI Ultra v{config['version']}
// ====================================================

// CONSTANTES Y CONFIGURACIÓN
const APP_CONFIG = {json.dumps(config, indent=2)};
const API_ENDPOINTS = {{
    POSTS: 'data/posts.json',
    USERS: 'data/users.json',
    CONFIG: 'config.json'
}};

// ESTADO DE LA APLICACIÓN
const AppState = {{
    user: {{
        id: 1,
        name: 'Usuario Demo',
        username: '@demo_user',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Usuario',
        bio: 'Apasionado de la tecnología y las redes sociales',
        stats: {{
            posts: 0,
            followers: 0,
            following: 0
        }}
    }},
    posts: [],
    stories: [],
    notifications: [],
    messages: [],
    currentTheme: localStorage.getItem('theme') || 'light',
    isOnline: navigator.onLine,
    isLoading: false
}};

// ELEMENTOS DOM PRINCIPALES
const DOM = {{
    // Containers
    postsContainer: document.getElementById('postsContainer'),
    storiesContainer: document.getElementById('storiesContainer'),
    searchResults: document.getElementById('searchResults'),
    toastContainer: document.getElementById('toastContainer'),
    
    // Modals
    createModal: document.getElementById('createModal'),
    
    // Inputs
    searchInput: document.querySelector('.search-input'),
    postContentInput: document.querySelector('.post-content-input'),
    
    // Buttons
    menuToggle: document.getElementById('menuToggle'),
    userMenuBtn: document.getElementById('userMenuBtn'),
    
    // Counters
    postCount: document.getElementById('postCount'),
    followerCount: document.getElementById('followerCount'),
    followingCount: document.getElementById('followingCount')
}};

// INICIALIZACIÓN DE LA APLICACIÓN
document.addEventListener('DOMContentLoaded', async function() {{
    console.log('🚀 Iniciando {config['nombre']} v{config['version']}');
    
    try {{
        // 1. Configurar tema
        setupTheme();
        
        // 2. Cargar datos iniciales
        await loadInitialData();
        
        // 3. Configurar event listeners
        setupEventListeners();
        
        // 4. Configurar Service Worker (PWA)
        setupServiceWorker();
        
        // 5. Mostrar bienvenida
        showWelcomeMessage();
        
        console.log('✅ Aplicación iniciada correctamente');
    }} catch (error) {{
        console.error('❌ Error al iniciar la aplicación:', error);
        showToast('Error al cargar la aplicación', 'error');
    }}
}});

// FUNCIONES DE INICIALIZACIÓN
function setupTheme() {{
    document.documentElement.setAttribute('data-theme', AppState.currentTheme);
    updateThemeIcon();
}}

async function loadInitialData() {{
    AppState.isLoading = true;
    showLoading(true);
    
    try {{
        // Cargar posts
        const postsResponse = await fetch(API_ENDPOINTS.POSTS);
        AppState.posts = await postsResponse.json();
        renderPosts();
        
        // Cargar historias
        await loadStories();
        
        // Cargar sugerencias
        await loadSuggestions();
        
        // Actualizar contadores
        updateCounters();
        
        // Simular carga de notificaciones
        simulateNotifications();
        
        showToast('Datos cargados correctamente', 'success');
    }} catch (error) {{
        console.error('Error cargando datos:', error);
        showToast('Error cargando datos', 'error');
        loadSampleData();
    }} finally {{
        AppState.isLoading = false;
        showLoading(false);
    }}
}}

function setupEventListeners() {{
    // Menú móvil
    if (DOM.menuToggle) {{
        DOM.menuToggle.addEventListener('click', toggleMobileMenu);
    }}
    
    // Menú usuario
    if (DOM.userMenuBtn) {{
        DOM.userMenuBtn.addEventListener('click', toggleUserMenu);
    }}
    
    // Búsqueda
    if (DOM.searchInput) {{
        DOM.searchInput.addEventListener('input', handleSearch);
        DOM.searchInput.addEventListener('focus', showSearchResults);
        DOM.searchInput.addEventListener('blur', hideSearchResults);
    }}
    
    // Modal crear post
    document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') closeCreateModal();
        if (e.key === 'n' && (e.ctrlKey || e.metaKey)) openCreateModal();
    }});
    
    // Detectar conexión
    window.addEventListener('online', () => {{
        AppState.isOnline = true;
        showToast('Conectado a internet', 'success');
    }});
    
    window.addEventListener('offline', () => {{
        AppState.isOnline = false;
        showToast('Sin conexión a internet', 'warning');
    }});
    
    // Scroll infinito
    window.addEventListener('scroll', handleInfiniteScroll);
}}

function setupServiceWorker() {{
    if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {{
                console.log('✅ Service Worker registrado:', registration.scope);
            }})
            .catch(error => {{
                console.error('❌ Error registrando Service Worker:', error);
            }});
    }}
}}

// FUNCIONES DE RENDERIZADO
function renderPosts() {{
    if (!DOM.postsContainer || !AppState.posts.length) return;
    
    DOM.postsContainer.innerHTML = '';
    
    AppState.posts.forEach((post, index) => {{
        const postElement = createPostElement(post, index);
        DOM.postsContainer.appendChild(postElement);
    }});
    
    // Aplicar animaciones escalonadas
    animateStaggered('.post-card', 'animate-fade-in');
}}

function createPostElement(post, index) {{
    const div = document.createElement('div');
    div.className = 'post-card glass-effect';
    div.style.animationDelay = `${{index * 100}}ms`;
    
    const formattedDate = formatPostDate(post.createdAt || new Date().toISOString());
    
    div.innerHTML = `
        <div class="post-header">
            <div class="post-author">
                <img src="${{post.author?.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + post.author?.name}}" 
                     alt="${{post.author?.name}}" class="post-avatar">
                <div class="post-author-info">
                    <h5>${{post.author?.name || 'Usuario'}}</h5>
                    <p>${{formattedDate}}</p>
                </div>
            </div>
            <button class="post-more" onclick="showPostOptions(${{post.id}})">
                <i class="fas fa-ellipsis-h"></i>
            </button>
        </div>
        
        <div class="post-content">
            <p class="post-text">${{post.content}}</p>
            
            ${{post.media ? `
                <div class="post-media">
                    ${{post.media.type === 'image' ? `
                        <img src="${{post.media.url}}" alt="Imagen del post" class="post-image" onclick="openImageModal('${{post.media.url}}')">
                    ` : post.media.type === 'video' ? `
                        <video class="post-video" controls>
                            <source src="${{post.media.url}}" type="video/mp4">
                        </video>
                    ` : ''}}
                </div>
            ` : ''}}
            
            ${{post.tags?.length ? `
                <div class="post-tags">
                    ${{post.tags.map(tag => `<span class="post-tag">#${{tag}}</span>`).join('')}}
                </div>
            ` : ''}}
        </div>
        
        <div class="post-stats">
            <span><i class="fas fa-heart"></i> <span class="like-count">${{post.stats?.likes || 0}}</span></span>
            <span><i class="fas fa-comment"></i> <span class="comment-count">${{post.stats?.comments || 0}}</span></span>
            <span><i class="fas fa-share"></i> <span class="share-count">${{post.stats?.shares || 0}}</span></span>
        </div>
        
        <div class="post-actions">
            <button class="post-action-btn ${{post.liked ? 'liked' : ''}}" onclick="likePost(${{post.id}})">
                <i class="fas fa-heart"></i> <span>Me gusta</span>
            </button>
            <button class="post-action-btn" onclick="commentPost(${{post.id}})">
                <i class="fas fa-comment"></i> <span>Comentar</span>
            </button>
            <button class="post-action-btn" onclick="sharePost(${{post.id}})">
                <i class="fas fa-share"></i> <span>Compartir</span>
            </button>
        </div>
    `;
    
    return div;
}}

async function loadStories() {{
    try {{
        // Generar historias de ejemplo
        AppState.stories = Array.from({{length: 10}}, (_, i) => ({{
            id: i + 1,
            user: {{
                name: ['Ana', 'Carlos', 'Laura', 'David', 'Marta'][i % 5],
                avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=Story${{i}}`
            }},
            media: {{
                type: 'image',
                url: `https://source.unsplash.com/random/400x600/?story,people&v=${{i}}`
            }},
            seen: i > 3
        }}));
        
        renderStories();
    }} catch (error) {{
        console.error('Error cargando historias:', error);
    }}
}}

function renderStories() {{
    if (!DOM.storiesContainer) return;
    
    DOM.storiesContainer.innerHTML = '';
    
    AppState.stories.forEach((story, index) => {{
        const storyElement = document.createElement('div');
        storyElement.className = 'story-item';
        storyElement.innerHTML = `
            <div class="story-avatar-container ${{story.seen ? '' : 'has-story'}}" onclick="openStory(${{story.id}})">
                <img src="${{story.user.avatar}}" alt="${{story.user.name}}" class="story-avatar">
            </div>
            <span class="story-username">${{story.user.name}}</span>
        `;
        DOM.storiesContainer.appendChild(storyElement);
    }});
}}

// FUNCIONES DE INTERACCIÓN
function likePost(postId) {{
    const post = AppState.posts.find(p => p.id === postId);
    if (!post) return;
    
    // Alternar like
    post.liked = !post.liked;
    post.stats = post.stats || {{likes: 0, comments: 0, shares: 0}};
    post.stats.likes += post.liked ? 1 : -1;
    
    // Actualizar UI
    const likeBtn = document.querySelector(`button[onclick="likePost(${{postId}})"]`);
    const likeCount = document.querySelector(`.post-card:nth-child(${{AppState.posts.indexOf(post) + 1}}) .like-count`);
    
    if (likeBtn) {{
        likeBtn.classList.toggle('liked', post.liked);
        likeBtn.innerHTML = `<i class="fas fa-heart"></i> <span>${{post.liked ? 'Te gusta' : 'Me gusta'}}</span>`;
        
        // Animación de corazón
        const icon = likeBtn.querySelector('i');
        icon.style.animation = 'heartBeat 0.6s ease';
        setTimeout(() => icon.style.animation = '', 600);
    }}
    
    if (likeCount) {{
        likeCount.textContent = post.stats.likes;
        likeCount.parentElement.style.animation = 'pulse 0.3s ease';
        setTimeout(() => likeCount.parentElement.style.animation = '', 300);
    }}
    
    // Notificación
    if (post.liked) {{
        showToast('¡Post liked!', 'success');
    }}
    
    // Simular envío al servidor
    simulateAPICall('likePost', {{ postId, liked: post.liked }});
}}

function commentPost(postId) {{
    const comment = prompt('Escribe tu comentario:');
    if (!comment?.trim()) return;
    
    const post = AppState.posts.find(p => p.id === postId);
    if (!post) return;
    
    post.stats = post.stats || {{likes: 0, comments: 0, shares: 0}};
    post.stats.comments++;
    
    // Actualizar UI
    const commentCount = document.querySelector(`.post-card:nth-child(${{AppState.posts.indexOf(post) + 1}}) .comment-count`);
    if (commentCount) {{
        commentCount.textContent = post.stats.comments;
        commentCount.parentElement.style.animation = 'pulse 0.3s ease';
        setTimeout(() => commentCount.parentElement.style.animation = '', 300);
    }}
    
    showToast('Comentario añadido', 'success');
    simulateAPICall('addComment', {{ postId, comment }});
}}

function sharePost(postId) {{
    const post = AppState.posts.find(p => p.id === postId);
    if (!post) return;
    
    post.stats = post.stats || {{likes: 0, comments: 0, shares: 0}};
    post.stats.shares++;
    
    // Web Share API
    if (navigator.share) {{
        navigator.share({{
            title: 'Compartir post',
            text: post.content.substring(0, 100),
            url: window.location.href
        }}).then(() => {{
            showToast('¡Post compartido!', 'success');
        }}).catch(error => {{
            console.log('Error compartiendo:', error);
            copyToClipboard(window.location.href);
        }});
    }} else {{
        copyToClipboard(window.location.href);
    }}
    
    // Actualizar UI
    const shareCount = document.querySelector(`.post-card:nth-child(${{AppState.posts.indexOf(post) + 1}}) .share-count`);
    if (shareCount) {{
        shareCount.textContent = post.stats.shares;
        shareCount.parentElement.style.animation = 'pulse 0.3s ease';
        setTimeout(() => shareCount.parentElement.style.animation = '', 300);
    }}
    
    simulateAPICall('sharePost', {{ postId }});
}}

// MODALES
function openCreateModal(type = 'post') {{
    if (!DOM.createModal) return;
    
    DOM.createModal.classList.add('show');
    document.body.style.overflow = 'hidden';
    
    // Configurar según tipo
    const modalTitle = document.querySelector('.modal-header h3');
    if (modalTitle) {{
        modalTitle.textContent = type === 'photo' ? 'Subir foto/video' :
                                 type === 'live' ? 'Transmitir en vivo' :
                                 type === 'event' ? 'Crear evento' :
                                 type === 'poll' ? 'Crear encuesta' :
                                 'Crear publicación';
    }}
    
    // Animación de entrada
    DOM.createModal.style.animation = 'modalSlideIn 0.3s ease-out';
}}

function closeCreateModal() {{
    if (!DOM.createModal) return;
    
    DOM.createModal.style.animation = 'modalSlideOut 0.3s ease-out';
    
    setTimeout(() => {{
        DOM.createModal.classList.remove('show');
        document.body.style.overflow = 'auto';
        
        // Limpiar formulario
        if (DOM.postContentInput) {{
            DOM.postContentInput.value = '';
        }}
        
        const postPreview = document.getElementById('postPreview');
        if (postPreview) {{
            postPreview.innerHTML = '';
            postPreview.classList.remove('has-content');
        }}
    }}, 250);
}}

function submitPost() {{
    const content = DOM.postContentInput?.value?.trim();
    if (!content) {{
        showToast('Escribe algo para publicar', 'warning');
        return;
    }}
    
    const newPost = {{
        id: Date.now(),
        author: {{
            name: AppState.user.name,
            username: AppState.user.username,
            avatar: AppState.user.avatar
        }},
        content: content,
        createdAt: new Date().toISOString(),
        stats: {{ likes: 0, comments: 0, shares: 0 }},
        liked: false,
        tags: extractHashtags(content)
    }};
    
    // Añadir al principio
    AppState.posts.unshift(newPost);
    
    // Renderizar
    renderPosts();
    
    // Actualizar contadores
    AppState.user.stats.posts++;
    updateCounters();
    
    // Cerrar modal
    closeCreateModal();
    
    // Mostrar éxito
    showToast('¡Publicación creada!', 'success');
    
    // Simular envío al servidor
    simulateAPICall('createPost', newPost);
    
    // Efecto de confeti
    createConfetti();
}}

// TEMAS
function toggleTheme() {{
    AppState.currentTheme = AppState.currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', AppState.currentTheme);
    localStorage.setItem('theme', AppState.currentTheme);
    updateThemeIcon();
    
    showToast(`Modo ${{AppState.currentTheme === 'dark' ? 'oscuro' : 'claro'}} activado`, 'info');
}}

function updateThemeIcon() {{
    const themeIcon = document.querySelector('.btn-theme i');
    if (themeIcon) {{
        themeIcon.className = AppState.currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }}
}}

// UTILIDADES
function showToast(message, type = 'info') {{
    if (!DOM.toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${{type}}`;
    
    const icons = {{
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    }};
    
    toast.innerHTML = `
        <i class="toast-icon ${{icons[type] || icons.info}}"></i>
        <div class="toast-content">
            <h4 class="toast-title">${{type.charAt(0).toUpperCase() + type.slice(1)}}</h4>
            <p class="toast-message">${{message}}</p>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    DOM.toastContainer.appendChild(toast);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {{
        if (toast.parentElement) {{
            toast.style.animation = 'toastSlideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }}
    }}, 5000);
}}

function showLoading(show) {{
    const preloader = document.querySelector('.preloader');
    if (preloader) {{
        preloader.style.display = show ? 'flex' : 'none';
        preloader.style.opacity = show ? '1' : '0';
    }}
}}

function updateCounters() {{
    if (DOM.postCount) DOM.postCount.textContent = AppState.user.stats.posts;
    if (DOM.followerCount) DOM.followerCount.textContent = AppState.user.stats.followers;
    if (DOM.followingCount) DOM.followingCount.textContent = AppState.user.stats.following;
}}

function formatPostDate(dateString) {{
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Ahora mismo';
    if (diffMins < 60) return `Hace ${{diffMins}} min`;
    if (diffHours < 24) return `Hace ${{diffHours}} h`;
    if (diffDays < 7) return `Hace ${{diffDays}} d`;
    
    return date.toLocaleDateString('es-ES', {{ 
        day: 'numeric', 
        month: 'short',
        year: diffDays > 365 ? 'numeric' : undefined
    }});
}}

function extractHashtags(text) {{
    const hashtags = text.match(/#[a-zA-Z0-9_]+/g);
    return hashtags ? hashtags.map(tag => tag.substring(1)) : [];
}}

function copyToClipboard(text) {{
    navigator.clipboard.writeText(text).then(() => {{
        showToast('Enlace copiado al portapapeles', 'success');
    }}).catch(err => {{
        console.error('Error copiando:', err);
        showToast('Error al copiar', 'error');
    }});
}}

function animateStaggered(selector, animationClass) {{
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {{
        setTimeout(() => {{
            el.classList.add(animationClass);
        }}, index * 100);
    }});
}}

// SIMULACIONES
function simulateAPICall(endpoint, data) {{
    console.log(`📡 Simulando llamada a ${{endpoint}}:`, data);
    return new Promise(resolve => {{
        setTimeout(() => resolve({{ success: true, data }}), 500);
    }});
}}

function simulateNotifications() {{
    // Simular notificaciones cada 30 segundos
    setInterval(() => {{
        if (Math.random() > 0.7) {{
            const notifications = [
                'Nuevo seguidor: @nuevo_usuario',
                'A Carlos le gustó tu publicación',
                'Recordatorio: Evento en 1 hora',
                'Tendencia: #NuevaActualización'
            ];
            
            const randomNotification = notifications[Math.floor(Math.random() * notifications.length)];
            showToast(randomNotification, 'info');
        }}
    }}, 30000);
}}

function loadSampleData() {{
    // Datos de ejemplo si falla la carga
    AppState.posts = [
        {{
            id: 1,
            author: {{ name: 'María Gómez', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria' }},
            content: '¡Qué bonito día hace hoy! 🌞 Perfecto para salir a tomar fotos.',
            createdAt: new Date(Date.now() - 3600000).toISOString(),
            media: {{ type: 'image', url: 'https://source.unsplash.com/random/800x600/?sunny,day' }},
            stats: {{ likes: 45, comments: 12, shares: 3 }},
            liked: false,
            tags: ['fotografia', 'dia', 'sol']
        }},
        {{
            id: 2,
            author: {{ name: 'Carlos Ruiz', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Carlos' }},
            content: 'Acabando mi proyecto final de la universidad 🎓 #estudiante #programacion',
            createdAt: new Date(Date.now() - 7200000).toISOString(),
            stats: {{ likes: 89, comments: 23, shares: 5 }},
            liked: true,
            tags: ['estudiante', 'programacion', 'universidad']
        }}
    ];
    
    renderPosts();
    updateCounters();
}}

// FUNCIONES GLOBALES (para onclick en HTML)
window.toggleMobileMenu = function() {{
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {{
        navMenu.classList.toggle('mobile-open');
        
        // Animación del botón hamburguesa
        const spans = document.querySelectorAll('.menu-toggle span');
        if (navMenu.classList.contains('mobile-open')) {{
            spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
        }} else {{
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }}
    }}
}};

window.toggleUserMenu = function() {{
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {{
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }}
}};

window.openStory = function(storyId) {{
    const story = AppState.stories.find(s => s.id === storyId);
    if (!story) return;
    
    // Marcar como visto
    story.seen = true;
    
    // Mostrar modal de historia
    const modal = document.createElement('div');
    modal.className = 'story-modal';
    modal.innerHTML = `
        <div class="story-modal-content">
            <div class="story-progress">
                <div class="story-progress-bar"></div>
            </div>
            <img src="${{story.media.url}}" alt="Historia">
            <div class="story-modal-footer">
                <div class="story-user-info">
                    <img src="${{story.user.avatar}}" alt="${{story.user.name}}">
                    <span>${{story.user.name}}</span>
                </div>
                <button class="story-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {{
        if (modal.parentElement) modal.remove();
    }}, 5000);
}};

window.followUser = function(userId) {{
    AppState.user.stats.following++;
    updateCounters();
    showToast('¡Usuario seguido!', 'success');
}};

window.joinEvent = function(eventId) {{
    showToast(`¡Te has unido al evento ${{eventId}}!`, 'success');
}};

window.scrollToTop = function() {{
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}};

window.openChat = function() {{
    showToast('Funcionalidad de chat próximamente', 'info');
}};

window.showWelcomeMessage = function() {{
    setTimeout(() => {{
        showToast(`¡Bienvenido a ${{APP_CONFIG.nombre}}! 🎉`, 'success');
    }}, 1000);
}};

// FUNCIONES NO IMPLEMENTADAS (placeholders)
window.handleSearch = function() {{}};
window.showSearchResults = function() {{}};
window.hideSearchResults = function() {{}};
window.handleInfiniteScroll = function() {{}};
window.showPostOptions = function() {{}};
window.openImageModal = function() {{}};
window.createConfetti = function() {{}};

// EXPORTAR PARA DESARROLLO
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{
        AppState,
        DOM,
        setupTheme,
        loadInitialData,
        renderPosts,
        likePost,
        commentPost,
        sharePost,
        openCreateModal,
        closeCreateModal,
        submitPost,
        toggleTheme,
        showToast
    }};
}}

console.log('✨ {config['nombre']} JavaScript cargado correctamente');
'''
    
    def generar_componentes(self):
        """Generar componentes individuales"""
        componentes = {
            'navbar.html': self.componente_navbar(),
            'post-card.html': self.componente_post(),
            'story-card.html': self.componente_story(),
            'user-card.html': self.componente_user()
        }
        
        for nombre, contenido in componentes.items():
            ruta = Path(f'components/{nombre}')
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ components/{nombre}")
    
    def generar_datos_ejemplo(self):
        """Generar datos de ejemplo"""
        datos = {
            'posts': self.crear_posts_ejemplo(),
            'users': self.crear_usuarios_ejemplo(),
            'analytics': self.crear_analytics_ejemplo()
        }
        
        for nombre, contenido in datos.items():
            ruta = Path(f'data/{nombre}.json')
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(contenido, f, indent=2, ensure_ascii=False)
            print(f"   ✅ data/{nombre}.json")
    
    def generar_documentacion(self):
        """Generar documentación completa"""
        docs = {
            'README.md': self.crear_readme(),
            'INSTALL.md': self.crear_guia_instalacion(),
            'API.md': self.crear_documentacion_api(),
            'CHANGELOG.md': self.crear_changelog()
        }
        
        for nombre, contenido in docs.items():
            with open(nombre, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"   ✅ {nombre}")
    
    def crear_readme(self):
        """Crear README completo"""
        config = self.config
        
        return f'''# {config['nombre']}

{config['icono']} **{config['nombre']}** - {config['eslogan']}

> {config['descripcion']}

## 🚀 Características

✅ **Diseño {self.respuestas['estilo']['nombre']}** con animaciones avanzadas  
✅ **{self.respuestas['caracteristica']['nombre']}** como característica principal  
✅ **Totalmente responsive** (móvil, tablet, desktop)  
✅ **PWA** (Instalable como app nativa)  
✅ **Modo offline** funcional  
✅ **Notificaciones push**  
✅ **SEO optimizado**  
✅ **Performance 95+** en Lighthouse  

## 📁 Estructura del Proyecto
