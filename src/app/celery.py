import os
import celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = celery.Celery('keywords')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
