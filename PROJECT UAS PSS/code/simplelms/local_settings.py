from django.conf import settings
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

# KITA NONAKTIFKAN BARIS INI KARENA 'core' SUDAH ADA DI SETTINGS.PY UTAMA
# settings.INSTALLED_APPS += [
#     'core',
# ]

# Gunakan PostgreSQL jika ada di lingkungan Docker, 
# jika tidak, biarkan pakai SQLite bawaan settings.py
if os.environ.get('DB_HOST') == 'postgres' or os.environ.get('DOCKER_ENV'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'simple_lms',
            'USER': 'simple_user',
            'PASSWORD': 'simple_password',
            'HOST': 'simple_db',
        }
    }