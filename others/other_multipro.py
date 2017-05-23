# _*_ coding: utf-8 _*_

"""
other_multipro.py by xianhu
"""

import time
import threading
import multiprocessing

g_queue = multiprocessing.Queue()


def start_thread(index=0):
    print("thread[index=%s, name=%s, empty=%s] start" % (index, threading.current_thread().name, g_queue.empty()))
    while not g_queue.empty():
        time.sleep(1)
        try:
            data = g_queue.get(block=True, timeout=1)
            print("thread[index=%s, name=%s, data=%s]" % (index, threading.current_thread().name, data))
        except Exception as excep:
            print("thread[index=%s, name=%s, error=%s]" % (index, threading.current_thread().name, str(excep)))
    print("thread[index=%s, name=%s, empty=%s] end" % (index, threading.current_thread().name, g_queue.empty()))
    return


def start_process(index=0):
    test_list = list(range(10000))
    print("process[index=%s, name=%s, empty=%s] start" % (index,  multiprocessing.current_process().name, g_queue.empty()))
    while not g_queue.empty():
        count = 0
        for i in range(10000):
            count += pow(3*2, 3*2) if i in test_list else 0
        try:
            data = g_queue.get(block=True, timeout=1)
            print("process[index=%s, name=%s, data=%s]" % (index, multiprocessing.current_process().name, data))
        except Exception as excep:
            print("process[index=%s, name=%s, error=%s]" % (index, threading.current_thread().name, str(excep)))
    print("process[index=%s, name=%s, empty=%s] end" % (index,  multiprocessing.current_process().name, g_queue.empty()))
    return index


def init_queue():
    print("init g_queue start......")
    while not g_queue.empty():
        g_queue.get()
    for _index in range(10):
        g_queue.put(_index)
    time.sleep(0.1)
    print("init g_queue end, empty=%s" % g_queue.empty())
    return


if __name__ == '__main__':
    print("cpu count:", multiprocessing.cpu_count(), "\n")

    print("threading: no threading, start time:", time.time())
    init_queue()
    start_thread()
    print("threading: no threading, end time:", time.time())
    print("\n")

    print("threading: simple threading, start time:", time.time())
    init_queue()
    t_list = [threading.Thread(target=start_thread, args=(i,)) for i in range(5)]
    for t in t_list:
        t.start()
    for t in t_list:
        if t.is_alive():
            t.join()
    print("threading: simple threading, end time:", time.time())
    print("\n")

    print("multiprocess: no multiprocess, start time:", time.time())
    init_queue()
    start_process()
    print("multiprocess: no multiprocess, end time:", time.time())
    print("\n")

    print("multiprocess: simple multiprocess, start time:", time.time())
    init_queue()
    p_list = [multiprocessing.Process(target=start_process, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in p_list:
        p.start()
    for p in p_list:
        if p.is_alive():
            p.join()
    print("multiprocess: simple multiprocess, end time:", time.time())
    print("\n")

    print("multiprocess: multiprocess pool, start time:", time.time())
    init_queue()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = [pool.apply_async(start_process, args=(i,)) for i in range(multiprocessing.cpu_count())]
    pool.close()
    pool.join()
    print([item.get() for item in result])
    print("multiprocess: multiprocess pool, end time:", time.time())
    print("\n")

    print("threading and multiprocess, start time:", time.time())
    init_queue()
    p_list = [multiprocessing.Process(target=start_process, args=(i,)) for i in range(multiprocessing.cpu_count())]
    for p in p_list:
        p.start()
    t_list = [threading.Thread(target=start_thread, args=(i,)) for i in range(5)]
    for t in t_list:
        t.start()

    for p in p_list:
        if p.is_alive():
            p.join()
    for t in t_list:
        if t.is_alive():
            t.join()
    print("threading and multiprocess, end time:", time.time())

    exit()
