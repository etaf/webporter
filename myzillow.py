#!/usr/bin/env python
# encoding: utf-8

import web
import urllib2
import cookielib
import urlparse
import sqlite3
import time
import socket
urls = (
    "/","index",
    "/search", "search",
        )
app = web.application(urls, globals())


class index:
    def GET(self):
        render = web.template.render('templates/')
        return render.index()

from data_api import get_houses_by_zip
class search:
    def POST(self):
        zip_code = web.input().zip
        houses = get_houses_by_zip(zip_code)
        content = "\n".join(str(house) for house in houses)
        print content
        render = web.template.render('templates/')
        return render.search_result(zip_code, houses)
if __name__ == "__main__":
    app.run()
