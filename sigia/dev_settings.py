from __future__ import unicode_literals
from __future__ import absolute_import
import os
from easy_thumbnails.conf import Settings as thumbnail_settings
from django.contrib.messages import constants as messages
from datetime import timedelta
import djcelery

djcelery.setup_loader()

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    127: 'script',
}

# JS_MESSAGE = 127

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

SECRETARIA_EMAIL = 'secretaria@aitec.edu.ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



ALLOWED_HOSTS = []

LOGIN_URL = '/login/'

INTERNAL_IPS = ('127.0.0.1', '192.168.201.22')

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'floppyforms',
    'easy_thumbnails',
    'image_cropping',
    'captcha',
    'sigia',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
    #    'sigia.middleware.HttpPostTunnelingMiddleware',
    'sigia.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'sigia.urls'

WSGI_APPLICATION = 'sigia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'
        'NAME': 'sigia_dev',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'test.sqlite',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-EC'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

REPORT_SERVER = ""

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "sigia.context_processors.report_server",
            ],
            'debug': True,
        },
    },
]

# DEBUG_TOOLBAR_PANELS = [
#     'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]
#
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': 'ddt_request_history.panels.request_history.allow_ajax',
# }
#
# DEBUG_TOOLBAR_CONFIG = {
#     'RESULTS_STORE_SIZE': 100,
# }

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
BROKER_URL = 'amqp://sigia:Sigia*2015@192.168.201.6:5672/sigia'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Guayaquil'
CELERY_MESSAGE_COMPRESSION = 'gzip'
BROKER_TRANSPORT = 'amqplib'
BROKER_POOL_LIMIT = 3
BROKER_CONNECTION_MAX_RETRIES = 0
CELERY_TASK_RESULT_EXPIRES = 14400
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'hello-every-30-seconds': {
        'task': 'sigia.tasks.hello_celery',
        'schedule': timedelta(seconds=30),
        'args': ''
    },
}
