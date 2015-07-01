#!/usr/bin/env python
# encoding: utf-8

import web
import urllib2
import cookielib
import urlparse

urls = ("/.*","proxy")
app = web.application(urls, globals())
class Crawler:
    def __init__(self):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        user_agent ='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
        self.http_header =  {'User-Agent':user_agent}

    def get_page_html(self, target_url):
        try:
            req = urllib2.Request(target_url, headers = self.http_header)
            return self.opener.open(req).read()
        except urllib2.HTTPError, err:
            print "==================\n",err
            print "==================\n",target_url
            print "==================\n"
            return ""

class proxy:
    crawler = Crawler()
    proxy_target_url = "http://www.zillow.com"
    def GET(self):
        target_url = urlparse.urljoin(self.proxy_target_url, web.ctx['path'])
        target_url = urlparse.urljoin(target_url, web.ctx['query'])
        page = self.crawler.get_page_html(target_url)
        new_page = page.replace(self.proxy_target_url, "")
        return new_page

if __name__ == "__main__":
    app.run()
