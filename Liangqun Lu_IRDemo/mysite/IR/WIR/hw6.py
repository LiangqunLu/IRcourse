#!/usr/bin/python3

"""
Automatically collect from memphis.edu 10,000 unique documents
"""

import os, sys

os.chdir("/home/llu/Code/WIR")

sys.path = [''] + sys.path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
from bs4 import Comment
from stemming.porter2 import stem
import pandas as pd
import re
import urllib.request
import urllib.response
import urllib.error


def stopwords():
    
    if os.path.exists("english.stopwords.txt"):
        
        inn = open("english.stopwords.txt", 'r')
        stops = inn.readlines()
        stops = [one.replace("\n", '') for one in stops]
    
    else:    
    
        url = 'http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt'
        stops = urlopen(url).read().decode('iso-8859-1').split("\n")
        stops = [one.strip() for one in stops if one != '']
    
    return(stops)

def text_clean_hw4(text):
    
    texts = text.lower()
    
    #remove digits
    texts = re.sub(r'\d+', ' ', texts)
    texts = re.sub(r'%', ' ', texts)
    texts = re.sub(r"\s+", ' ', texts)    
    ##remove stop words
    stops = stopwords()
    stops = [one.lower() for one in stops]  

    texts = " ".join([one for one in texts.split() if one not in stops])
    texts = re.sub(r'\W+', ' ', texts)

    texts = [stem(one) for one in texts.split()]
    texts = list(set(texts))
    
    texts = " ".join(texts)
    
    return(texts)
    
    
def obtain_url_text(onelink):
    
    onelink = onelink
    try:
        html = urllib.request.urlopen(onelink)
    except urllib.error.HTTPError as e:
        return("")
    
    code = urlopen(onelink).getcode()
    
    if code != 200:
        return("")
    
    #url = onelink
    #html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser', from_encoding="iso-8859-1")    
    
    for script in soup(["script", "style"]):
        script.extract()

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    # get text
    text = u' '.join(soup.findAll(text=True))
    
    text = text_clean_hw4(text)
    
    return(text)        
    
    
def obtain_url_links(url):

    onelink = url
    try:
        html = urllib.request.urlopen(onelink)
    except urllib.error.HTTPError as e:
        return("")
    
    code = urlopen(onelink).getcode()
    
    if code != 200:
        return("")

    #html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser', from_encoding="iso-8859-1")

    links = []

    for one in soup.find_all('a', href=True):
    
        http = one['href']
        
        if http.startswith('http://www.memphis.edu'):
            
            http = http.replace('http://www.memphis.edu', '') 
            
            links.append(http)
            
        else:
            links.append(http)
            
    
    links = [one for one in links if not one.startswith("https://") or not one.startswith("http://")]
    links = [one for one in links if one.startswith("/") and len(one) > 1 ]
    links = [one for one in links if "pdf" not in one and '.mp4' not in one]
    links = [one for one in links if "@" not in one and '.jpg' not in one and '.zip' not in one]
    links = [one for one in links if ".png" not in one and '.eps' not in one and '.xls' not in one]
    links = [one for one in links if ".mp4" not in one and '#' not in one and '.jpg' not in one]    
    
    links = list(set(links))
    
    return(links)


allhtml = [] ##10, 000 unique links
allwords = []


url = "http://www.memphis.edu"

Q = deque([url])

while Q:
    
    u = Q.popleft()
    
    print("Total unique urls:", len(Q)); 
    
    print("Total unique urls:", len(set(Q)));     
    
    print("Saved unique urls:", len(allhtml))
    
    print(u)
    
    text = obtain_url_text(u)
    
    if(len(text.split()) >= 50 and u not in allhtml):
        
        allhtml.append(u)
        allwords.append(text)
        
    links = obtain_url_links(u)
    
    links = [one if "memphis.edu" in one else url + one for one in links]
    links = [one for one in links if '%' not in one]
    links = [one for one in links if one.count('www.memphis') == 1]
    links = [one for one in links if '.docx' not in one]
    links = [one for one in links if one.startswith('http://www.memphis.')]    
    
    links = list(set(links) - set(Q))

    Q.extend(links)

    if len(set(allhtml)) == 10000:
        
        break
                
##save 10, 000 htmls and their texts

out = open('allhtml.txt', 'w')

for idx, one in enumerate(allhtml):

    out.write( str(idx) + "\t" + one + "\n")
    
out.close()

out = open('allhtml_text.txt', 'w')

for idx, one in enumerate(allwords):
    
    out.write( str(idx) + "\t" + one + "\n")
    
out.close()    

##write out to seperate text files

for idx, one in enumerate(allwords):
    
    out = open('./hw6_UofM_text_files/' + str(idx) + '.txt', 'w')
    
    out.write(one)
    
    out.close()

##obtain webpage_title
def Get_title(url):
    
    title = ''
    
    if ".php" in url or url.endswith('/'): 
    
        onelink = url
        try:
            html = urllib.request.urlopen(onelink)
        except urllib.error.HTTPError as e:
            return("")
            
        code = urlopen(onelink).getcode()
    
        if code != 200:
            return("")
    
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding="iso-8859-1")

        title = soup.title.text
    
        title = title.replace('\n', '')
        title = title.replace('\s+', ' ')    

    return(title)



ff = pd.read_table("allhtml.txt", header = None)
ff['title'] = pd.Series("", index=ff.index)

for i in range(ff.shape[0]):
    
    ff.iloc[i, 2] = Get_title(ff.iloc[i, 1])
    
    print(i, ff.iloc[i, 2])
    
ff.to_csv("allhtml_add_title.csv")

