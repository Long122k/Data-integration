import csv
from operator import index
from textwrap import indent
import pandas as pd
import numpy as np
from pyvi import ViTokenizer
from sympy import re


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

def fullTextSearch(input):
    reader = csv.DictReader(open("crawlData/Data/invertedIndex.csv"))
    dict = {}
    for raw in reader:
        dict = raw

    input = input.lower()
    text = []
    for token in input.split(' '):
        if token != '':
            text.append(token)

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

    print(textCorrect)

    return getDataByIndex(indexs), textCorrect


def getDataByIndex(indexs):
    df = pd.read_csv("crawlData/Data/Data.csv")
    list1 = []
    for idx in indexs:
        idx = int(idx)
        list1.append(df[idx:(idx+1)])
    
    #print(np.array(list1[0:(len(list1)-1)]))
    print(len(list1))
    return np.array(list1[0:(len(list1))])


text = "  điện   thoạt xamxung  "
fullTextSearch(text)