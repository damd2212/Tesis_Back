#!/usr/bin/env bash
# Exit on error
set -o errexit


pip install -r requirements.txt


python manage.py collectstatic --no-input
python manage.py migrate

# Aquí definimos la ruta que queremos revisar
ruta="/opt/render/project/src/.venv/bin/gunicorn"

# Mostrar el contenido de la ruta
echo "Contenido de la ruta $ruta:"
ls -l $ruta