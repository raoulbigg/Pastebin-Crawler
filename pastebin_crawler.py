import requests
import re
import os
import time
import sys
from bs4 import BeautifulSoup
from optparse import OptionParser


passwords_pat = "(password|pswd|passwd|pwd|admin:admin)"
mails_pat = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
leaked_pat = "(hacked|hacking)"


local = os.getcwd()

def request():
    try:
        r = []
        timestr = time.strftime("%H-%M-%S")
        PASTEBIN = 'http://www.pastebin.com'
        URL = PASTEBIN + '/archive'
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text)

        div = soup.find(id="menu_2")
        hrefs = div.find('a').get('href')
        print "Searching in:", hrefs, timestr
        print
        r.connection.close()
        r1 = requests.get(PASTEBIN+'/raw'+hrefs, timeout=10)
        soup = BeautifulSoup(r1.text)
        match(r1, soup, timestr)
        
    except requests.exceptions.ConnectionError:
        print "Connection refused.. sleeping for 40"
        time.sleep(40)
        request()

    except UnboundLocalError:
        print "UnboundLocalError..."
        pass
    except RuntimeError as e:
        time.sleep(40)
        request()
        pass    

def match(r1, soup, timestr):

    if  soup.findAll(text=re.compile(leaked_pat)) == []:
        print "No leaks found"
    else:
        print "\033[92mLeaks found...\033[0m"
        if not os.path.exists("leaks"):
            os.makedirs("leaks")
            os.chdir("leaks")
            f = open("leaks"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)
        else:
            os.chdir("leaks")
            f = open("leaks"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)
   
    if soup.findAll(text=re.compile(passwords_pat)) == []:
        print "No passwords found..."
    else:
        print "\033[92mPasswords found...\033[0m"
        if not os.path.exists("passwords"):
            os.makedirs("passwords")
            os.chdir("passwords")
            f = open("passwords"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)
        else:
            os.chdir("passwords")
            f = open("passwords"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)

    if soup.findAll(text=re.compile(mails_pat)) == []:
        print "No mails found..."
    else:
        print "\033[92mMails found...\033[0m"
        if not os.path.exists("mails"):
            os.makedirs("mails")
            os.chdir("mails")
            f = open("mails"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)

        else:
            os.chdir("mails")
            f = open("mails"+timestr+".txt", "a")
            f.write(str(soup))
            f.close()
            os.chdir(local)
    r1.connection.close()
    print "Next request will be in 7 seconds"
    print
    time.sleep(7)
    request()



if __name__ == '__main__':
    request()
