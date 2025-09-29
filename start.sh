#!/bin/bash

# Create necessary directories
mkdir -p uploads downloads sessions

# Set permissions
chmod 755 uploads downloads sessions

# Install system dependencies if needed
# apt-get update && apt-get install -y ffmpeg

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 backend:app