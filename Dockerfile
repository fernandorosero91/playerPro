FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies in a single layer with minimal packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and set permissions in one step
RUN mkdir -p uploads downloads sessions static \
    && chmod 755 uploads downloads sessions static

# Expose port (Render will set PORT env var)
EXPOSE $PORT

# Health check with dynamic port
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=2 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Start command with dynamic port
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --worker-class sync backend:app"]