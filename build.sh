#!/usr/bin/env bash
# Exit on error
set -o errexit


pip install -r requirements.txt

# Archivo original
archivo_original="/opt/render/project/src/.venv/bin/gunicorn"

# Patrón de búsqueda y reemplazo
patron_busqueda="from gunicorn.app.wsgiapp import run"
patron_reemplazo="from TesisApp.columnExtractor import ColumnExtractor\n\n\0"

# Editar el archivo usando sed
sed -i "s/$patron_busqueda/$patron_reemplazo/g" "$archivo_original"

python manage.py collectstatic --no-input
python manage.py migrate

