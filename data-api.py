#!/usr/bin/env python
# encoding: utf-8
import sqlite3
class House(object):
    def __init__(self, zillow_home_id, addr="", house_status = "", price = "", intro = ""):
        self.zillow_home_id = zillow_home_id
        self.addr = addr
        self.house_status = house_status
        self.price = price
        self.intro = intro

    def __str__(self):
        return "=======\n" + '\n'.join([self.zillow_home_id, self.addr, self.house_status, self.price, self.intro])

def get_extrated_houses():
    #return a list of instance of class House
    houses = []
    conn = sqlite3.connect('house.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM house")
    for row in cursor:
        houses.append( House(row[0],row[1],row[2],row[3],row[4]))
    return houses

if __name__ =='__main__':

    houses = get_extrated_houses()
    print "%d houses."  % len(houses)
    print "an example:"
    print houses[0]

