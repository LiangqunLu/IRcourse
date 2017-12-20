#!/usr/bin/python3

"""
In this homework, we aim to generate the inverted index of a set of already preprocessed files

Usage: ./hw5.py "/home/llu/Code/WIR/news/"

"""

import os, sys

#dirname = "/home/llu/Code/WIR/news/"

if len(sys.argv) == 2:
    dirname = sys.argv[1]
else:
    
    print("Usage: ./hw5.py \"/home/llu/Code/WIR/news/\"")
    sys.exit("folder name is demanding!!!")
    
allfiles = os.listdir(dirname)
allfiles = [one for one in allfiles if ".html" in one]  
    
###step 1 obtain a series of docs
def Step1_read_doc(allfiles):
    
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

def Step2_index():

    docs = Step1_read_doc(allfiles)
    
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


inverted_index = Step2_index()
print(inverted_index)    

