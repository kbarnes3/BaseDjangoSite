from settings_base import *

#Settings for running a local development server using runserver

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'newdjangosite.db',             # Or path to database file if using sqlite3.
    }
}
