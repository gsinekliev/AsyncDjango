import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse, HttpRequest
from tasks import call_external_api, call_external_api_celery, a_call_external_api, error_handler
import requests
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


def sync_handler(request: HttpRequest):
    start_time = time.monotonic()
    call_external_api()
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


def celery_handler(request):
    start_time = time.monotonic()
    call_external_api_celery.apply_async((), link_error=error_handler.s())
    #call_external_api_celery.delay()
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


def thread_handler(request: HttpRequest):
    logger.info("Request for thread received")
    start_time = time.monotonic()
    future = thread_pool.submit(call_external_api)
    future.add_done_callback(on_complete)
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


async def async_handler(request: HttpRequest):
    logger.info("Request for async_handler received")
    start_time = time.monotonic()
    asyncio.create_task(a_call_external_api())
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")


async def async_with_threads(request: HttpRequest):
    logger.info("Request for async_handler received")
    start_time = time.monotonic()
    asyncio.create_task(sync_to_async(sync_sleep, executor=thread_pool)())
    end_time = time.monotonic()
    return HttpResponse(f"Hello, world. This page loaded in {end_time - start_time} seconds\n")