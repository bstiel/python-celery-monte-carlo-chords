import os
from celery import Celery


app = Celery(__name__)
app.conf.update({
    'broker_url': os.environ['CELERY_BROKER_URL'],
    'imports': ('tasks',),
    'result_backend': os.environ['CELERY_RESULT_BACKEND'],
    'result_persistent': False,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']})
