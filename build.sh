#!/usr/bin/env bash
# Render build script
# https://render.com/docs/deploy-django

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
