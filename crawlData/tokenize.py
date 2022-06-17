df = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/data.csv")
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

df.to_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/dataTokenize.csv")
