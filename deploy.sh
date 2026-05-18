#!/bin/bash
set -e

echo "=== Deploy exam_system ==="

git pull

source venv/bin/activate

pip install -r requirements.txt --quiet

python manage.py migrate --noinput

python manage.py collectstatic --noinput --clear

sudo systemctl restart exam-system

echo "=== Done ==="
