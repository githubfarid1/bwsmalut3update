#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port 5005..."
exec gunicorn --config gunicorn-cfg.py core.wsgi