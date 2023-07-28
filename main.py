from fastapi import Body, FastAPI, Path, Query  # Query() object modifies the info in the /docs panel
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    name: str
    pwd: str

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
async def mq(q: Annotated[ str | None , Query(title="title", description="des", alias="m-q", min_length=3)]):
    result = {}
    if q:
        result.update({"q": q})
    return result

# Query(alias=) is for /docs panel to describe the param, in the following case is "q"
@app.get('/mq1/{m_q}')
# the /docs panel will display all params in the routing function's signature
# You cant have "async def mq( m-q : ..."
# as "m-q" is not a valid variable name in python
# but if you like to have m-q displayed in the /docs panel, use alias= in the Query()
async def mq(q: Annotated[ str | None , Query(title="title", description="des", deprecated=True, min_length=3)]):
    return q

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get('/plain')
async def get_Plain():
    return 'amogus'

@app.get('/hidden')
async def hidden(
    # not suggested (but valid) => hidden_param: Annotated[str|None, Query(include_in_schema=False)],
    # required but hidden param(s) may cost development problem
    hidden_param: Annotated[str|None, Query(include_in_schema=False)] = None,
    shown:  Annotated[str|None, Query()] = None
):
    result = {
        "shown": shown,
        "hide_params": hidden_param
    }
    return result

@app.get('/path/{test}')
async def path_test(
    # test: Annotated[ str| None, Path()],    # required
    test: Annotated[ int , Path(ge=1)],
    q: Annotated[ str | None, Query()] = None,
):
    return {test: q}

@app.post('/mbp/{item_id}')
async def mbp(
    item_id: Annotated[ int, Path()],
    item: Item,
    user: User,
    importance: Annotated[ int | None, Body()] = 0
):
    return { 
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }