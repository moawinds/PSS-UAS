from django.conf import settings
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

# KITA NONAKTIFKAN BARIS INI KARENA 'core' SUDAH ADA DI SETTINGS.PY UTAMA
# settings.INSTALLED_APPS += [
#     'core',
# ]

import dj_database_url

# Gunakan DATABASE_URL jika didefinisikan (misalnya di Render/Production)
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=False)
    }
# Gunakan PostgreSQL jika ada di lingkungan Docker lokal
elif os.environ.get('DB_HOST') == 'postgres' or os.environ.get('DOCKER_ENV'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'simple_lms',
            'USER': 'simple_user',
            'PASSWORD': 'simple_password',
            'HOST': 'simple_db',
        }
    }