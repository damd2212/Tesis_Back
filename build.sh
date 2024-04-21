#!/usr/bin/env bash
# Exit on error
set -o errexit


pip install -r requirements.txt

ruta="/opt/render/project/src"
ls -l $ruta

# Aquí definimos la ruta que queremos revisar
cat /opt/render/project/src/.venv/bin/gunicorn

python manage.py collectstatic --no-input
python manage.py migrate

