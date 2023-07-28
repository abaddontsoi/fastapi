from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Annotated
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://guest:guest@cluster0.f3jexph.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

class Booking(BaseModel):
    bkNum: str
    PlaneNum: str
    passangerName: str
    contactNum: str
    age: int
    totalCost: float | None

bkCol = client["Booking"]["bk01"]

class Captain(BaseModel):
    id: str
    name: str
    age: int

capCol = client['Captain']['cap01']

class Flight(BaseModel):
    flightId: str
    flightName: str | None
    seats: list[int]
    captains: list[Captain]

fCol = client['Flight']['f01']

class Account(BaseModel):
    id: str
    name: str
    age: int
    contactNum: str

# create booking
@app.post('/booking')
async def createBk(
    booking: Booking
):
    try:
        bkCol.insert_one(booking.dict())
        return "success"
    except Exception as e:
        return e


# read booking
@app.get('/booking')
async def getBk(
    bkid: Annotated[ str , 
        Query(
            # max_length=8, 
            # min_length=8
        )
    ]
):
    result = bkCol.find_one({
            "bkNum": bkid
        }
    )
    print(result)
    return {
        'bkNum': result['bkNum'], 
        'PlaneNum': result['PlaneNum'], 
        'passangerName': result['passangerName'], 
        'contactNum': result['contactNum'], 
        'age': result['age'], 
        'totalCost': result['totalCost']
    }

# update booking
@app.put('/booking')
async def updateBk(
    bknum: Annotated[ str, Query(
        # max_length=8, 
        # min_length=8
        )
    ],
    info: Booking
):
    target = bkCol.find_one_and_replace({
        "bkNum": bknum
    }, info.dict())


# delete booking
@app.delete('/booking')
async def deleteBk(
    bknum: Annotated[ str, Query(
        # max_length=8,
        # min_length=8
    )],
    # info: Booking,
    confirmCode: Annotated[str, Query()]    
):
    target = bkCol.find_one_and_delete({
        "bkNum": bknum
    })

# create accounts
@app.post('/account')
async def createAc(

):
    ...
# read accounts
# update accounts
# delete accounts

# create flights
# read flights
# update flights
# delete flights
