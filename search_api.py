from cmath import isnan
from fastapi import FastAPI
from crawlData.searching import fullTextSearch
import json

app = FastAPI()


# @app.get("/users/me") # <- here
# async def read_user_me():
#     return {"user_id": "the current user"}
def isNaN(num):
    return num!= num

@app.get("/{user_id}") # <- and here
async def read_user(user_id: str):
    list_a = fullTextSearch(user_id)[0]
    list_b = []
    label = ['link', 'phone_name', 'price', 'image', 'branch', 'chip', 'ram', 'rom']
    print(len(list_a))
    for a in list_a:
        dict2 = {}
        for i in range(0, 8):
            if isNaN(a[0][i+1]):
                dict2[label[i]]='No information'
            else:
                dict2[label[i]]=a[0][i+1]
        list_b.append(dict2)
    print(len(list_b))
    print(list_b)
    return list_b, {"query": fullTextSearch(user_id)[1]}
    # print(list_a)
