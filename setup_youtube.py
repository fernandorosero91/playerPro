#!/usr/bin/env python3
"""
Script de configuración para YouTube API
Ayuda a configurar la API key de YouTube de forma interactiva
"""

import os
import sys

def create_env_file():
    """Crea el archivo .env con la configuración"""
    print("🔑 Configuración de YouTube API")
    print("=" * 50)
    
    # Verificar si ya existe .env
    if os.path.exists('.env'):
        print("⚠️  El archivo .env ya existe.")
        overwrite = input("¿Quieres sobrescribirlo? (s/N): ").lower().strip()
        if overwrite != 's':
            print("❌ Configuración cancelada.")
            return False
    
    print("\n📋 Necesitas una API Key de YouTube Data API v3")
    print("   Sigue estos pasos:")
    print("   1. Ve a: https://console.cloud.google.com/")
    print("   2. Crea un proyecto o selecciona uno existente")
    print("   3. Habilita 'YouTube Data API v3'")
    print("   4. Crea credenciales > Clave de API")
    print("   5. Copia la clave generada")
    
    print("\n" + "-" * 50)
    
    # Solicitar API Key
    api_key = input("🔑 Pega tu YouTube API Key aquí: ").strip()
    
    if not api_key:
        print("❌ API Key no puede estar vacía.")
        return False
    
    if not api_key.startswith('AIza'):
        print("⚠️  La API Key no parece válida (debería empezar con 'AIza')")
        continue_anyway = input("¿Continuar de todas formas? (s/N): ").lower().strip()
        if continue_anyway != 's':
            return False
    
    # Solicitar clave secreta
    secret_key = input("🔐 Clave secreta para la app (opcional, presiona Enter para generar): ").strip()
    
    if not secret_key:
        import secrets
        secret_key = secrets.token_urlsafe(32)
        print(f"✅ Clave secreta generada automáticamente")
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración de YouTube API
YOUTUBE_API_KEY={api_key}

# Configuración de la aplicación
SECRET_KEY={secret_key}
DEBUG=True

# Configuración generada automáticamente por setup_youtube.py
# No compartas este archivo en repositorios públicos
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        print("📁 Ubicación: " + os.path.abspath('.env'))
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def test_api_key():
    """Prueba la API key configurada"""
    try:
        from config import Config
        from youtube_integration import YouTubeIntegration
        
        if not Config.YOUTUBE_API_KEY:
            print("❌ No se encontró API Key en la configuración")
            return False
        
        print("\n🧪 Probando API Key...")
        youtube = YouTubeIntegration()
        
        # Hacer una búsqueda de prueba
        results = youtube.search_youtube("test music", max_results=1)
        
        if results and len(results) > 0:
            print("✅ API Key funciona correctamente!")
            print(f"   Resultado de prueba: {results[0]['title']}")
            return True
        else:
            print("⚠️  API Key configurada pero no devuelve resultados")
            print("   Verifica que la API esté habilitada y tenga cuota disponible")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error probando API Key: {e}")
        return False

def show_usage_instructions():
    """Muestra instrucciones de uso"""
    print("\n" + "=" * 60)
    print("🎵 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. Ejecutar: python backend.py")
    print("   2. Abrir: http://localhost:5000")
    print("   3. Hacer clic en 'Buscar en YouTube'")
    print("   4. ¡Disfrutar de la música!")
    
    print("\n⚠️  IMPORTANTE:")
    print("   • No subas el archivo .env a repositorios públicos")
    print("   • La API de YouTube tiene límites de cuota diarios")
    print("   • Si no funciona, verifica que la API esté habilitada")
    
    print("\n🔗 ENLACES ÚTILES:")
    print("   • Google Cloud Console: https://console.cloud.google.com/")
    print("   • YouTube API Docs: https://developers.google.com/youtube/v3")
    print("=" * 60)

def main():
    print("🚀 Configurador de YouTube API para Reproductor Musical Pro")
    
    # Crear archivo .env
    if create_env_file():
        # Probar la API key
        if test_api_key():
            show_usage_instructions()
            print("\n✅ ¡Configuración exitosa!")
        else:
            print("\n⚠️  Configuración creada pero hay problemas con la API")
            print("   Revisa la API Key y vuelve a intentar")
    else:
        print("\n❌ Error en la configuración")
        sys.exit(1)

if __name__ == "__main__":
    main()