from cmath import isnan
from xmlrpc.client import boolean
from fastapi import FastAPI
from crawlData.searching import fullTextSearch
import json
from pydantic import BaseModel

class Item(BaseModel):
    name: str

app = FastAPI()


# @app.get("/users/me") # <- here
# async def read_user_me():
#     return {"user_id": "the current user"}
def isNaN(num):
    return num!= num

# @app.get("/{name}") # <- and here
# async def read_user(name: str):
#     # name = name.encode('utf-8')
#     list_a = fullTextSearch(name)[0]
#     list_b = []
#     label = ['link', 'phone_name', 'price', 'image', 'branch', 'chip', 'ram', 'rom']
#     print(len(list_a))
#     for a in list_a:
#         dict2 = {}
#         for i in range(0, 8):
#             if isNaN(a[0][i+2]):
#                 dict2[label[i]]='No information'
#             else:
#                 dict2[label[i]]=a[0][i+2]
#         list_b.append(dict2)
#     # print(len(list_b))
#     # print(list_b)
#     return list_b, {"query": fullTextSearch(name)[1]}
#     # print(list_a)

@app.post("/") # <- and here
async def search_phone(item: Item):
    print(item.name)

    list_a = fullTextSearch(item.name)[0]
    list_b = []
    label = ['link', 'phone_name', 'price', 'image', 'branch', 'chip', 'ram', 'rom']
    print(len(list_a))
    for a in list_a:
        dict2 = {}
        for i in range(0, 8):
            if isNaN(a[0][i+2]):
                dict2[label[i]]='No information'
            else:
                dict2[label[i]]=a[0][i+2]
        list_b.append(dict2)
    print(len(list_b))
    return list_b, {"query": fullTextSearch(item.name)[1]}
    # return {"name": item.name}
