import pandas as pd
import numpy as np

files = ['24hstore', 'CellPhones', 'clickbuy', 'didongmango', 'Didongthongminh', 'didongviet', 
        'hnammobile', 'hoanghamobile', 'NguyenKim', 'thegioididong', 'digiphone', 'mediamart', 'mobilecity', 'viettelstore']

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']

df = []
for file in files:
    data = pd.read_csv('crawlData/rawData/'+file+'.csv')
    print(data.shape)
    df.append(data[list])

df = pd.concat(df, ignore_index=True)
print(df.shape)
df.to_csv("CrawlData/Data/data.csv")