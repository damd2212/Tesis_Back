#!/usr/bin/env bash
# Exit on error
set -o errexit


pip install -r requirements.txt
ls -l "/opt/render/project/src"
sed -i 's/if __name__ == '\''__main__'\'':/if __name__ == '\''__main__'\'':\n    from src.TesisApp.columnExtractor import ColumnExtractor/' /opt/render/project/src/.venv/bin/gunicorn
cat /opt/render/project/src/.venv/bin/gunicorn

python manage.py collectstatic --no-input
python manage.py migrate

