import pandas as pd

data1 = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/NguyenKim.csv")
data2 = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/CellPhones.csv")
data3 = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/Didongthongminh.csv")
data4 = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/hoanghamobile.csv")
data5 = pd.read_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/thegioididong.csv")

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
df1 = data1[list]
df2 = data2[list]
df3 = data3[list]
df4 = data4[list]
df5 = data5[list]

df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
print(df)
df.to_csv("/Users/lap60570/Documents/HUST/20212/Tích hợp dữ liệu/BTL/CrawlData/data.csv")


