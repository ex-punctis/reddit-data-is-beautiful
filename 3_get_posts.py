# -*- encoding: UTF-8 -*-

# 3. Download post pages

import requests, os, sys
from time import sleep
import random
from bs4 import BeautifulSoup

# return shuffled list of user agents
def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    print ("User agents loaded")
    return uas

# Fetch web page using requests library
def get_page(url, user_agents):
    ua = random.choice(user_agents)
    headers = {"Connection" : "keep-alive", "User-Agent" : ua}
    try:
        s = requests.session()
        page = s.get(url, headers=headers).content
    except:
        page = None
    return page


# Fetch web page using requests library
def get_page(url):
    global s
    ua = random.choice(user_agents)
    headers = {"Connection" : "keep-alive", "User-Agent" : ua}
    try:
        s = requests.session()
        page = s.get(url, headers=headers).content
    except:
        print ("Error, no page")
        return None
    return page

# Path + file name + extension
def get_save_name(path, name):
    return path+name+'.html'

# Save web page
def save(page, name, path):
    fn = get_save_name(path+'/posts/', name)
    if not os.path.isdir(os.path.dirname(fn)):
        os.makedirs(os.path.dirname(fn))
    f = open(fn, 'wb')
    try:
        with open(fn, 'wb') as f:
            f.write(page)
    except:
        pass


# Append error log
def log(url):
    with open(rootdir+'post_download_err.log', 'a') as error_log:
        error_log.write (url + "\n")

# Scrape post pages
def scrape(url):
    sleep(2+random.random()*5)
    page = get_page(url)
    size = sys.getsizeof(page)
    if size > 1000:
        print "         success, size = "+str(size)+" Bytes"
        save(page, 'post_'+url.split('comments/', 1)[1].split('/')[0], rootdir)
    else:
        print "         size too small, appending error log and skipping, size = "+str(size)+" Bytes"
        try:
            save(page, '_error', rootdir)
        except:
            print ("No page, passing")
            pass
        log(url)


# main:

rootdir = u'.../reddit_dataisbeautiful_new/'                # destination folder

# load user agents in random order
user_agents = LoadUserAgents('.../user_agents_non_mobile.txt') # list of non-mobile user agents
s = requests.session()
i = 0
with open(rootdir+'post_links.txt', 'r') as source:
    for url in source.readlines():
        print i, ":   ", url
        i += 1
        scrape(url)






