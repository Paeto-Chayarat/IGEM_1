from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import Dict
from config import config
from pymongo.mongo_client import MongoClient

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
db = client["calculator"]
collection = db["variable"]


class Variable(BaseSettings):
    name: str
    value: int


@app.get('/')
def hello_world():
    return {"Hello": "World"}


@app.post('/variable')
def post_variable(variable: Variable):
    data = {"name": variable.name, "value": variable.value}
    result = collection.insert_many([data])
    return {variable.name: variable.value}


@app.get('/addition')
def get_addition(variable_1: str, variable_2: str):
    variable_1_list = list(collection.find({"name": variable_1}))
    variable_2_list = list(collection.find({"name": variable_2}))
    result = 0
    if len(variable_1_list) != 0:
        result = result + variable_1_list[0]["value"]

    if len(variable_2_list) != 0:
        result = result + variable_2_list[0]["value"]
    return {"result": result}
