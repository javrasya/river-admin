import django_heroku

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "river-admin-demo.herokuapp.com", "demo.riveradminproject.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USERNAME"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DATABASE_URL"),
        'PORT': '5432'
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

django_heroku.settings(locals())
