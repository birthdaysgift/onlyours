import os

from celery import Celery

# This lets celery to work on windows
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Onlyours.settings')

app = Celery('Onlyours')
app.config_from_object('Onlyours.celeryconfig')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
