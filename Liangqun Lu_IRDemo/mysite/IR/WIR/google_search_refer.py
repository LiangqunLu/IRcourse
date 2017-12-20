#!/usr/bin/python3

"""
this script aims to grab 100 results from google search on those 10 exmaple queries
count how many are in our local document pool and calculate the precision and recall to evaluate our website

"""

import os, sys

os.chdir("/home/llu/Code/WIR")

sys.path = [''] + sys.path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
from bs4 import Comment

import pandas as pd
import re
import urllib.request
import urllib.response
import urllib.error
import requests
import pandas as pd
import time


def get_google_page(url):
    
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    links = []
    for item in soup.find_all('h3', attrs={'class' : 'r'}):
        links.append(item.a['href'][7:])    

    return(links)

    
def set_page(query = 'software engineering research'):
    
    google_s_front = 'https://www.google.com/search?q='
    
    q = query.replace(" ", "+")
    
    s2 = '+site%3A+memphis.edu&ei=jyoqWraBF6HejwS41oroDg&start='
    
    #page = str(0) here 
    
    s3 = '&sa=N&biw=1056&bih=568'
    
    ranks = []
    
    for i in range(10):
        
        page = str(i * 10)
        
        url = google_s_front + q + s2 + page + s3
        
        results = get_google_page(url)
        
        print(page)
        print(results)
        
        time.sleep(5)
        
        ranks.extend(results)
        
    return(ranks)


Q_list = ['international office', 'software engineering research', 'Cookie', 'president of the university', 'computer science research awards', 'semantic similarity', "tiger bike's current offer", "where is the library located?", "How to graduate with honors?", "scholarships in computer science"]
 
google_search = pd.DataFrame(index = Q_list, columns = range(100))

for one in Q_list[7:]:
    
    print(one)
    
    ranks = set_page(one)

    print(len(ranks))

    if len(ranks) > 0:
        
        google_search.ix[one, :(len(ranks) - 1)] = ranks

google_search.to_csv("google_search_refer_last3.csv")





