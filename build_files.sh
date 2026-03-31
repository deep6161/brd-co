#!/usr/bin/env bash

# Install dependencies
pip install -r requirements.txt

# Collect static files into staticfiles_build
python manage.py collectstatic --no-input

# Create the output directory that Vercel expects
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/

# Run migrations
python manage.py migrate --no-input

# Create superuser if env vars are set
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --no-input || true
fi
