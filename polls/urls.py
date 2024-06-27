from django.urls import path, include

from . import views, call_service_views

urlpatterns = [
    path("", views.celery_handler, name="index"),
    path("celery", views.celery_handler, name="index"),
    path("sync", views.sync_handler, name="index"),
    path("threads", views.thread_handler, name="index"),
    path("async", views.async_handler, name="index"),
    path("async_with_threads", views.async_with_threads, name="index"),

    path("call/sync", call_service_views.sync_handler, name="call_external_api"),
    path("call/threads", call_service_views.thread_handler, name="thread_handler"),
    path("call/async", call_service_views.async_handler, name="async_handler"),
    path("call/celery", call_service_views.celery_handler, name="celery_handler"),
]