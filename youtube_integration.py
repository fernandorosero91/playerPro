"""
YouTube Integration Module
Maneja la búsqueda y descarga de audio desde YouTube usando API oficial
"""

import yt_dlp
import os
import uuid
import requests
from config import Config

class YouTubeIntegration:
    def __init__(self, download_path='downloads'):
        self.download_path = download_path
        self.api_key = Config.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
        os.makedirs(download_path, exist_ok=True)
        
        # Configuración para yt-dlp
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'extract_flat': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True
        }
    
    def search_youtube_api(self, query, max_results=10):
        """Busca videos usando YouTube Data API v3 (oficial)"""
        if not self.api_key:
            print("⚠️  YouTube API Key no configurada, usando método alternativo...")
            return self.search_youtube_fallback(query, max_results)
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key,
                'videoCategoryId': '10',  # Música
                'order': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            video_ids = []
            
            # Recopilar IDs de videos para obtener duración
            for item in data.get('items', []):
                # Verificar que el item tenga la estructura correcta
                if 'id' in item and isinstance(item['id'], dict) and 'videoId' in item['id']:
                    video_ids.append(item['id']['videoId'])
            
            # Obtener detalles adicionales (duración, estadísticas)
            if video_ids:
                details = self.get_video_details(video_ids)
                
                for i, item in enumerate(data.get('items', [])):
                    # Verificar estructura del item
                    if 'id' not in item or not isinstance(item['id'], dict) or 'videoId' not in item['id']:
                        continue
                        
                    video_id = item['id']['videoId']
                    snippet = item['snippet']
                    
                    # Obtener duración del detalle
                    duration = 0
                    if video_id in details:
                        duration = self.parse_duration(details[video_id].get('duration', 'PT0S'))
                    
                    results.append({
                        'id': video_id,
                        'title': snippet['title'],
                        'uploader': snippet['channelTitle'],
                        'duration': duration,
                        'thumbnail': snippet['thumbnails'].get('medium', {}).get('url', ''),
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'description': snippet.get('description', '')[:100] + '...',
                        'publishedAt': snippet['publishedAt']
                    })
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error con YouTube API: {e}")
            return self.search_youtube_fallback(query, max_results)
        except KeyError as e:
            print(f"Error de estructura en respuesta de YouTube API: {e}")
            return self.search_youtube_fallback(query, max_results)
        except Exception as e:
            print(f"Error inesperado en YouTube API: {e}")
            return self.search_youtube_fallback(query, max_results)
    
    def get_video_details(self, video_ids):
        """Obtiene detalles adicionales de los videos"""
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'contentDetails,statistics',
                'id': ','.join(video_ids),
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            details = {}
            for item in data.get('items', []):
                video_id = item['id']
                details[video_id] = {
                    'duration': item['contentDetails']['duration'],
                    'viewCount': item['statistics'].get('viewCount', 0)
                }
            
            return details
            
        except Exception as e:
            print(f"Error obteniendo detalles de videos: {e}")
            return {}
    
    def parse_duration(self, duration_str):
        """Convierte duración ISO 8601 a segundos"""
        try:
            # Formato: PT4M13S (4 minutos 13 segundos)
            import re
            pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
            match = re.match(pattern, duration_str)
            
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                seconds = int(match.group(3) or 0)
                return hours * 3600 + minutes * 60 + seconds
            
            return 0
        except:
            return 0
    
    def search_youtube_fallback(self, query, max_results=10):
        """Método de respaldo usando yt-dlp cuando no hay API key"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'extract_flat': False
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                search_results = ydl.extract_info(
                    f"ytsearch{max_results}:{query}",
                    download=False
                )
                
                if not search_results or 'entries' not in search_results:
                    print("No se encontraron resultados en la búsqueda de respaldo")
                    return []
                
                results = []
                for entry in search_results['entries']:
                    if not entry:  # Saltar entradas vacías
                        continue
                        
                    results.append({
                        'id': entry.get('id', 'unknown'),
                        'title': entry.get('title', 'Título desconocido'),
                        'uploader': entry.get('uploader', 'Canal desconocido'),
                        'duration': entry.get('duration', 0),
                        'thumbnail': entry.get('thumbnail', ''),
                        'url': entry.get('webpage_url', ''),
                        'description': (entry.get('description', '') or '')[:100] + '...',
                        'publishedAt': 'Fecha desconocida'
                    })
                
                return results
        except Exception as e:
            print(f"Error en búsqueda de respaldo: {e}")
            return []
    
    def search_youtube(self, query, max_results=10):
        """Método principal de búsqueda (usa API si está disponible)"""
        return self.search_youtube_api(query, max_results)
    
    def download_audio(self, video_url):
        """Descarga audio de un video de YouTube"""
        try:
            # Generar nombre único para el archivo
            unique_id = str(uuid.uuid4())[:8]
            
            # Configuración específica para descarga
            download_opts = self.ydl_opts.copy()
            download_opts['outtmpl'] = os.path.join(
                self.download_path, 
                f'{unique_id}_%(title)s.%(ext)s'
            )
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                # Extraer información del video
                info = ydl.extract_info(video_url, download=False)
                title = info.get('title', 'Unknown')
                uploader = info.get('uploader', 'Unknown')
                
                # Descargar el audio
                ydl.download([video_url])
                
                # Encontrar el archivo descargado
                for file in os.listdir(self.download_path):
                    if file.startswith(unique_id):
                        return {
                            'success': True,
                            'filename': file,
                            'title': title,
                            'artist': uploader,
                            'path': os.path.join(self.download_path, file)
                        }
                
                return {'success': False, 'error': 'File not found after download'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_video_info(self, video_url):
        """Obtiene información de un video sin descargarlo"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'extract_flat': False,
                'skip_download': True
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                if not info:
                    return {'error': 'No se pudo obtener información del video'}
                
                # Verificar si el video está disponible
                availability = info.get('availability', 'unknown')
                if availability in ['private', 'premium_only', 'subscriber_only']:
                    return {'error': f'Video no disponible: {availability}'}
        
                # Verificar si el video permite reproducción embebida
                embed_url = info.get('embed_url')
                if not embed_url:
                    return {'error': 'Video no permite reproducción embebida'}
        
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': info.get('description', '')[:200] + '...',
                    'availability': availability,
                    'is_live': info.get('is_live', False)
                }
        except Exception as e:
            error_msg = str(e)
            if 'HTTP Error 400' in error_msg:
                return {'error': 'Video no disponible o bloqueado por YouTube'}
            elif 'Private video' in error_msg:
                return {'error': 'Video privado'}
            elif 'Video unavailable' in error_msg:
                return {'error': 'Video no disponible'}
            else:
                return {'error': f'Error al obtener información: {error_msg}'}