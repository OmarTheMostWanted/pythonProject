


import threading
import time

t1 = True

t2 = True

message = "message old"

threading.Thread

def thread1(name):
    print(" hello from 1" + name + "\n")

    while t1:
        time.sleep(2)
        global message
        print("thread 1" + name + " still going \n"  + message)
    print("1" + name + "died \n")

def thread2(name):
    print("hello from 2" + name)

    while t2:
        time.sleep(2)
        print("thread 2" + name + " still going" + "\n")

    print("2" + name + "died \n")




threading.Thread(target=thread1  , name="thread 1.1" , args=(".1", )).start()

threading.Thread(target=thread1  , name="thread 1.2" , args=(".2", )).start()

threading.Thread(target=thread2  , name="thread 2.1" , args=(".1", )).start()


input()
t1 = False



time.sleep(3)

t1 = True
threading.Thread(target=thread1  , name="thread 1.1" , args=(".1.1", )).start()


message = input("type new message")




