import pandas as pd

df = pd.read_csv("crawlData/Data/Data.csv")
contents = df['title']

from pyvi import ViTokenizer
for id, content in enumerate(contents):
  try: 
    tmp = ViTokenizer.tokenize(content.lower())
    contents[id] = tmp
  except:
    content = None

contents = df['chip']
for id, content in enumerate(contents):
  try: 
    tmp = ViTokenizer.tokenize(content.lower())
    contents[id] = tmp
  except:
    content = None

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
df = df[list]

df.to_csv("crawlData/Data/dataTokenize.csv")
