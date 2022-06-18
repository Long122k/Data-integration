import pandas as pd

df = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/Data/data.csv")
contents = df['title']

from pyvi import ViTokenizer
for id, content in enumerate(contents):
  try: 
    tmp = ViTokenizer.tokenize(content)
    contents[id] = tmp
  except:
    content = None

contents = df['chip']
for id, content in enumerate(contents):
  try: 
    tmp = ViTokenizer.tokenize(content)
    contents[id] = tmp
  except:
    content = None

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
df = df[list]

df.to_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/Data/dataTokenize.csv")
