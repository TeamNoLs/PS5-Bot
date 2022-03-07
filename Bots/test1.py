import time
import multiprocessing


def check1():
    print('1 is starting...')
    time.sleep(5)
    print('1 is done...')

def check2():
    print('2 is starting...')
    time.sleep(5)
    print('2 is done...')

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=check1)
    p2 = multiprocessing.Process(target=check2)

    p1.start()
    p2.start()

   