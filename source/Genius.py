'''
Created on Jan 9, 2018

@author: Mathilda
'''

import random
from urllib2 import URLError, HTTPError
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from xml_cleaner import wiki_markup_processing as wikip
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import httplib

class GeniusInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        # raw is the filename of all the markup files
        path = r'/Users/Mathilda/Documents/workspace/WikiHoax/source/nonhoax/markup'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        random.shuffle(files)
        
        self.files = files[0:1520]
        self.lna = []
        self.lnawrong = []
        self.wordcount = []
        self.linkcount = []
        self.egonum = []
        
    def get_lna(self): 
        for item in self.files:
#             print(item)
            src = r'/Users/Mathilda/Documents/workspace/WikiHoax/source/nonhoax/markup/' + item
            try:
                with open(src,'r') as f:
                    text = f.read().split('name="wpTextbox1" rows="25" style="" tabindex="1">')[1].split('</textarea>')[0]
                    text.replace('\n', ' ')
                    p = wikip.to_raw_text_markupless(text, keep_whitespace=False, normalize_ascii=False)
                    self.lna.append([text, p])
            except:
                self.lnawrong.append(item)
                print(item)
                 
        text = []
        for item in self.lna:
            sen = []
            for sentence in item[1]:
                for word in sentence:
                    if re.match(r'\W',word):
                        sentence.remove(word)
                sen.append((' ').join(sentence))
            text.append((' ').join(sen))
             
        for i in range(0,len(self.lna)):
            self.lna[i][1] = text[i]
             
#         print(len(self.lna))
#         print(len(self.lnawrong))
                
                
    def get_linkcount(self):
        for item in self.lna:
            wikilink = len(re.findall(r'\[\[.+?\]\]',item[0]))
            url = len(re.findall(r'url',item[0]))
            self.linkcount.append([wikilink,url+wikilink])
    
    def get_wordcount(self):
        tokenizer = RegexpTokenizer(r'\w+')
        for item in self.lna:
            self.wordcount.append([len(word_tokenize(item[0].decode('utf-8'))),len(tokenizer.tokenize(item[1]))])
    
    
    def get_egonum(self):
        egonetwork = []
        egonames = []
        for i in range(0,len(self.lna)):
            articles = []
            names = []
            wikilink = re.findall(r'\[\[.+?\]\]',self.lna[i][0])
            for link in wikilink:
                name = link[2:-2].split('|')[0].replace(' ','_')
                html = r"https://en.wikipedia.org/w/index.php?title=" + name.decode('utf-8') + "&action=edit"
                try:
                    page = urllib2.urlopen(html.encode('utf-8'))
                    try:
                        pagemarkup = page.read()
                    except httplib.IncompleteRead, e:
                        return e.partial
                except (URLError, HTTPError) as e:
                    print e.reason
                try:
                    article = BeautifulSoup(pagemarkup,'html.parser').find(id="wpTextbox1").text
                    articles.append(article)
                    names.append(name)
                except:
                    print name    
                    
            egonetwork.append(articles)
            egonames.append(names)
        
        for i in range(0,len(egonetwork)):
            self.egonum.append(0)
            for article in egonetwork[i]:
                wikilink = re.findall(r'\[\[.+?\]\]',article.encode('utf-8'))
                for link in wikilink:
                    name = link[2:-2].split('|')[0].replace(' ','_')
                    if name in egonames[i]:
                        self.egonum[i] += 1
            if len(egonames[i]) == 0 or len(egonames[i]) == 1:
                self.egonum[i] = 0
            else:
                self.egonum[i] = self.egonum[i] / float(len(egonames[i]) * (len(egonames[i])-1))
             
                
                
                
    def get_all(self):
        self.get_lna()
        self.get_wordcount()
        self.get_linkcount()
        self.get_egonum()
                
                
                
                
                
                
                
                
                
                
                
                
                
                