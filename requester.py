#!/usr/bin/env python
# encoding: utf-8
from webporter import  Proxy
from Queue import Queue
from bs4 import BeautifulSoup
import urlparse
import sys
import time

proxy = Proxy()
states = []
cities = []
zips = []

class Requester():
    q = Queue()
    max_depth = 5

    def request(self,search_type, citystatezip):
        with self.q.mutex:
            self.q.queue.clear()
        target_url = "/search/RealEstateSearch.htm?origplaceholdertext=&searchbar-type=%s&citystatezip=%s" % (search_type,"+".join(citystatezip.split()))
        self.q.put([target_url,0])
        while not self.q.empty():
            (url, depth) = self.q.get()
            if(depth <= self.max_depth):
                self.request_helper(url, depth)
                self.q.task_done()

    def request_helper(self, target_url, depth):
        target_url = urlparse.urljoin(proxy.proxy_target_url, target_url )
        print "****processing: ", target_url
        (page, in_db) = proxy.get_page(target_url)
        if page == "":
            return
        soup = BeautifulSoup(page)
        links = soup.find_all('a')
        for tag in links:
            link = tag.get('href',None)
            if (link is not None) and (len(link) > 1) and(link[0] == '/') and (link[1]!="/") and (depth <self.max_depth):
                self.q.put([link,depth+1])



def get_all_state():
    fp = open("states","w")
    target_url = "/browse/homes/"
    target_url = urlparse.urljoin(proxy.proxy_target_url, target_url)
    page = proxy.get_page(target_url)[0]
    soup = BeautifulSoup(page)
    for a in soup.find('div', attrs={'class':'zsg-lg-1-2 zsg-sm-1-1'}).findAll('a'):
        states.append([a.text, a['href']])
        fp.write(a.text+"\n")
    fp.close()

def get_all_city():
    fp = open("cities","w")
    for state in states:
        state_url = urlparse.urljoin(proxy.proxy_target_url, state[1])
        page = proxy.get_page(state_url)[0]
        soup = BeautifulSoup(page)
        for a in soup.find('div', attrs={'class':'zsg-lg-1-2 zsg-sm-1-1'}).findAll('a'):
            cities.append([a.text, a['href']])
            fp.write(a.text + "\n")
    fp.close()

def get_all_zip():
    fp = open("zips","w")
    for city in cities:
        city_url = urlparse.urljoin(proxy.proxy_target_url,city[1] )
        print "processing city:", city_url
        page = proxy.get_page(city_url)[0]
        soup = BeautifulSoup(page)
        for a in soup.find('div', attrs={'class':'zsg-lg-1-2 zsg-sm-1-1'}).findAll('a'):
            zips.append([a.text, a['href']])
            fp.write(a.text + "\n")
    fp.close()

def get_all_statecityzip():
    get_all_state()
    print states
    get_all_city()
    print cities
    get_all_zip()
    print zips

def get_all_querys_from_file():
    querys = []
    fp = open("states.txt","r")
    for line in fp.readlines():
        querys.append(line.strip())
    fp.close()
    fp = open("cities.txt","r")
    for line in fp.readlines():
        querys.append(line.strip())
    fp.close()
    fp = open("zips.txt","r")
    for line in fp.readlines():
        querys.append(line.strip())
    fp.close()
    return querys

def main():
    requester = Requester()
    #get_all_statecityzip()
    querys = get_all_querys_from_file()
    search_types = ['1_ah','for_sale','for_rent']
    for query in querys:
        for search_type in search_types:
            print "***processing query:",search_type, query
            requester.request(search_type, query)
    print "Finished!"


if __name__ =="__main__":
    main()
