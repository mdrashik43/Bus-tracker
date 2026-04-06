import os
import dj_database_url
from .settings import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-build-only')
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'bustracker.wsgi.application'
ASGI_APPLICATION = 'bustracker.asgi.application'

CSRF_TRUSTED_ORIGINS = ['https://bustracker-production-4469.up.railway.app']

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'