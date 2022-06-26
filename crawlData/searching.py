import csv
from pyvi import ViTokenizer

reader = csv.DictReader(open("crawlData/Data/invertedIndex.csv"))

dict = {}
for raw in reader:
    dict = raw

def fullTextSearch(input):
    text = input.lower()
    text = ViTokenizer.tokenize(text).split(' ')
    print(dict[text[1]], type(dict[text[1]]))
    set = set(dict[text[1]])
    print(set, type(set))


text = "Điện thoại iphone 13"
fullTextSearch(text)