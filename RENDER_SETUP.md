# 🚀 PlayerPro - Configuración para Render

## ✅ Archivos de configuración creados:

### 1. **render.yaml** - Configuración principal
- Servicio web Python configurado
- Plan gratuito
- Variables de entorno definidas
- Disco persistente para descargas

### 2. **requirements.txt** - Dependencias actualizadas
- Flask y Flask-CORS
- yt-dlp para descargas de YouTube
- gunicorn para producción
- Todas las dependencias necesarias

### 3. **Dockerfile** - Containerización
- Imagen Python 3.11
- FFmpeg instalado
- Health checks configurados
- Optimizado para producción

### 4. **start.sh** - Script de inicio
- Creación de directorios
- Configuración de permisos
- Inicio con gunicorn

### 5. **.env.production** - Variables de entorno
- Configuración de producción
- Plantilla para variables sensibles

## 🔧 Pasos para desplegar:

### 1. Subir a GitHub
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### 2. Conectar a Render
1. Ve a [render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Selecciona "Web Service"
4. Render detectará automáticamente el `render.yaml`

### 3. Configurar variables de entorno
En el dashboard de Render, configura:
- `YOUTUBE_API_KEY`: Tu clave de API de YouTube
- `SECRET_KEY`: Una clave secreta segura
- Las demás se configuran automáticamente

### 4. Configurar dominio personalizado
- En Settings → Custom Domains
- Agregar: `playerpro.onrender.com`

## 🎯 Características incluidas:

✅ **Sistema de proxies rotativos** - Evita bloqueos de IP
✅ **Gestión de sesiones** - Persistencia de cookies
✅ **Anti-detección** - Múltiples configuraciones de user-agent
✅ **Producción ready** - Gunicorn + configuración optimizada
✅ **Health checks** - Monitoreo automático
✅ **Auto-deploy** - Despliegue automático desde GitHub

## 📝 Notas importantes:

- **Plan gratuito**: 750 horas/mes, suficiente para uso personal
- **Limitaciones**: CPU y memoria limitadas en plan gratuito
- **Almacenamiento**: Archivos temporales, se limpian automáticamente
- **API Key**: Necesaria para búsquedas de YouTube

## 🔍 URL final:
Una vez desplegado, tu aplicación estará disponible en:
**https://playerpro.onrender.com**

¡Tu PlayerPro está listo para producción! 🎵