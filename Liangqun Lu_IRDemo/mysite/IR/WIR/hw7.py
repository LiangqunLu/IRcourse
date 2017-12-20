#!/usr/bin/python3

'''
Develop a retrieval program that takes as input an user query in the form of a set of keywords, uses the inverted index to retrieve documents containing
at least one of the keywords, and then ranks these documents based on cosine values between query vector and document vectors.
'''

from stemming.porter2 import stem
import os, sys

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
from scipy import spatial
import math
import numpy as np

#os.chdir("/Users/Leah/Downloads/django/mysite/IR")

##
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


###step 1 obtain a series of docs
def Step1_read_doc(dirname, allfiles):
    
    docs = dict()
    
    for one in allfiles:
        
        filename = dirname + one
        ff = open(filename, "r")
        word_list = ff.readlines()
        docs[one] = word_list[0]
        ff.close()
        
    return(docs)        


###step 2 Indexing, index terms, df, Dj, Tfj
##dict inside dict my_dict={'a':{'df':10,'dlist':["abc", 20]}}

def Step2_index(dirname, allfiles):

    docs = Step1_read_doc(dirname, allfiles)
    
    inverted_index = dict()

    ###search df and tf in all docs
    for k, v in docs.items():
        
        wlist = v.split(" ")
        
        for one in wlist:

            if one in inverted_index.keys():
                
                inverted_index[one]["df"] += 1 
                inverted_index[one]["dlist"].append([k, wlist.index(one)])
                
            else:
                
                inverted_index[one] = dict()
                inverted_index[one]["df"] = 1 
                inverted_index[one]["dlist"] = [[k, wlist.index(one)]]
                
    #print(inverted_index)
    return(inverted_index)

def Cosine_Val(q_tfidf, df, dirname):
    
    """
    output a data frame with index url, column cosine
    
    """
    http = pd.read_csv(dirname + "../allhtml_add_title_1000.csv", sep=None, index_col = 0)
    #http = pd.read_table(dirname + "../allhtml_1000.txt", sep='\t', header = None, index_col = 0)    

    out = pd.DataFrame(index = df.columns, columns = ["url","cosine", "title"])
    
    #out.loc[:, "cosine"] = [1 - spatial.distance.cosine(q_tfidf, df.loc[:, one]) for one in out.index]
    norm_q = sum([one**2 for one in q_tfidf])**(1/2)
  
    out.loc[:, "cosine"] = [np.dot(q_tfidf, df.ix[:-1, one])/(norm_q * df.ix[-1, one]) for one in out.index]
  
    ##add url
    url_l = [int(one.replace(".txt", "")) for one in out.index]
    
    out.loc[:, "url"] = list(http.ix[url_l, 1])
    
    out.loc[:, 'title'] = list(http.ix[url_l, 2])    
    
    out = out.sort_values('cosine', ascending = 0)
    
    return(out)  


def keyword_tdidf(index, inverted_index, N, dirname):
    
    """
    grab all relevant urls for the keyword first
    the output is a data frame with index seperate keyword, columns all relevant urls 
    
    """
    index = index
    urls = []
    
    for a in index:
        
        urls = urls + [one[0] for one in inverted_index[a]['dlist']]
        

    urls = list(set(urls))    
    df = pd.DataFrame(index = index + ['doc_norm'], columns = urls)
    
    for one in urls:
        
        ff = open(dirname + one, "r")
        
        ff_l = ff.readline().split()
        
        #df.loc[index, one] = [ff_l.count(one) * math.log10(N/inverted_index[one]['df']) / len(set(ff_l))  for one in index]
        
        df.loc[index, one] = [ff_l.count(one) * math.log10(N/inverted_index[one]['df']) / len(set(ff_l))  for one in index]
        
        ###add td-idf for all unique index in documents
        norm_doc = [ff_l.count(one) * math.log10(N/inverted_index[one]['df']) / len(set(ff_l))  for one in set(ff_l)]
    
        norm_doc = (sum([one**2 for one in norm_doc]))**(1/2)
        
        df.loc['doc_norm', one] = norm_doc
        
        ##normalize 
        #df.loc[index, one] = df.loc[index, one]/df.loc['doc_norm', one]
        
    
    return(df)    


def IR(query = 'international office'):

    #query = 'software engineering research'

    q = text_clean_hw4(query)

    index = q.split()

    dirname = os.getcwd() + '/IR/WIR/hw6_UofM_text_files_1000/'

    allfiles = os.listdir(dirname)

    N = len(allfiles)

    inverted_index = Step2_index(dirname, allfiles)

    q_tfidf = [index.count(one) * math.log10(N/inverted_index[one]['df']) / len(index) for one in index]

    df = keyword_tdidf(index, inverted_index, N, dirname)

    out = Cosine_Val(q_tfidf, df, dirname)

    print(query)
    print(out)
    
    return(out)


