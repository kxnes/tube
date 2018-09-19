SECRET_KEY = '_ve^f^b2fc@)t8=p3cm0iw8^ufj!smq7_08rd1na!6h272lt55'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '--DB_NAME--',
        'HOST': '--DB_HOST--',
        'PORT': '--DB_PORT--',
        'USER': '--DB_USER--',
        'PASSWORD': '--DB_PASSWORD--'
    }
}

YOUTUBE_API_KEY = '--YOUTUBE_API_KEY--'

REDIS = {
    'HOST': '--REDIS_HOST--',
    'PORT': '--REDIS_PORT--',
    'DB': '--REDIS_DB--',
    'PASSWORD': ''
}

CELERY_BROKER_URL = 'redis://{}:{}/{}'.format(REDIS['HOST'], REDIS['PORT'], REDIS['DB'])
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
