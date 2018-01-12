'''
Created on Jan 9, 2018

@author: Mathilda
'''

from urllib2 import URLError, HTTPError
import urllib2
import re
from nltk.tokenize import word_tokenize, RegexpTokenizer
from xml_cleaner import wiki_markup_processing as wikip
from os.path import isfile
from bs4 import BeautifulSoup
from HoaxCollection import *
import httplib

class HoaxInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        # raw is the filename of all the markup files
#         if isfile('/Users/Mathilda/Documents/workspace/WikiHoax/source/m30/m30.txt'):
        self.raw = read_in_m30()
#         else:
#             raw = get_formatted_date(get_abstract())
#             save_docs(raw)
        # lna is the list that contains markup and markupless
        self.lna = []
        self.lnawrong = []
        # wordcount contains wordcount for both versions of file
        self.wordcount = []
        # linkcount contains number of internal/external links in each articles
        self.linkcount = []
        self.egonum = []
        
    def get_lna(self): 
        for item in self.raw:
            src = r'/Users/Mathilda/Documents/workspace/WikiHoax/source/m30/' + item[0] + '.html'
            try:
                with open(src,'r') as f:
                    text = f.read()
                    text.replace('\n', ' ') 
                    p = wikip.to_raw_text_markupless(text, keep_whitespace=False, normalize_ascii=False)
                    self.lna.append([text, p])
            except:
                self.lnawrong.append(item)
                self.raw.remove(item)
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
                
    def get_wordcount(self):
        tokenizer = RegexpTokenizer(r'\w+')
        for item in self.lna:
            self.wordcount.append([len(word_tokenize(item[0].decode('utf-8'))),len(tokenizer.tokenize(item[1]))])
    
         
    def get_linkcount(self):
        for item in self.lna:
            wikilink = len(re.findall(r'\[\[.+?\]\]',item[0]))
            url = len(re.findall(r'url',item[0]))
            self.linkcount.append([wikilink,url+wikilink])
    
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
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                