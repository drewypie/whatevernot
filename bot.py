import csv
import urllib
import urllib2
import re
import time
import datetime
import json
import random
import cProfile
import threading
import random

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

weaponscsv = open('weapons.csv')
weapons = csv.reader(weaponscsv)

ListedItems = open('listeditemsconv.csv')
weapons = csv.reader(ListedItems)

AllListedItems = open('alllisteditems.csv')
weapons = csv.reader(AllListedItems)


threadnum = raw_input("Threads: ")

def threadGen():
    i=0
    ListedItems.seek(int(random.random()*400))
    AllListedItems.seek(int(random.random()*400))
    while True:
        print "loop"
        for weapon in weapons:
            i+=1
            #print i
            print threading.currentThread().getName() + " : " + weapon[0]
            #
            if(getRatio(weapon[0])<.5):
            	print "W00T!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print weapon[0] + " : " + str(getRatio(weapon[0]))
                print removeDollarSign(getMedianPrice(weapon[0]))
                print removeDollarSign(getLowestPrice(weapon[0]))
        ListedItems.seek(0)
        AllListedItems.seek(0)
            
def buildURL(weapon):
    url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=" + urllib.quote_plus(str(weapon))
    return url

def getJSON(url):
    try:
        #print url
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        #ListedItems.write(url+"\n")
        return response
        #print response
        
    except urllib2.HTTPError,err:
        #print err
        
        if err.code == 429:
            #print response.info()
            time.sleep(10)
            print("OVERLOAD")
            if random.random() > .25:
                return getJSON(url)
            else:
                return fakeJSON()
            
        if err.code == 500:
            #print url
            return fakeJSON()

        if err.code == 403:
            #print url
            print err
            time.sleep(300)
            return fakeJSON()

def fakeJSON():
    return '{"success":false,"lowest_price":"&#36;1.00","volume":"1","median_price":"&#36;1.00"}'

def getLowestPrice(weapon):
    try:
        pricearray = json.load(getJSON(buildURL(weapon)))
    except:
        pricearray = json.loads(getJSON(buildURL(weapon)))
	return pricearray['lowest_price']

def getMedianPrice(weapon):
    try:
        pricearray = json.load(getJSON(buildURL(weapon)))
    except:
        pricearray = json.loads(getJSON(buildURL(weapon)))
    try:
        return pricearray['median_price']
    except:
        return pricearray['lowest_price']

def removeDollarSign(string):
    return re.sub('&#36;','',string)

def getRatio(weapon):                        
    return float(removeDollarSign(getLowestPrice(weapon)))/float(removeDollarSign(getMedianPrice(weapon)))

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def __main__():
    threads = []
    for i in range(int(threadnum)):
        t = threading.Thread(target=threadGen)
        threads.append(t)
        t.start()
    
__main__()
#cProfile.run('__main__()')
