import pandas as pd
import csv
import numpy as np

df = pd.read_csv('crawlData/Data/newData.csv')
demo = np.array(df['title'])

num = len(demo)
dict = {}

for i in range(0, num):
    try:
        chain = (demo[i].lower()).split(' ')
    except:
        continue
    for token in chain:
        if not token in dict:
            dict[token] = [i]
        else:
            dict[token].append(i)
    
keys = [key for key in dict]
print(len(keys))

with open('crawlData/Data/invertedIndex.csv', 'w') as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerow(dict)
        