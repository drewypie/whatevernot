import csv
import urllib
import urllib2
import re
import time
import json
import threading
import random

hdr = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

weaponscsv = open('weapons.csv')
# weapons = csv.reader(weaponscsv)

ListedItems = open('listeditemsconv.csv')
# weapons = csv.reader(ListedItems)

AllListedItems = open('alllisteditems.csv')
weapons = csv.reader(AllListedItems)

threadnum = raw_input("Threads: ")


def threadgen():
    i = 0
    while True:
        print "loop"
        for weapon in weapons:
            i += 1
            # print i
            # print threading.currentThread().getName() + " : " + weapon[0]
            #
            if getratio(weapon[0]) < .5:
                print "W00T!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print weapon[0] + " : " + str(getratio(weapon[0]))
                print removedollarsign(getmedianprice(weapon[0]))
                print removedollarsign(getlowestprice(weapon[0]))
                print str(100 - round(100 * getratio(weapon[0]))) + " % Off"  # COOL
                print "W00T!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        ListedItems.seek(0)
        AllListedItems.seek(0)


def buildurl(weapon):
    url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=" + \
          urllib.quote_plus(str(weapon))
    return url


def getjson(url):
    try:
        # print url
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        # ListedItems.write(url+"\n")
        return response
    # print response

    except urllib2.HTTPError, err:
        # print err

        if err.code == 429:
            # print response.info()
            time.sleep(10)
            print("OVERLOAD")
            if random.random() > .25:
                return getjson(url)
            else:
                return fakejson()

        if err.code == 500:
            # print url
            return fakejson()

        if err.code == 403:
            # print url
            print err
            time.sleep(600)
            return fakejson()


def fakejson():
    return '{"success":false,"lowest_price":"&#36;1.00","volume":"1","median_price":"&#36;1.00"}'


def getlowestprice(weapon):
    global pricearray
    try:
        pricearray = json.load(getjson(buildurl(weapon)))
    except:
        try:
            pricearray = json.loads(getjson(buildurl(weapon)))
        except:
            pass
    # print pricearray.__len__()
    if pricearray.__len__() > 1:
        return pricearray['lowest_price']


def getmedianprice(weapon):
    global pricearray
    try:
        pricearray = json.load(getjson(buildurl(weapon)))
    except:
        try:
            pricearray = json.loads(getjson(buildurl(weapon)))
        except:
            pass
    try:
        if pricearray.__len__() > 1:
            return pricearray['median_price']
    except:
        if pricearray['lowest_price'] is not None:
            return pricearray['lowest_price']


def removedollarsign(string):
    return re.sub('&#36;', '', string)


def getratio(weapon):
    return float(removedollarsign(getlowestprice(weapon))) / float(removedollarsign(getmedianprice(weapon)))


def __main__():
    threads = []
    for i in range(int(threadnum)):
        t = threading.Thread(target=threadgen)
        threads.append(t)
        t.start()


__main__()
# cProfile.run('__main__()')
