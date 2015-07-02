#!/usr/bin/env python
# encoding: utf-8
from webporter import  Proxy
from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
#start_url = "/browse/homes/ok/"
start_url = "/"
q = Queue()
proxy = Proxy()

def do_work(url):

    target_url = urlparse.urljoin(proxy.proxy_target_url, url)
    print "processing: ", target_url
    (page, in_db) = proxy.get_page(target_url)
    if page == "" or in_db:
        return
    #get_all urls_from_page:
    soup = BeautifulSoup(page)
    links = soup.find_all('a')
    for tag in links:
        link = tag.get('href',None)
        if (link is not None) and (len(link) > 0) and(link[0] == '/') :
            q.put(link)

def woker():
    q.put(start_url)
    while not q.empty():
        url = q.get()
        do_work(url)
        q.task_done()

    print "Finished!"

def main():
    q.put(start_url)
    woker()


if __name__ =="__main__":
    main()
