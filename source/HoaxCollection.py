'''
Created on Jan 9, 2018

@author: Mathilda
'''

import xml.etree.ElementTree as ET
from datetime import datetime


def get_abstract():
    newarticles = []
    tree = ET.parse('./deletionpediaorg_w-20171214-wikidump/deletionpediaorg_w-20171214-history.xml')
    root = tree.getroot()
    for page in root.findall('page'):
        text = page.find('revision').find('text').text
        pagen = page.find('title').text.replace('/','')
        pagename = './wikihoax/' + pagen + '.html'
        if text is not None:
            with open(pagename,'w') as f:
                f.write(text.encode('utf-8'))
            rev = len(page.findall('revision'))
            author = page.find('revision').find('contributor').find('username').text
            timestamp = page.find('revision').find('timestamp').text
            if rev > 1:
                end = page.findall('revision')[rev-1].find('timestamp').text
                newarticles.append([pagen,rev,author,timestamp,end])
            else: 
                newarticles.append([pagen,rev,author,timestamp,timestamp])
    return newarticles


def get_formatted_date(newarticles):
    m30 = []
    dateformat = '%Y-%m-%d/%H:%M:%S'
    for item in newarticles:
        date1 = datetime.strptime(item[3], dateformat)
        date2 = datetime.strptime(item[4], dateformat)
        if (date2-date1).days >= 30:
            m30.append(item)
    return m30


def save_docs(m30):
    for item in m30:
        with open('m30.txt','a') as f:
            f.write(', '.join(item).encode('utf-8'))
            f.write('\n')

def read_in_m30():
    m30 = []
    with open(r'/Users/Mathilda/Documents/workspace/WikiHoax/source/ m30.txt','r') as f:
        for line in f:
            m30.append(line.split(','))
    return m30
    
     
def get_datedict(m30):
    datedict = {}
    for item in m30:
        if item[3][:10] not in datedict:
            datedict[item[3][:10]] = 1
        else:
            datedict[item[3][:10]] += 1
    return datedict