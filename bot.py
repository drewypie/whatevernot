import csv
import urllib
import urllib2
import re
import time
import json
import threading
import random
import webbrowser
import HTMLParser
import os

h = HTMLParser.HTMLParser()

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
# weapons = csv.reader(AllListedItems)

AdrenalineItems = open('adrenalineitems.csv')  # specially selected items to increase speed
weapons = csv.reader(AdrenalineItems)

# threadnum = raw_input("Threads: ")

# checkonlinebool = raw_input("Check Online: ")

sessid = '6c71d1405fd5f3764949ab49'  # raw_input("Session ID: ")


def checkonline():
    global OnlineItems
    global weapons
    writer = ""
    for weapon in weapons:
        # print weapon[0]
        print buildbrowserurl(weapon[0])
        html = geturl(buildbrowserurl(weapon[0]))
        if re.findall('no listings', str(html.read())):
            print weapon[0]
        else:
            writer += weapon[0] + "\n"
    onlineitemsfile = open("onlineitems.csv", "w+")
    onlineitemsfile.write(writer)
    onlineitemsfile.close()


def threadgen():
    i = 0
    while True:
        print "loop"
        print time.time()
        for weapon in weapons:
            i += 1
            # print i
            # print threading.currentThread().getName() + " : " + weapon[0]
            # print removedollarsign(getmedianprice(weapon[0]))
            #
            ratio = getratio(weapon[0])
            if ratio < .5:
                webbrowser.open(buildbrowserurl(weapon[0]))
                print "W00T!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print weapon[0] + " : " + str(ratio)
                # print removedollarsign(getmedianprice(weapon[0]))
                print removedollarsign(getlowestprice(weapon[0]))
                print str(100 - round(100 * ratio)) + " % Off"  # COOL
                print "W00T!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        OnlineItems.seek(0)


def buildjsonurl(weapon):
    url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=" + \
          urllib.quote_plus(str(weapon), "%")
    # print url
    return url


def buildbrowserurl(weapon):
    url = "https://steamcommunity.com/market/listings/730/" + \
          urllib.quote(str(weapon), "%")
    return url


def getbuyurl(weapon, price):
    listingurl = buildbrowserurl(weapon)
    html = geturl(listingurl)
    stringhtml = html.read()
    pricecheck = getprice(stringhtml)
    print pricecheck
    pricechecknocomma = re.sub(',', '.', pricecheck)
    listing = getlisting(stringhtml)
    if closeenough(pricechecknocomma, price):
        url = "https://steamcommunity.com/market/buylisting/" + listing
    else:
        print 'TOO SLOW'
        return
    subtotal = getsubtotal(stringhtml)
    subtotalnocomma = re.sub(',', '.', subtotal)
    fee = float(pricechecknocomma) - float(subtotalnocomma)

    post_values = {
        'sessionid': sessid,
        'currency': '5',
        'subtotal': removedecimal(subtotalnocomma),
        'fee': removedecimal(fee),
        'total': removedecimal(pricechecknocomma),
        'quantity': '1'
    }

    action = url
    method = 'post'

    js_submit = '$(document).ready(function() {$("#form").submit();});'

    input_field = '<input type="hidden" name="{0}" value="{1}" />'

    base_file_contents = """
    <script src='http://www.google.com/jsapi'></script>
    <script>
        google.load('jquery', '1.3.2');
    </script>

    <script>
        {0}
    </script>

    <form id='form' action='{1}' method='{2}' />
        {3}
    </form>
    """

    input_fields = ""

    for key, value in post_values.items():
        input_fields += input_field.format(key, value)

    with open('temp_file.html', "w") as file:
        file.write(base_file_contents.format(js_submit, action, method, input_fields))
        file.close()
        webbrowser.open(os.path.abspath(file.name))
        # os.remove(os.path.abspath(file.name))


def getlisting(html):
    listingwithtag = re.search("listing_\d{18}\"", html)
    listingwithouttag = re.sub('\D', '', listingwithtag.group(0))
    return listingwithouttag


def removedecimal(string):
    string = str(string)
    string = re.sub('\.', '', string)
    return re.sub("(?<!\d)0+(?=\d+)", "", string)


def getprice(html):
    # print html
    pricewithtag = re.search('market_listing_price market_listing_price_with_fee">.*?<\/span>', html, re.DOTALL)
    print pricewithtag.group(0)
    pricewithouttag = re.sub('[^\d\.\d,\d]', '', h.unescape(pricewithtag.group(0)))
    print pricewithouttag
    return pricewithouttag


def getsubtotal(html):
    # print html
    pricewithtag = re.search('market_listing_price market_listing_price_without_fee">.*?<\/span>', html, re.DOTALL)
    pricewithouttag = re.sub('[^\d\.\d,\d]', '', h.unescape(pricewithtag.group(0)))
    # print pricewithouttag
    return pricewithouttag


def closeenough(price1, price2):
    print "!" + str(price2)
    try:
        price1 = float(str(price1) + "0")
        print(str(price1) + "0")
        price2 = float(str(price2) + "0")
    except:
        print 'SOLD!'
        return False
    if price1 is 0 or price2 is 0:
        print 'SOLD!'
        return False
    # USD
    if 1.1 > (price1 / price2) > .9:
        print "!" + str(price1)
        return True
    # Euro
    europrice1 = price1 / .88
    if 1.1 > (europrice1 / price2) > .9:
        print "!" + str(europrice1)
        return True
    # Ruble
    rubleprice1 = price1 / 54.04
    if 1.1 > (rubleprice1 / price2) > .9:
        print "!" + str(rubleprice1)
        return True
    # GBP
    gbpprice1 = price1 / .63
    if 1.1 > (gbpprice1 / price2) > .9:
        print "!" + str(gbpprice1)
        return True
    return False


def buy(weapon, price):
    getbuyurl(weapon, price)


def geturl(url):
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
                return geturl(url)
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
        pricearray = json.load(geturl(buildjsonurl(weapon)))
    except:
        try:
            pricearray = json.loads(geturl(buildjsonurl(weapon)))
        except:
            pass
    # print pricearray.__len__()
    if 'lowest_price' in pricearray:
        return pricearray['lowest_price']
    return "&#36;100000"


def getmedianprice(weapon):
    global pricearray
    try:
        pricearray = json.load(geturl(buildjsonurl(weapon)))
    except:
        try:
            pricearray = json.loads(geturl(buildjsonurl(weapon)))
        except:
            pass
    try:
        if 'median_price' in pricearray:
            return pricearray['median_price']
    except:
        if 'lowest_price' in pricearray:
            return pricearray['lowest_price']
    return '&#36;1'


def removedollarsign(string):
    # print string
    return re.sub('&#36;', '', string)


def getratio(weapon):
    return float(removedollarsign(getlowestprice(weapon))) / float(removedollarsign(getmedianprice(weapon)))


def __main__():
    global OnlineItems
    global weapons
    if "yes" in str(checkonlinebool):
        checkonline()
    OnlineItems = open('onlineitems.csv')
    weapons = csv.reader(OnlineItems)
    threads = []
    for i in range(int(threadnum)):
        t = threading.Thread(target=threadgen)
        threads.append(t)
        t.start()


buy('M4A1-S | Nitro (Minimal Wear)', 3.37)
# checkonline()
# __main__()
# cProfile.run('__main__()')
