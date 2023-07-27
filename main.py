from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    print(item_dict)
    if item.tax:
        pt = item.price + item.tax
        item_dict.update({"pt":pt})
    return item_dict

@app.put('/items/{item_id}')
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {
        "item_id": item_id, 
        **item.dict()
    }
    if q:
        result.update({"q": q})
    return result

@app.get('/')
async def root():
    return {"message":"hello world"}

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=5)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get('/items/{item_id}')
async def getItem(item_id: int):
    return {
        "id": item_id,
    }

@app.get('/mq')
async def mq(q: Annotated[list[str]| None , Query()] = ["suka"]):
    return q

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get('/plain')
async def get_Plain():
    return 'amogus'