# Despliegue en Render - PlayerPro

## Configuración para playerpro.onrender.com

### Pasos para el despliegue:

1. **Conectar repositorio a Render:**
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - Conecta tu repositorio de GitHub
   - Selecciona "Web Service"

2. **Configuración del servicio:**
   - **Name:** playerpro
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT backend:app`
   - **Plan:** Free (o el que prefieras)

3. **Variables de entorno requeridas:**
   ```
   FLASK_ENV=production
   SECRET_KEY=[generar una clave secreta]
   YOUTUBE_API_KEY=[tu clave de API de YouTube]
   PORT=10000
   ```

4. **Configuración de dominio personalizado:**
   - En el dashboard de Render, ve a Settings
   - En "Custom Domains", agrega: `playerpro.onrender.com`

### Archivos de configuración incluidos:

- `render.yaml` - Configuración automática para Render
- `Dockerfile` - Para despliegue containerizado
- `start.sh` - Script de inicio
- `.env.production` - Variables de entorno de producción
- `requirements.txt` - Dependencias actualizadas

### Características del despliegue:

✅ **Proxy rotation** - Sistema de rotación de proxies para evitar bloqueos
✅ **Session management** - Gestión de sesiones con persistencia de cookies
✅ **Anti-detection** - Múltiples configuraciones para evitar detección
✅ **Production ready** - Configurado con Gunicorn para producción
✅ **Health checks** - Monitoreo de salud del servicio
✅ **Auto-deploy** - Despliegue automático desde GitHub

### Notas importantes:

- El plan gratuito de Render tiene limitaciones de CPU y memoria
- Los archivos descargados se almacenan temporalmente
- Se recomienda configurar un dominio personalizado para mejor rendimiento
- Asegúrate de tener una API key válida de YouTube

### Troubleshooting:

Si hay problemas con el despliegue:
1. Verifica que todas las variables de entorno estén configuradas
2. Revisa los logs en el dashboard de Render
3. Asegúrate de que el repositorio esté actualizado
4. Verifica que la API key de YouTube sea válida