import requests
from celery import Celery
from random import choices
import string
import logging

app = Celery('tasks')
app.conf.broker_url = 'redis://localhost:6379/0'
#app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.task_ignore_result = True
app.conf.task_store_errors_even_if_ignored = True
app.conf.redis_max_connections = 10

app.autodiscover_tasks()

logger = logging.getLogger(__name__)



@app.task(name="call_external_api", task_ignore_result=True)
def call_external_api_celery():
    connect_timeout, read_timeout = 5.0, 30.0
    get = requests.get('http://localhost:9000/', timeout=(connect_timeout, read_timeout))
    body = get.content
    #task_complete_logger.info(f"Received {body} from external api")


@app.task(name="log_to_file", task_ignore_result=True)
def log_to_file():
    with open('log.txt', 'a+') as f:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=2 * 10**6)) + '\n'
        f.write(random_string)


@app.task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))


