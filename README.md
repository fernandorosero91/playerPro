# 🎵 Reproductor Musical Pro

Un reproductor de música profesional desarrollado en Python y JavaScript que implementa **listas doblemente enlazadas** para la gestión eficiente de playlists, con integración completa de **YouTube**.

![Reproductor Musical Pro](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)
![YouTube](https://img.shields.io/badge/YouTube-API-red.svg)

## 🚀 Características Principales

### 🎯 **Estructura de Datos**
- ✅ **Lista Doblemente Enlazada** implementada desde cero
- ✅ **Operaciones O(1)** para inserción y eliminación
- ✅ **Navegación bidireccional** eficiente
- ✅ **Gestión de memoria** optimizada

### 🎨 **Interfaz Profesional**
- ✅ **Diseño moderno** con glassmorphism
- ✅ **Botón de reproducción** con anillos concéntricos animados
- ✅ **Efectos visuales** y transiciones suaves
- ✅ **Responsive design** adaptativo
- ✅ **Tema oscuro** profesional

### 🎵 **Funcionalidades de Audio**
- ✅ **Reproducción local** de archivos MP3, WAV, OGG, FLAC
- ✅ **Controles completos** (play, pause, next, prev, shuffle, repeat)
- ✅ **Control de volumen** con slider visual
- ✅ **Barra de progreso** interactiva
- ✅ **Información dinámica** de pistas

### 🔴 **Integración con YouTube**
- ✅ **Búsqueda en tiempo real** en YouTube
- ✅ **Descarga de audio** automática
- ✅ **Añadir URLs** directamente
- ✅ **Miniaturas** y metadatos
- ✅ **Gestión de calidad** de audio

### 📱 **Funcionalidades Avanzadas**
- ✅ **Búsqueda local** en playlist
- ✅ **Drag & Drop** para reordenar
- ✅ **Persistencia** de datos
- ✅ **API REST** completa
- ✅ **Scroll personalizado**

## 🛠️ Instalación

### **Paso 1: Instalación Básica**
```bash
# Clonar el repositorio
git clone [tu-repositorio]
cd reproductor-musical-pro

# Ejecutar instalador automático
python install.py
```

### **Paso 2: Configurar YouTube API (Opcional pero Recomendado)**

#### **2.1 Crear API Key de YouTube:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo o selecciona uno existente
3. Habilita **"YouTube Data API v3"**:
   - Ve a **"APIs y servicios" > "Biblioteca"**
   - Busca **"YouTube Data API v3"**
   - Haz clic en **"HABILITAR"**
4. Crear credenciales:
   - Ve a **"APIs y servicios" > "Credenciales"**
   - Haz clic en **"+ CREAR CREDENCIALES"**
   - Selecciona **"Clave de API"**
   - Copia la clave generada

#### **2.2 Configurar en el Proyecto:**
```bash
# Ejecutar configurador automático
python setup_youtube.py

# O crear manualmente el archivo .env
cp .env.example .env
# Editar .env y agregar tu API Key
```

### **Paso 3: Ejecutar el Proyecto**
```bash
# Iniciar servidor
python backend.py

# Abrir en navegador
# http://localhost:5000
```

### **Instalación Manual (Avanzada)**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear directorios
mkdir uploads downloads static

# Configurar variables de entorno
echo "YOUTUBE_API_KEY=tu_api_key_aqui" > .env

# Ejecutar servidor
python backend.py
```

## 🎯 Uso

1. **Iniciar el servidor:**
   ```bash
   python backend.py
   ```

2. **Abrir en navegador:**
   ```
   http://localhost:5000
   ```

3. **Funcionalidades disponibles:**
   - 📁 **Subir archivos locales**
   - 🔍 **Buscar en YouTube**
   - ⬇️ **Descargar desde YouTube**
   - 🎵 **Reproducir música**
   - 📝 **Gestionar playlist**

## 🏗️ Arquitectura del Proyecto

### **Backend (Python + Flask)**
```
backend.py              # Servidor principal
youtube_integration.py  # Módulo de YouTube
requirements.txt        # Dependencias
```

### **Frontend (HTML + CSS + JavaScript)**
```
index.html             # Interfaz principal
static/               # Archivos estáticos
```

### **Estructura de Datos**
```python
class DoublyLinkedPlaylist:
    def __init__(self):
        self.head = None      # Primer nodo
        self.tail = None      # Último nodo
        self.current = None   # Nodo actual
        self.length = 0       # Tamaño de la lista
```

## 🔧 API Endpoints

### **Playlist Management**
- `GET /playlist` - Obtener playlist completa
- `POST /add` - Añadir canción
- `DELETE /remove` - Eliminar canción
- `POST /move/{from}/{to}` - Mover canción

### **Playback Control**
- `GET /current` - Canción actual
- `POST /play` - Reproducir
- `POST /pause` - Pausar
- `POST /next` - Siguiente
- `POST /prev` - Anterior

### **YouTube Integration**
- `GET /youtube/search` - Buscar en YouTube
- `POST /youtube/download` - Descargar audio
- `POST /youtube/add_url` - Añadir URL directa
- `POST /youtube/info` - Información de video

## 🎨 Tecnologías Utilizadas

### **Backend**
- **Python 3.8+** - Lenguaje principal
- **Flask 2.3+** - Framework web
- **yt-dlp** - Descarga de YouTube
- **Flask-CORS** - Manejo de CORS

### **Frontend**
- **HTML5** - Estructura
- **CSS3** - Estilos y animaciones
- **JavaScript ES6+** - Lógica del cliente
- **Tailwind CSS** - Framework de estilos
- **Font Awesome** - Iconografía

### **Audio**
- **HTML5 Audio API** - Reproducción
- **Web Audio API** - Controles avanzados

## 📊 Complejidad Algorítmica

| Operación | Complejidad | Descripción |
|-----------|-------------|-------------|
| Insertar al inicio | O(1) | Prepend |
| Insertar al final | O(1) | Append |
| Insertar en posición | O(n) | Insert at index |
| Eliminar nodo | O(1) | Remove node |
| Buscar por índice | O(n) | Node at index |
| Siguiente/Anterior | O(1) | Navigation |

## 🔒 Características de Seguridad

- ✅ **Validación de archivos** subidos
- ✅ **Sanitización de URLs** de YouTube
- ✅ **Manejo de errores** robusto
- ✅ **CORS configurado** correctamente
- ✅ **Límites de tamaño** de archivo

## 🛠️ Solución de Problemas con YouTube

### ❌ **Error 150: "Video no permite reproducción embebida"**
Este error ocurre cuando el video tiene restricciones de reproducción embebida.

**Soluciones:**
1. **Descargar el audio**: Usa el botón "Descargar" en lugar de "Añadir URL"
2. **Probar otro video**: Algunos videos tienen estas restricciones
3. **Verificar disponibilidad**: Videos privados o bloqueados no funcionarán

### ❌ **Error 400: "Bad Request"**
Indica problemas con la API de YouTube.

**Soluciones:**
```bash
# Actualizar yt-dlp
pip install --upgrade yt-dlp

# Verificar URL válida
# Reiniciar servidor
python backend.py
```

### 🚫 **Videos que no se reproducen**
**Tipos de videos problemáticos:**
- Videos privados o eliminados
- Videos con restricciones geográficas
- Videos en vivo (pueden tener problemas)
- Videos con derechos de autor estrictos

**Recomendaciones:**
- Usa videos públicos y populares
- Prueba con música oficial de artistas
- Los videos de Creative Commons suelen funcionar mejor

### 🔧 **Comandos de Diagnóstico**
```bash
# Probar las mejoras
python test_youtube_fix.py

# Actualizar yt-dlp
pip install --upgrade yt-dlp

# Verificar dependencias
pip list | grep -E "(yt-dlp|google-api)"

# Verificar servidor
curl http://localhost:5000/playlist
```

### 💡 **Consejos de Uso**
- El reproductor maneja automáticamente errores de YouTube
- Los videos bloqueados se saltan automáticamente
- Se muestran advertencias para videos problemáticos
- Fallback automático entre diferentes métodos de reproducción

## 🚀 Funcionalidades Futuras

- 🎚️ **Ecualizador visual**
- 🎨 **Temas personalizables**
- 📱 **App móvil nativa**
- 🔊 **Efectos de audio**
- 📊 **Estadísticas de reproducción**
- 🎵 **Recomendaciones inteligentes**

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- **YouTube** por su API pública
- **yt-dlp** por la excelente librería
- **Flask** por el framework web
- **Tailwind CSS** por los estilos

---

⭐ **¡Dale una estrella si te gustó el proyecto!** ⭐