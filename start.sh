#!/bin/bash

# Create necessary directories
mkdir -p uploads downloads sessions

# Set permissions
chmod 755 uploads downloads sessions

# Set default port if not provided (Render uses 10000 by default)
export PORT=${PORT:-10000}

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --worker-class sync backend:app