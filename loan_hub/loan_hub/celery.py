# loan_hub/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_hub.settings')

app = Celery('loan_hub')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule the task to run every minute
app.conf.beat_schedule = {
    'calculate-interest-every-minute': {
        'task': 'your_app_name.tasks.calculate_daily_interest',
        'schedule': crontab(),  # This runs the task every minute
    },
}


