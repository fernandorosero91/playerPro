"""
Configuración del proyecto
Maneja las API keys y configuraciones sensibles
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # YouTube API Configuration
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

    # Configuración de la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Configuración de archivos - usar rutas absolutas para mayor robustez
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    
    # Configuración de YouTube
    YOUTUBE_MAX_RESULTS = 20
    YOUTUBE_SEARCH_TIMEOUT = 30
    
    @staticmethod
    def validate_youtube_api():
        """Valida que la API key de YouTube esté configurada"""
        if not Config.YOUTUBE_API_KEY:
            print("⚠️  ADVERTENCIA: YouTube API Key no configurada")
            print("   Algunas funcionalidades de YouTube no estarán disponibles")
            return False
        return True