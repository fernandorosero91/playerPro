from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dataclasses import dataclass
from typing import Optional, List
import os
import uuid
import pickle
from youtube_integration import YouTubeIntegration
from config import Config

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuración desde config.py
app.config.from_object(Config)
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
DOWNLOAD_FOLDER = Config.DOWNLOAD_FOLDER
PLAYLIST_FILE = 'playlist.pkl'

# Crear directorios necesarios
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Validar configuración de YouTube
Config.validate_youtube_api()

# Inicializar integración de YouTube
youtube = YouTubeIntegration(DOWNLOAD_FOLDER)

def save_playlist():
    try:
        with open(PLAYLIST_FILE, 'wb') as f:
            pickle.dump(playlist.get_all_tracks(), f)
    except Exception as e:
        print(f"Error saving playlist: {e}")

def load_playlist():
    try:
        with open(PLAYLIST_FILE, 'rb') as f:
            tracks = pickle.load(f)
            for track in tracks:
                playlist.append(track)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading playlist: {e}")

# Data structures
@dataclass
class Track:
    path: str
    title: str

class Node:
    def __init__(self, track: Track):
        self.track: Track = track
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class DoublyLinkedPlaylist:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.current: Optional[Node] = None
        self.length = 0
        self.is_playing = False

    def append(self, track: Track):
        node = Node(track)
        if not self.head:
            self.head = self.tail = node
            self.current = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
            self.current = node
        self.length += 1

    def prepend(self, track: Track):
        node = Node(track)
        if not self.head:
            self.head = self.tail = node
            self.current = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
            self.current = node
        self.length += 1

    def insert_at_index(self, index: int, track: Track):
        if index <= 0:
            self.prepend(track)
            return
        if index >= self.length:
            self.append(track)
            return
        node_at = self._node_at_index(index)
        if node_at is None:
            self.append(track)
            return
        node = Node(track)
        prev_node = node_at.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = node_at
        node_at.prev = node
        self.current = node
        self.length += 1

    def remove_node(self, node: Node):
        if node is None:
            return
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        if self.current is node:
            self.current = node.next or node.prev or None
        node.prev = node.next = None
        self.length -= 1

    def remove_by_index(self, index: int) -> bool:
        node = self._node_at_index(index)
        if node:
            self.remove_node(node)
            return True
        return False

    def remove_by_title(self, title: str) -> bool:
        node = self.head
        while node:
            if node.track.title.lower() == title.lower():
                self.remove_node(node)
                return True
            node = node.next
        return False

    def next_track(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current
        return None

    def prev_track(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current
        return None

    def set_current_to_index(self, index: int):
        node = self._node_at_index(index)
        if node:
            self.current = node

    def iterate(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def get_all_tracks(self) -> List[Track]:
        return [node.track for node in self.iterate()]

    def search(self, query: str) -> List[Track]:
        query = query.lower()
        return [node.track for node in self.iterate() if query in node.track.title.lower()]

    def shuffle(self):
        import random
        if self.length < 2:
            return
        tracks = self.get_all_tracks()
        random.shuffle(tracks)
        self.clear()
        for track in tracks:
            self.append(track)
        self.current = self.head

    def move(self, from_index: int, to_index: int):
        if from_index == to_index or from_index < 0 or to_index < 0 or from_index >= self.length or to_index > self.length:
            return
        node = self._node_at_index(from_index)
        if not node:
            return
        # remove the node
        self.remove_node(node)
        # insert at new position
        if to_index > from_index:
            to_index -= 1
        self.insert_at_index(to_index, node.track)

    def clear(self):
        self.head = self.tail = self.current = None
        self.length = 0

    def _node_at_index(self, index: int) -> Optional[Node]:
        if index < 0 or index >= self.length:
            return None
        if index < self.length // 2:
            node = self.head
            i = 0
            while i < index:
                node = node.next
                i += 1
            return node
        else:
            node = self.tail
            i = self.length - 1
            while i > index:
                node = node.prev
                i -= 1
            return node

# Global playlist instance
playlist = DoublyLinkedPlaylist()
load_playlist()

# API Routes
@app.route('/playlist', methods=['GET'])
def get_playlist():
    tracks = playlist.get_all_tracks()
    return jsonify([{'path': t.path, 'title': t.title} for t in tracks])

@app.route('/current', methods=['GET'])
def get_current():
    if playlist.current:
        return jsonify({'path': playlist.current.track.path, 'title': playlist.current.track.title})
    return jsonify({'error': 'No current track'}), 404

@app.route('/add', methods=['POST'])
def add_track():
    path = request.form.get('path')
    title = request.form.get('title')
    position = request.form.get('position', 'end')
    if not path or not title:
        return jsonify({'error': 'Invalid data'}), 400
    track = Track(path=path, title=title)
    if position == 'start':
        playlist.prepend(track)
    elif position == 'end':
        playlist.append(track)
    elif position.isdigit():
        playlist.insert_at_index(int(position), track)
    else:
        return jsonify({'error': 'Invalid position'}), 400
    save_playlist()
    return jsonify({'message': 'Track added'})

@app.route('/remove', methods=['DELETE'])
def remove_track():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    if 'index' in data:
        success = playlist.remove_by_index(data['index'])
    elif 'title' in data:
        success = playlist.remove_by_title(data['title'])
    else:
        return jsonify({'error': 'Specify index or title'}), 400
    if success:
        return jsonify({'message': 'Track removed'})
    return jsonify({'error': 'Track not found'}), 404

@app.route('/next', methods=['POST'])
def next_track():
    if playlist.next_track():
        return jsonify({'message': 'Moved to next'})
    return jsonify({'error': 'No next track'}), 404

@app.route('/prev', methods=['POST'])
def prev_track():
    if playlist.prev_track():
        return jsonify({'message': 'Moved to previous'})
    return jsonify({'error': 'No previous track'}), 404

@app.route('/play', methods=['POST'])
def play():
    if playlist.current:
        playlist.is_playing = True
        return jsonify({'message': 'Playing'})
    return jsonify({'error': 'No track to play'}), 404

@app.route('/pause', methods=['POST'])
def pause():
    playlist.is_playing = False
    return jsonify({'message': 'Paused'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    tracks = playlist.search(query)
    return jsonify([{'path': t.path, 'title': t.title} for t in tracks])

@app.route('/shuffle', methods=['POST'])
def shuffle_playlist():
    playlist.shuffle()
    return jsonify({'message': 'Playlist shuffled'})

@app.route('/clear', methods=['POST'])
def clear_playlist():
    playlist.clear()
    return jsonify({'message': 'Playlist cleared'})
@app.route('/set_current/<int:track_index>', methods=['POST'])
def set_current(track_index):
    playlist.set_current_to_index(track_index)
    return jsonify({'message': 'Current set'})

@app.route('/move/<int:from_index>/<int:to_index>', methods=['POST'])
def move_track(from_index, to_index):
    playlist.move(from_index, to_index)
    return jsonify({'message': 'Track moved'})

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for Docker and monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'PlayerPro',
        'version': '1.0.0'
    }), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        url = f'/uploads/{filename}'
        title = os.path.splitext(file.filename)[0]
        return jsonify({'url': url, 'title': title})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/downloads/<filename>')
def downloaded_file(filename):
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

# YouTube Integration Routes
@app.route('/youtube/search', methods=['GET'])
def youtube_search():
    query = request.args.get('q', '')
    max_results = request.args.get('max_results', 10, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    results = youtube.search_youtube(query, max_results)
    return jsonify(results)

@app.route('/youtube/info', methods=['POST'])
def youtube_info():
    data = request.json
    video_url = data.get('url', '')
    
    if not video_url:
        return jsonify({'error': 'URL required'}), 400
    
    info = youtube.get_video_info(video_url)
    return jsonify(info)

@app.route('/youtube/download', methods=['POST'])
def youtube_download():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        video_url = data.get('url', '')
        print(f"🎵 Download request for URL: {video_url}")
        
        if not video_url:
            return jsonify({'error': 'URL required'}), 400
        
        result = youtube.download_audio(video_url)
        print(f"📥 Download result: {result}")
        
        if result.get('success'):
            # Agregar automáticamente a la playlist
            track = Track(
                path=f'/downloads/{result["filename"]}',
                title=f'{result["title"]} - {result["artist"]}'
            )
            playlist.append(track)
            save_playlist()
            
            return jsonify({
                'success': True,
                'message': 'Downloaded and added to playlist',
                'track': {
                    'path': track.path,
                    'title': track.title
                }
            })
        else:
            error_msg = result.get('error', 'Unknown download error')
            
            # Detectar errores de bot detection y proporcionar mensajes más útiles
            if any(keyword in error_msg.lower() for keyword in ['bot detection', 'sign in', 'authentication', 'cookies']):
                return jsonify({
                    'success': False,
                    'error': 'YouTube está bloqueando las descargas temporalmente debido a detección de bots. Esto es normal en servidores de producción.',
                    'error_type': 'bot_detection',
                    'suggestion': 'Intenta de nuevo en unos minutos o usa la función de búsqueda para encontrar contenido alternativo.',
                    'info': result.get('info', {})
                }), 429  # Too Many Requests
            else:
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'error_type': 'download_error'
                }), 400
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error in youtube_download: {e}")
        
        # Detectar errores de bot detection en excepciones
        if any(keyword in error_msg.lower() for keyword in ['bot', 'sign in', 'authentication', 'cookies']):
            return jsonify({
                'success': False,
                'error': 'YouTube requiere autenticación debido a detección de bots. Esto es una restricción temporal.',
                'error_type': 'bot_detection',
                'suggestion': 'Intenta de nuevo más tarde.'
            }), 429
        
        return jsonify({
            'success': False,
            'error': f'Server error: {error_msg}',
            'error_type': 'server_error'
        }), 500

@app.route('/youtube/add_url', methods=['POST'])
def add_youtube_url():
    """Agregar una URL de YouTube directamente sin descargar"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        video_url = data.get('url', '')
        print(f"Add URL request for: {video_url}")
        
        if not video_url:
            return jsonify({'error': 'URL required'}), 400
        
        # Obtener información del video
        try:
            info = youtube.get_video_info(video_url)
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error obteniendo información del video: {str(e)}'
            }), 500

        if 'error' in info:
            # Sanitize error message to avoid Unicode encoding issues
            error_msg = info['error']
            try:
                error_msg.encode('utf-8')
            except UnicodeEncodeError:
                error_msg = 'Error procesando información del video (caracteres especiales)'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Advertir si el video puede tener problemas de reproducción
        warning_message = None
        if info.get('is_live'):
            warning_message = 'Este es un video en vivo, puede tener problemas de reproducción'
        elif info.get('availability') not in ['public', 'unlisted']:
            warning_message = f'Video con disponibilidad: {info.get("availability")}'
        
        # Crear track con URL de YouTube
        # Sanitize title and uploader to avoid Unicode issues
        title = info.get("title", "Unknown")
        uploader = info.get("uploader", "Unknown")
        try:
            title.encode('utf-8')
            uploader.encode('utf-8')
        except UnicodeEncodeError:
            title = "Título con caracteres especiales"
            uploader = "Artista desconocido"

        track = Track(
            path=video_url,  # Guardar la URL directamente
            title=f'{title} - {uploader}'
        )
        
        playlist.append(track)
        save_playlist()
        
        response_data = {
            'success': True,
            'message': 'YouTube video added to playlist',
            'track': {
                'path': track.path,
                'title': track.title
            }
        }
        
        if warning_message:
            response_data['warning'] = warning_message
        
        return jsonify(response_data)
        
    except Exception as e:
        error_msg = str(e)
        # Handle Unicode encoding issues in Windows
        try:
            print(f"Error in add_youtube_url: {error_msg}")
        except UnicodeEncodeError:
            print("Error in add_youtube_url: Unicode encoding error in error message")
        return jsonify({
            'success': False,
            'error': 'Server error: Error procesando la información del video'
        }), 500


@app.route('/youtube/test', methods=['GET'])
def test_youtube():
    """Endpoint de prueba para verificar la funcionalidad de YouTube"""
    try:
        # Probar búsqueda simple
        results = youtube.search_youtube("test music", 2)
        
        return jsonify({
            'success': True,
            'message': 'YouTube integration working',
            'api_key_configured': bool(youtube.api_key),
            'results_count': len(results),
            'sample_results': results[:1] if results else []
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'api_key_configured': bool(youtube.api_key)
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)