# -*- encoding: UTF-8 -*-

# 1. Download lists of new posts

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
    #print ("         user agent: ", ua)
    headers = {"Connection" : "keep-alive", "User-Agent" : ua}
    try:
        s = requests.session()
        page = s.get(url, headers=headers).content
    except:
        page = None
    return page

def get_save_name(path, name):
    return path + '/' + name + '.html'

# save web page
def save(page, path, name):
    fn = get_save_name(path, name)
    if not os.path.isdir(os.path.dirname(fn)):
        os.makedirs(os.path.dirname(fn))
    f = open(fn, 'wb')
    try:
        with open(fn, 'wb') as f:
            f.write(page)
    except:
        pass

# obtain the url of the next page
def next_url (page):
    soup = BeautifulSoup(page, "html5lib")
    return soup.find_all("span", class_="next-button")[0].find("a").get('href')

# download web page
def download(url, name, path, user_agents):
    page = get_page(url, user_agents)
    size = sys.getsizeof(page)
    while size < 50000:
        print "         size too small, trying again, size = "+str(size)+" Bytes"
        page = get_page(url, user_agents)
        size = sys.getsizeof(page)
        print page
        sleep(60+random.random()*5)
    save(page, path, name)
    print "         success, size = "+str(size)+" Bytes"
    print >> download_log, url
    return next_url (page) # return next url to crawl




root_dir = '.../reddit_dataisbeautiful_new/'                    # destination folder
root_url = 'https://www.reddit.com'
download_log = open(root_dir+'post_lists.log', 'w')             # download log
user_agents = LoadUserAgents(root_dir+'user_agents_non_mobile.txt')  # load non-mobile user agents in random order
url = root_url+'/r/dataisbeautiful/new/'
for i in range (1,41):                                          # reddit keeps only 40 pages of latest posts. Each page lists 25 posts.
    print "target: ", url
    url = download(url, 'list'+str(i), root_dir+'list/', user_agents)   # download previous page and return page address
    sleep(1+random.random()*3)                                  # IMPORTANT! Must wait between requests. Don't hog reddit servers! And make a donation afterwords.

