import pandas as pd
import numpy as np
from sympy import re

files = ['24hstore', 'CellPhones', 'clickbuy', 'didongmango', 'Didongthongminh', 'didongviet', 
        'hnammobile', 'hoanghamobile', 'NguyenKim', 'thegioididong']

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
df = []

def getPathImg(list):
    newList = []
    for path in list:
        try:
            path = path.replace('{', '').replace('}','').replace(',','').split(' ')[0].replace('\'', '')
        except:
            print(path)
        newList.append(path)
    return newList
    

for file in files:
    data = pd.read_csv('crawlData/rawData/'+file+'.csv')
    data['pathImg'] = getPathImg(data['pathImg'])
    df.append(data[list])

df = pd.concat(df, ignore_index=True)
df.to_csv('crawlData/Data/Data.csv')


