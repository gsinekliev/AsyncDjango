
## Threads
ab -n 1000 -c 5 http://127.0.0.1:8000/polls/call/threads

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     0    9 103.4      0    1635
Waiting:        0    9 103.4      0    1635
Total:          0    9 103.4      1    1636


## Celery
ab -n 1000 -c 4 http://127.0.0.1:8000/polls/call/celery
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     1    4  36.1      1     547
Waiting:        0    4  36.1      1     547
Total:          1    4  36.1      1     547


## Asyncio
ab -n 1000 -c 4 http://127.0.0.1:8000/polls/call/async

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     2    4   1.9      4      27
Waiting:        2    4   1.9      3      27
Total:          3    4   1.9      4      28
