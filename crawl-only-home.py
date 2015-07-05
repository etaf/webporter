#!/usr/bin/env python
# encoding: utf-8
import threading
import time
from webporter import  Proxy
proxy = Proxy()
def visit_house_by_id_range(thread_id, min_zillow_id, max_zillow_id):
    global mutex
    global exit_flag
    pre_url = 'http://www.zillow.com/homedetails/'
    for i in xrange(min_zillow_id, max_zillow_id):
        if exit_flag:
            print "Thread %d:exiting.." % thread_id
            return
        target_url = pre_url + "%d_zpid/" % i
        print "****thread %d processing: %s" % (thread_id, target_url)
        target_page = proxy.get_from_db(target_url)
        if(target_page == None):
            #in_db = False
            page = proxy.crawler.get_page_html(target_url)
            new_page = page.replace(proxy.proxy_target_url, "")
            if new_page != "":
                #lock
                mutex.acquire()
                print "*****saving content of:", target_url
                proxy.save_to_db(target_url, new_page)
                mutex.release()
                #unlock


def main(thread_num):
    global mutex
    global exit_flag
    exit_flag = False
    mutex = threading.Lock()
    threads = []
    start_id = 1
    id_range = 100000
    thread_id = 0
    for i in xrange(thread_num):
        thread_id = thread_id + 1
        threads.append(threading.Thread(target = visit_house_by_id_range, args=(thread_id, start_id, start_id + id_range)))
        start_id = start_id + id_range
    for t in threads:
        t.daemon = True
        t.start()

    while len(threads) > 0 :
        try:
            time.sleep(1)
            #threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            exit_flag  = True
            print "Ctrl-c received! Sending kill to threads..."
            break;

    for t in threads:
        t.join()
if __name__ == '__main__':
    main(6)
