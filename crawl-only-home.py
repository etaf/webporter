#!/usr/bin/env python
# encoding: utf-8

from webporter import  Proxy
proxy = Proxy()
def visit_all_home_page(max_zillow_id):
    pre_url = 'http://www.zillow.com/homedetails/'
    for i in xrange(max_zillow_id):
        target_url = pre_url + "%d_zpid/" % (i+1)
        print "****processing: ", target_url
        (new_page, in_db) = proxy.get_page(target_url)
if __name__ == '__main__':
    visit_all_home_page(1000000)
