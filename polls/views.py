import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse, HttpRequest
from tasks import log_to_file
from helpers import log_to_file_no_celery, async_sleep, sync_sleep

import time

from concurrent.futures import Future
import logging


logger = logging.getLogger(__name__)

thread_pool = ThreadPoolExecutor(max_workers=2)


def on_complete(future: Future):
    logger.info("Completed poll")
    if future._exception:
        logger.error("Exception during file write", future._exception)
    elif future._state != "FINISHED":
        logger.error(f"Future is {future._state}")


def celery_handler(request):
    start_time = time.monotonic()
    log_to_file.delay()
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


def sync_handler(request: HttpRequest):
    start_time = time.monotonic()
    log_to_file()
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


def thread_handler(request: HttpRequest):
    logger.info("Request for thread received")
    start_time = time.monotonic()
    future = thread_pool.submit(log_to_file_no_celery)
    future.add_done_callback(on_complete)
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


async def async_handler(request: HttpRequest):
    logger.info("Request for async_handler received")
    start_time = time.monotonic()
    asyncio.create_task(async_sleep())
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


async def async_with_threads(request: HttpRequest):
    logger.info("Request for async_handler received")
    start_time = time.monotonic()
    asyncio.create_task(sync_to_async(sync_sleep, executor=thread_pool)())
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")