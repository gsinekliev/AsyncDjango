import asyncio
import string
import time
import logging
from random import choices

import aiohttp
import requests

logger = logging.getLogger(__name__)
task_complete_logger = logging.getLogger("tasks")

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