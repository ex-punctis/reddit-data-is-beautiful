# -*- encoding: UTF-8 -*-

# 2. Extract post urls from post lists

import os
from bs4 import BeautifulSoup

def read_file(filepath, attribute):
    try:
        with open(filepath, attribute) as source:
            file = source.read()
    except:
        print ("no such file", filepath)
    return file

# url examples
#<a href="/r/dataisbeautiful/comments/6nlfnk/who_is_the_simpsons_main_side_character_oc/" data-inbound-url="/r/dataisbeautiful/comments/6nlfnk/who_is_the_simpsons_main_side_character_oc/?utm_content=comments&amp;utm_medium=browse&amp;utm_source=reddit&amp;utm_name=dataisbeautiful" data-href-url="/r/dataisbeautiful/comments/6nlfnk/who_is_the_simpsons_main_side_character_oc/" data-event-action="comments" class="bylink comments may-blank" rel="nofollow">1375 comments</a>
#<a href="/r/dataisbeautiful/comments/70gjal/where_and_when_rivers_flooded_from_hurricane_irma/" data-inbound-url="/r/dataisbeautiful/comments/70gjal/where_and_when_rivers_flooded_from_hurricane_irma/?utm_content=comments&amp;utm_medium=browse&amp;utm_source=reddit&amp;utm_name=dataisbeautiful" data-href-url="/r/dataisbeautiful/comments/70gjal/where_and_when_rivers_flooded_from_hurricane_irma/" data-event-action="comments" class="bylink comments may-blank" rel="nofollow">343 comments</a>

# Parse and return urls as list
def parse(filepath, data):
    soup = BeautifulSoup(read_file(filepath, 'r'), "html5lib")
    links = soup.find_all("a", class_="bylink comments may-blank")
    return links

# write out to tab delimited file
def write_out (data):
    for element in data:
        print >> post_links, element.get('href').encode('utf-8')


root_dir = u'.../reddit_dataisbeautiful_new/'           # folder with downloaded post lists
post_links = open(root_dir+'post_links.txt', 'w')       # where post url will be saved
data = []
for i in range (1,41):
    filepath = root_dir+'list/list'+str(i)+'.html'
    print "target: ", filepath
    data = parse(filepath, data)
    if data:
        write_out(data)