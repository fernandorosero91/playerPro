#!/usr/bin/env python3
"""
Instalador automático para el Reproductor Musical Pro
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala las dependencias necesarias"""
    print("🎵 Instalando dependencias del Reproductor Musical Pro...")
    
    try:
        # Instalar dependencias de Python
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias de Python instaladas correctamente")
        
        # Verificar instalación de yt-dlp
        try:
            import yt_dlp
            print("✅ yt-dlp instalado correctamente")
        except ImportError:
            print("⚠️  Instalando yt-dlp...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directories():
    """Crea los directorios necesarios"""
    directories = ['uploads', 'downloads', 'static']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio '{directory}' creado")
        else:
            print(f"📁 Directorio '{directory}' ya existe")

def show_instructions():
    """Muestra las instrucciones de uso"""
    print("\n" + "="*60)
    print("🎵 REPRODUCTOR MUSICAL PRO - INSTALACIÓN COMPLETA")
    print("="*60)
    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1. Configurar YouTube API (OPCIONAL):")
    print("   python setup_youtube.py")
    print("\n2. Ejecutar el servidor:")
    print("   python backend.py")
    print("\n3. Abrir en el navegador:")
    print("   http://localhost:5000")
    print("\n🎯 FUNCIONALIDADES DISPONIBLES:")
    print("   ✅ Reproducción de archivos locales")
    print("   ✅ Lista doblemente enlazada")
    print("   ✅ Interfaz profesional")
    print("   ✅ Controles avanzados")
    print("   🔑 Búsqueda en YouTube (requiere API Key)")
    print("   🔑 Descarga de audio desde YouTube (requiere API Key)")
    print("\n⚠️  NOTAS IMPORTANTES:")
    print("   • YouTube API es opcional pero recomendada")
    print("   • Sin API Key, algunas funciones estarán limitadas")
    print("   • La configuración es gratuita y toma 5 minutos")
    print("="*60)

def main():
    print("🚀 Iniciando instalación del Reproductor Musical Pro...")
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if install_requirements():
        show_instructions()
        print("\n✅ ¡Instalación completada exitosamente!")
    else:
        print("\n❌ Error en la instalación. Revisa los errores anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()