'''
Created on Jan 9, 2018

@author: Mathilda
'''
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
import random
from sklearn import tree
from sklearn.svm import SVC

from Hoax import *
from Genius import *
import os; 
if __name__ == '__main__':
    
#     print(os.path.abspath(os.getcwd()))
    
    genius = GeniusInfo()
    genius.get_all()
    hoax = HoaxInfo()
    hoax.get_all()
    
    
    dataset = []
    for wc, lc, en in zip (hoax.wordcount, hoax.linkcount, hoax.egonum):
        dataset.append([1, wc[1]/float(wc[0]), wc[1],lc[0],lc[1],en])

        
    for wc, lc, en in zip (genius.wordcount, genius.linkcount, genius.egonum):
        dataset.append([0, wc[1]/float(wc[0]), wc[1],lc[0],lc[1],en])    
       
    random.shuffle(dataset)
    print('\n\n\n data finished')
    print (dataset)
    print('\n\n\n\n')
    X = []
    y = []
    for item in dataset:
        X.append(item[1:])
        y.append(item[0])
    
    print (X)
    print (y)
    scores = [] 
    clf = GaussianNB()
    scores.append(['Gaussioan', cross_val_score(clf, X, y, cv=10)])
    clf = tree.DecisionTreeClassifier()
    scores.append(['Tree', cross_val_score(clf, X, y, cv=10)])
#     clf = SVC(kernel='linear', C=1)
#     scores.append(['SVC', cross_val_score(clf, X, y, cv=10)])
    print(scores)