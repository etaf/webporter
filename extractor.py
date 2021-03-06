#!/usr/bin/env python
# encoding: utf-8

import sqlite3
import re
import os
from bs4 import BeautifulSoup
import urllib


#get all house from database
def get_all_house_from_db():
    conn = sqlite3.connect('zillow.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM zillow")
    pattern = re.compile(r'^http:\/\/www\.zillow\.com\/(homedetails|community)\/.*$')
    house_num = 0
    for row in cursor:
        if pattern.match(row[0]):
            house_num = house_num + 1
            print "****get detail from : ",row[0]
            get_house_detail(row[0], row[1])
    conn.close()
    print "Fiinished! %d houses extracted\n" % house_num

def get_house_detail(url,html_page):
    soup = BeautifulSoup(html_page)
    img_urls = []
    addr = ""
    house_status = ""
    price = ""
    intro = ""
    zillow_home_id = ""

    tmp = re.findall('Zillow Home ID: (\d+)</li>',html_page)
    if tmp:
        zillow_home_id = tmp[0]
    else:
        return
    addr_html = soup.find('header', attrs = {'class':'zsg-content-header addr'}).find('h1')
    if addr_html:
        addr = addr_html.text.strip()
        zip_code = re.findall(r'\d{5}', addr)
        if len(zip_code) <= 0:
            return
        else:
            zip_code = zip_code[0]
            print zip_code
    else:
        return
    for img_div in soup.findAll('img', attrs = {'class':'hip-photo'}):
        if img_div.has_attr('src'):
            img_urls.append(img_div['src'])
        if img_div.has_attr('href'):
            img_urls.append(img_div['href'])
    house_status_html = soup.find('div', attrs = {'class':'status-icon-row'})
    if house_status_html:
        house_status = house_status_html.text.strip()

    price_html = soup.find('div', attrs = {'class':'main-row  home-summary-row'})
    if price_html:
        price = price_html.text.strip()

    intro_html = soup.find('div', attrs = {'class':'notranslate'})
    if intro_html:
        intro = intro_html.text

    save_house_to_db(zillow_home_id, zip_code, addr, house_status, price, intro)
    print "details saved to database"
    #save_imgs(zillow_home_id, img_urls)
    #print "images saved to local director"

def save_imgs(zillow_home_id, img_urls):
    img_dir = os.path.join('./static/img',zillow_home_id)
    if  os.path.exists(img_dir):
        return
    os.makedirs(img_dir)
    i = 0
    for url in img_urls:
        i = i + 1
        print "***Downloading image from %s", url
        urllib.urlretrieve(url,os.path.join(img_dir,'%d.jpg' % i))
        break

def save_house_to_db(zillow_home_id, zip_code, addr, house_status, price, intro):
    conn = sqlite3.connect('house.db')
    conn.text_factory = str
    try:
        conn.execute("INSERT INTO house VALUES (?,?,?,?,?,?) ", (zillow_home_id,zip_code, addr, house_status, price, intro))
        conn.commit()
    except :
        pass
    finally:
        conn.close()

def create_db_table():
    conn = sqlite3.connect('house.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS house
                 (zillow_home_id TEXT PRIMARY KEY NOT NULL,
                 zip_code INTEGER,
                 addr TEXT,
                 house_status TEXT,
                 price TEXT,
                 intro TEXT
                 );''')
    conn.commit()
    conn.close()

if __name__ =='__main__':
    create_db_table()
    get_all_house_from_db()


