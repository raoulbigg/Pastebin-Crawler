import requests
import re
import os
import time
import sys
from bs4 import BeautifulSoup
from optparse import OptionParser


psn_plus = "(playstation plus|ps plus)"


local = os.getcwd()

def request():
    try:
        r = []
        timestr = time.strftime("%H-%M-%S")
        PASTEBIN = 'http://www.pastebin.com'
        URL = PASTEBIN + '/archive'
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text, features="html.parser")

        div = soup.find(id="menu_2")
        hrefs = div.find('a').get('href')
        print "Searching in:", hrefs, timestr
        print
        r.connection.close()
        r1 = requests.get(PASTEBIN+'/raw'+hrefs, timeout=10)
        soup = BeautifulSoup(r1.text, features="html.parser")
        match(r1, soup, timestr)

    except Exception as e:
        print e
        time.sleep(40)
        request()
        pass    

def match(r1, soup, timestr):

    if  soup.findAll(text=re.compile(psn_plus)) != []:
        print "\033[92mpsn_plus found...\033[0m"
        Save(soup)
    r1.connection.close()

    time.sleep(7)
    request()


def Save(soup):
    if not os.path.exists("psn_plus"):
        os.makedirs("psn_plus")
        os.chdir("psn_plus")
        f = open("psn_plus"+timestr+".txt", "a")
        f.write(str(soup))
        f.close()
        os.chdir(local)
    else:
        os.chdir("psn_plus")
        f = open("psn_plus"+timestr+".txt", "a")
        f.write(str(soup))
        f.close()
        os.chdir(local)   



if __name__ == '__main__':
    request()
