import threading
import time

def one(o):
    for i in range(o):
        print('one:'+str(i))
        time.sleep(1)

def two(t):
    for j in range(t):
        print('two:'+str(j))
        time.sleep(1)


t1 = threading.Thread(target=one,args=(10,))
t2 = threading.Thread(target=two,args=(10,))
t1.start()
t2.start()