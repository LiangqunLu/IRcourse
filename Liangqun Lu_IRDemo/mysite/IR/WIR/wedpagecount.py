#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


###part I download text from the website
url = "http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"

html = urlopen(url)

soup = BeautifulSoup(html, 'html.parser')

texts = soup.getText()


# process the text including the removal of non-alphanumeric and numbers

texts = texts.lower()

texts = re.sub(r'\W+', ' ', texts)

texts = re.sub(r'\d+', ' ', texts)

texts = re.sub(r"_", ' ', texts)

texts = re.sub(r"\s+", ' ', texts)

texts = texts.strip()

print('The length of the texts is: ', len(texts.split(" ")))

## count the number of unique words as well as word frequency
def word_count(str):
    counts = dict()
    words = str.split(" ")

    for word in words:
    
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    
    return counts


counts = word_count(texts)    

print("total word number: ", len(counts))

#save an ordered word list to an output file

ff = open('file.txt', 'w')

for key in sorted(counts.keys()):

    line = key + ":" + str(counts[key]) 

    print(line)
    
    ff.write(line + "\n")
    
ff.close()
    


