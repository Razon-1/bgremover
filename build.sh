#!/bin/bash

# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
cd backend
python manage.py migrate
cd ..

# Collect static files
cd backend
python manage.py collectstatic --noinput
cd ..
