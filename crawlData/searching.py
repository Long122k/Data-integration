import csv
from operator import index
from textwrap import indent
import pandas as pd
import numpy as np
from pyvi import ViTokenizer
from sympy import re

MAX_N = 20

def calJaccardMeasure(s1, s2):
    s1 = '#'+s1+'#'
    s2 = '#'+s2+''
    set1 = set()
    set2 = set()

    for i in range(len(s1)-1):
        set1.add(s1[i:(i+2)])

    for i in range(len(s2)-1):
        set2.add(s2[i:(i+2)])
    
    return (len(set1 & set2) / len(set1 | set2))

def spellingCorrection(dict, string):
    dist = -1
    result = ''
    for key in dict:
        tmp = calJaccardMeasure(key, string)
        if tmp > dist:
            dist = tmp
            result = key
    return result 

def convertStringToSet(dict, token):
    if not token in dict:
        return set()
    tmp = dict[token].replace('[', '').replace(']', '').replace(',', '').split(' ');
    return set(tmp)

def fullTextSearch(input, decrease = False):
    reader = csv.DictReader(open("crawlData/Data/invertedIndex.csv"))
    dict = {}
    for raw in reader:
        dict = raw

    text = input.lower()
    text = input.split()

    tmp = text[0]
    if not tmp in dict:
        tmp = spellingCorrection(dict, tmp)
    
    indexs = convertStringToSet(dict, tmp)

    textCorrect = ''

    for token in text:
        if not token in dict:
            token = spellingCorrection(dict, token)
        textCorrect = textCorrect + ' ' + token
        list = convertStringToSet(dict, token)
        indexs = indexs & list

    if len(indexs) > MAX_N:
        indexs = getTopResult(indexs, text)

    data = getDataByIndex(indexs)
    return sortListResult(data), textCorrect


def getDataByIndex(indexs):
    df = pd.read_csv("crawlData/Data/Data.csv")
    list1 = []
    for idx in indexs:
        idx = int(idx)
        list1.append(df[idx:(idx+1)])
    
    #print(np.array(list1[0:(len(list1)-1)]))
    #   print(len(list1))
    return np.array(list1[0:(len(list1))])

def getTopResult(indexs, text):
    tf_idf = pd.read_csv('crawlData/Data/tf_idf.csv')
    list = []
    for idx in indexs:
        rank = 0
        for token in text:
            try:
                rank += tf_idf[token][idx:(idx+1)]
            except:
                rank -= 0.1
        list.append(rank)
    
    arr = []
    for i in range(len(list)): 
        arr.append((list[i], i))

    def take_first(item):
        return item[0]

    sorted_list = sorted(arr, key=take_first, reverse=True)

    listIndex = []
    for idx in indexs:
        listIndex.append(idx)
    
    arr2 = []
    for idx in range(MAX_N):
        item = sorted_list[idx]
        arr2.append(listIndex[item[1]])

    return arr2
    

def getNumber(string): 
    number = '';
    for c in string:
       if c.isnumeric():
            number = number + c;

    return int(number)

def sortListResult(data, decrease = True):
    def get_price(item):
        return getNumber(item[0][3]) #price

    sorted_list = sorted(data, key=get_price, reverse=decrease)
    return sorted_list

text = "  điện   thoạt  xamxung  "
print(fullTextSearch(text))