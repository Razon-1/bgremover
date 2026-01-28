#!/bin/bash
# Build script for Render

set -o errexit

# Install Python dependencies
pip install -r backend/requirements.txt

# Run Django migrations
python backend/manage.py migrate

# Collect static files
python backend/manage.py collectstatic --no-input
