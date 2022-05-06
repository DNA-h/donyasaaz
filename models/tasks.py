from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0') #!

import os

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "proj.settings"

app = Celery('donyasaaz')

@app.task(bind=True)
def test():
    print('just a test')