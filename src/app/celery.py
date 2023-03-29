import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app1 = Celery('app1')
app1.config_from_object('django.conf:settings', namespace='CELERY')
app1.autodiscover_tasks()
