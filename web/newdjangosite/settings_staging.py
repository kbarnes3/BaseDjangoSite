from settings_base import *

#Settings for running a local development server using runserver

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'newdjangosite-staging',                    # Or path to database file if using sqlite3.
        'USER': 'newdjangosite-user',
        'PASSWORD': 'passwordgoeshere',
        'HOST': 'localhost',             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

ALLOWED_HOSTS = ['staging.newdjangosite.com']

STATIC_ROOT = '/var/www/newdjangosite-staging/static'

