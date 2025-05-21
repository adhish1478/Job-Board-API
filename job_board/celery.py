import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')

app= Celery('job_board')

# ✅ Explicitly set broker (sometimes settings aren't picked up otherwise)
app.conf.broker_url = 'redis://localhost:6379/0'

app.config_from_object('django.conf:settings', namespace= 'CELERY')
app.autodiscover_tasks()

