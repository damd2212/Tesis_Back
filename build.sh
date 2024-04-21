#!/usr/bin/env bash
# Exit on error
set -o errexit


pip install -r requirements.txt

ruta="/opt/render/project/src/TesisApp"
ls -l $ruta

cat /opt/render/project/src/TesisApp/columnExtractor.py
# Aquí definimos la ruta que queremos revisar
echo "Contenido _________________"
cat /opt/render/project/src/.venv/bin/gunicorn

python manage.py collectstatic --no-input
python manage.py migrate

