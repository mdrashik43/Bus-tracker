#!/bin/bash
set -e

echo "=== Starting BusTracker ==="
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DATABASE_URL exists: $([ -n "$DATABASE_URL" ] && echo 'YES' || echo 'NO')"
echo "REDIS_URL exists: $([ -n "$REDIS_URL" ] && echo 'YES' || echo 'NO')"

echo "=== Running migrations ==="
python manage.py migrate --settings=bustracker.settings_production

echo "=== Creating superuser ==="
python manage.py createsuperuser --noinput --settings=bustracker.settings_production || true

echo "=== Testing ASGI import ==="
python -c "
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'bustracker.settings_production'
import django
django.setup()
print('Django setup OK')
from busapp.routing import websocket_urlpatterns
print('Routing import OK')
import bustracker.asgi
print('ASGI import OK')
" || { echo 'ASGI IMPORT FAILED - check above for error'; exit 1; }

echo "=== Starting Daphne ==="
exec daphne -v 2 -b 0.0.0.0 -p ${PORT:-8000} bustracker.asgi:application