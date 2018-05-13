# -*- encoding: UTF-8 -*-

# 4. Parse downloaded post pages for points, upvote percent, number of comments, date and time...

import os, re
from bs4 import BeautifulSoup

# read file
def read_file(filepath, attribute):
    try:
        with open(filepath, attribute) as source:
            file = source.read()
    except:
        print ("no such file", filepath)
        file = ''
    return file

# parse web page
def parse(filepath):
    soup = BeautifulSoup(read_file(filepath, 'r'), "html5lib")
    try:
        # <div class="side">...<div class="score"><span class="number">1,785</span> <span class="word">points</span> (86% upvoted)</div>...</
        score = soup.find("div", class_="side").find("div", class_="score").text.strip()
        points = score.split(' ', 1)[0]
        upvote_percent = score.split('(', 1)[1].split('%', 1)[0]
    except:
        points = 'NA'
        upvote_percent = 'NA'
    try:
        # <meta property="og:description" content="450 points and 33 comments so far on reddit">
        comments = soup.find("meta", property="og:description").get('content').split('points and ',1)[1].split(' comments',1)[0]
    except:
        comments = 'NA'
    # <div class="date"><span>this post was submitted on  </span><time datetime="2018-01-13T16:50:06+00:00">13 Jan 2018</time></div>
    try:
        date_time = soup.find("div", class_="date").find('time').get('datetime').split('+', 1)[0]
        date = date_time.split('T')[0]
        time = date_time.split('T')[1]
    except:
        date = 'NA'
        time = 'NA'
    #<div class="top-matter">...<a href="https://www.reddit.com/user/chasmccl" class="author may-blank id-t2_foaym">chasmccl</a>...</
    try:
        top_matter = soup.find("div", class_="top-matter")
    except:
        top_matter = 'NA'
    try:
        user = top_matter.find("a", class_=re.compile("^author may-blank id")).text.strip()
    except:
        user = 'NA'
    #<div class="top-matter">...<span class="flair flair-ocmaker" title="OC: 3">OC: 3</span>...</div>
    try:
        uflair = top_matter.find("span", class_="flair flair-ocmaker").text.strip().split(': ', 1)[1]
    except:
        uflair = 'NA'
    #<div class="top-matter"><p class="title"><a class="title may-blank loggedin outbound" data-event-action="title" href="https://www.youtube.com/attribution_link?a=p_qg-epTM4A&amp;u=%2Fwatch%3Fv%3DRAPN0Q8BlgI%26feature%3Dshare" tabindex="1" data-href-url="https://www.youtube.com/attribution_link?a=p_qg-epTM4A&amp;u=%2Fwatch%3Fv%3DRAPN0Q8BlgI%26feature%3Dshare" data-outbound-url="https://out.reddit.com/t3_71ww5u?url=https%3A%2F%2Fwww.youtube.com%2Fattribution_link%3Fa%3Dp_qg-epTM4A%26u%3D%252Fwatch%253Fv%253DRAPN0Q8BlgI%2526feature%253Dshare&amp;token=AQAAC1dpWtaXOJRemjdJs1gHwJG5c9fdjSvXsEzDEyyFLd9dmEh9&amp;app_name=reddit.com" data-outbound-expiration="1516853003000" rel="nofollow">【短片】【KO彭定康失實言論】馬恩國：塑造香港淪為人治形象、對香港聲譽影響十分大、點解你退了20年還要傷害香港？</a> <span class="domain">(<a href="/domain/youtube.com/">youtube.com</a>)</span></p>
    try:
        title = top_matter.find("a").text.strip()
    except:
        title = 'NA'
    print points, upvote_percent, comments, date, time, user, uflair, title
    data.append([element for element in [points, upvote_percent, comments, date, time, user, uflair, title, shorturl] if element])

# write out to tab delimited file
def write_out (data):
    with open(rootdir+filename_out, 'w') as output:
        for j in range(len(data)):
            for k in range(len(data[j])):
                if data[j][k]:
                    output.write(data[j][k].encode('utf8'))
                    output.write(u"\u0009")
            output.write(u"\u000D")


rootdir = u'.../reddit_dataisbeautiful_new/'        # where posts have been downloaded
filename_source = 'post_links.txt'                  # where post links have been saved
filename_out = 'results.txt'                        # where parsed data will be saved (tab-delimited format)
data = [['points', 'approval', 'comments', 'date', 'time', 'user', 'flair', 'title', 'url']]     #dataframe
i = 0

with open(rootdir+filename_source, 'r') as source:
    for url in source.readlines():
        sub = url.split('.com', 1)[1].split('/comments')[0]
        shorturl = url.split('comments/', 1)[1].split('/')[0]       # get short url
        filepath = rootdir+'posts/'+'post_'+shorturl+'.html'        # use short url for file name
        print '\n', i, ": ", url
        i += 1
        parse(filepath)
    if data:
        write_out(data)
        #print data


