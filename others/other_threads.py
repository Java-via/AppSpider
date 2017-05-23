# _*_ coding: utf-8 _*_

"""
other_threads.py by xianhu
"""

import time
import queue
import logging
import threading
import urllib.request
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

g_url_queue = queue.Queue()
g_save_queue = queue.Queue()


def url_fetch_func(name):
    """
    url fetch function
    """
    logging.debug("url_fetch_func name=%s start", name)
    while g_url_queue.qsize() > 0 or g_save_queue.qsize() > 0:
        try:
            url = g_url_queue.get(timeout=10)
            logging.debug("url_fetch_func name=%s fetch_url=%s", name, url)
            g_save_queue.put(urllib.request.urlopen(url).geturl())
            time.sleep(1)
        except:
            pass
    logging.debug("url_fetch_func name=%s exit", name)
    return


def save_items_func(name):
    """
    save items function
    """
    logging.debug("save_items_func name=%s start", name)
    while True:
        logging.debug("save_items_func name=%s save_url=%s", name, g_save_queue.get())
        time.sleep(1)
        if g_save_queue.qsize() == 0 and g_url_queue.qsize() == 0:
            break
    logging.debug("save_items_func name=%s exit", name)
    return


if __name__ == '__main__':
    for i in range(1, 21):
        g_url_queue.put(item="http://zhushou.360.cn/list/index/cid/2?page=%d" % i)

    threads = [threading.Thread(target=url_fetch_func, args=(str(i),)) for i in range(2)]
    threads.append(threading.Thread(target=save_items_func, args=("save",)))

    for th in threads:
        th.setDaemon(True)
        th.start()

    for th in threads:
        if th.is_alive():
            th.join()

    exit()
