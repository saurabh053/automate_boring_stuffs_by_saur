import os

from celery import Celery

# Tell Celery where Django settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "awd_main.settings")

app = Celery("awd_main")

# Read Celery settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks.py from all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignored_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")