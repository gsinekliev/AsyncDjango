import asyncio
import time

import aiohttp
import requests
from celery import Celery
from random import random, choices
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
task_complete_logger = logging.getLogger("tasks")


@app.task(name="log_to_file", task_ignore_result=True)
def log_to_file():
    with open('log.txt', 'a+') as f:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=2 * 10**6)) + '\n'
        f.write(random_string)


@app.task(name="call_external_api", task_ignore_result=True)
def call_external_api_celery():
    connect_timeout, read_timeout = 5.0, 30.0
    get = requests.get('http://localhost:9000/', timeout=(connect_timeout, read_timeout))
    body = get.content
    task_complete_logger.info(f"Received {body} from external api")


@app.task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error('Task {0} raised exception: {1!r}\n{2!r}'.format(
          request.id, exc, traceback))


def log_to_file_no_celery():
    logger.info("Log to file no celery called")
    with open('log.txt', 'a+') as f:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=2 * 10**6)) + '\n'
        logger.info("Random string generated")
        f.write(random_string)

###############################################


def call_external_api():
    get = requests.get('http://localhost:9000/')
    body = get.content
    task_complete_logger.info("Received {body} from external api")


async def a_call_external_api():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:9000') as resp:
            body = await resp.text()
            task_complete_logger.info(f"Received {body} from external api")


async def async_sleep():
    await asyncio.sleep(1)
    task_complete_logger.info("Async Sleep complete")


def sync_sleep():
    time.sleep(2)
    task_complete_logger.info("Sync sleep complete")