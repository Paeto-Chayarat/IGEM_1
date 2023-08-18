from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import config
from pymongo.mongo_client import MongoClient
import json
from pprint import pprint

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(config.MONGO_URI)
db = client.prediction_backend
collection = db.sequences

# How to start server with debug console:
# uvicorn app.main:app --reload


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.post("/sequences")
async def add_sequences(request: Request):
    data = await request.json()

    res = collection.insert_many([data])

    # test if the length of the inserted_ids list is greater than 0
    if len(res.inserted_ids) > 0:
        return True
    else:
        return False


@app.post("/add_task")
async def add_task(request: Request):
    data = await request.json()
    print(data)

    file = open("input_folder/" + data["name"], "w")
    file.write(data["file"])
    file.close()
    return True
