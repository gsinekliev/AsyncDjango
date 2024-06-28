# AsyncDjango

The goal of this projecte is to testing Asynchronous strategies with django

There are two types of tasks:
* CPU intensive task(log_to_file) - generates a 2MB string and writes to a file
* IO blocking - call external service on http://localhost:9000. Check out the simpleServer repo


The service uses several different approaches to execute these tasks
* sync
* async by using a threadpool
* async by using celery
* async by using asgi server and asyncio eventloop


## Set up celery
celery -A tasks worker -c 5 --loglevel=DEBUG

## set up UWSGI
uwsgi --ini .uwsgi/config.ini

## set up hypercorn(for asyncio tests)
We need the ulimit here, because asgi servers tend to keep more connections open, hence more sockets open
ulimit -n 2048 && hypercorn --port 8000 --loop asyncio --access-log logs/asgi.log djangoProject.asgi:application -w 4


## truncate all logs
truncate -s 0 curl_log.txt curl_error.txt log.txt logs/uwsgi.log logs/django.log logs/tasks.log logs/asgi.log ../simple-server/logs/access.log logs/celery.log

## benchmarking

We use apache benchmark tool. For example this will 
ab -n 2000 -c 4 http://127.0.0.1:8000/polls/call/sync






