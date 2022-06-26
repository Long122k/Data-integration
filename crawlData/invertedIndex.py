import pandas as pd
import csv
import numpy as np

df = pd.read_csv("crawlData/Data/dataTokenize.csv")
demo = np.array(df['title'])

num = len(demo)

dict = {}

for i in range(0, num):
    try:
        chain = demo[i].split(' ')
    except:
        break
    for token in chain:
        if not token in dict:
            dict[token] = (i,)
        else:
            dict[token] = dict[token] + (i,)
    
with open('crawlData/Data/invertedIndex.csv', 'w') as f:
    writer = csv.DictWriter(f, ['token', 'index'])
    writer.writeheader()
    for key in dict:
        writer.writerow({'token': key, 'index': dict[key]})
        