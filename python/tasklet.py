def foo():
    for n in range(5):
        print  "I am foo %d" %n
        yield

def bar():
    for n in range(5,7):
        print "I am bar %d" %n
        yield

def spam():
    for n in range(7,10):
        print "I am spam %d" %n
        yield

from collections import deque

taskqueue=deque()
taskqueue.append(spam())
taskqueue.append(bar())
taskqueue.append(foo())

while taskqueue :
    task=taskqueue.pop()
    try:
        next(task)
        taskqueue.appendleft(task)
    except StopIteration:
        pass
    
