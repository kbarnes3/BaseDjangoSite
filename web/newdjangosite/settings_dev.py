from settings_base import *

#Settings for running a local development server using runserver

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'newdjangosite-dev',                        # Or path to database file if using sqlite3.
        'USER': 'newdjangosite-dev-user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

STATIC_ROOT = '/var/www/newdjangosite-dev/static'

