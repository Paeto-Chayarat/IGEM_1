import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from config import config

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URI)
db = client.college


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Sequence(BaseModel):
    name: str = Field(...)
    value: str = Field(...)


class Sequences(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    seqs: Sequence = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # json_schema_extra = {
        #     "seqs": [
        #         {"name": "DNA1", "value": "ATGCGATTACG"},
        #         {"name": "DNA2", "value": "GGTAACTCGTA"},
        #     ]
        # }


# class UpdateStudentModel(BaseModel):
#     name: Optional[str]
#     email: Optional[EmailStr]
#     course: Optional[str]
#     gpa: Optional[float]

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "name": "Jane Doe",
#                 "email": "jdoe@example.com",
#                 "course": "Experiments, Science, and Fashion in Nanophotonics",
#                 "gpa": "3.0",
#             }
#         }


@app.post("/add", response_description="Add new student", response_model=Sequences)
async def create_student(data: Sequences = Body(...)):
    json_data = jsonable_encoder(data)
    new_patient = await db["prediction_backend"].insert_one(json_data)
    created_patient = await db["prediction_backend"].find_one(
        {"_id": new_patient.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_patient)


# @app.get(
#     "/", response_description="List all students", response_model=List[StudentModel]
# )
# async def list_students():
#     students = await db["students"].find().to_list(1000)
#     return students


# @app.get(
#     "/{id}", response_description="Get a single student", response_model=StudentModel
# )
# async def show_student(id: str):
#     if (student := await db["students"].find_one({"_id": id})) is not None:
#         return student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.put("/{id}", response_description="Update a student", response_model=StudentModel)
# async def update_student(id: str, student: UpdateStudentModel = Body(...)):
#     student = {k: v for k, v in student.dict().items() if v is not None}

#     if len(student) >= 1:
#         update_result = await db["students"].update_one({"_id": id}, {"$set": student})

#         if update_result.modified_count == 1:
#             if (
#                 updated_student := await db["students"].find_one({"_id": id})
#             ) is not None:
#                 return updated_student

#     if (existing_student := await db["students"].find_one({"_id": id})) is not None:
#         return existing_student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.delete("/{id}", response_description="Delete a student")
# async def delete_student(id: str):
#     delete_result = await db["students"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


## old

# from fastapi import FastAPI, HTTPException, Header
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic_settings import BaseSettings
# from typing import Dict
# from config import config
# from pymongo.mongo_client import MongoClient
# from fastapi import UploadFile, File
# from typing import List
# import bson
# import json

# app = FastAPI()

# origins = ["http://localhost:3000"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# client = MongoClient(config.MONGO_URI)


# db = client["prediction_backend"]
# collection = db["sequences"]


# # class PyObjectId(ObjectId):
# #     @classmethod
# #     def __get_validators__(cls):
# #         yield cls.validate

# #     @classmethod
# #     def validate(cls, v):
# #         if not ObjectId.is_valid(v):
# #             raise ValueError("Invalid objectid")
# #         return ObjectId(v)

# #     @classmethod
# #     def __modify_schema__(cls, field_schema):
# #         field_schema.update(type="string")


# # class Sequence(BaseModel):
# #     name: str
# #     value: str


# # class Sequences(BaseModel):
# #     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
# #     seqs: List[Sequence]


# @app.get("/")
# def hello_world():
#     return {"Hello": "World"}


# @app.post("/sequences")
# def add_sequences(data: dict):
#     b = bson.encode(data)
#     collection.insert_one(b)
#     return b


# # @app.get("/addition")
# # def get_addition(variable_1: str, variable_2: str):
# #     variable_1_list = list(collection.find({"name": variable_1}))
# #     variable_2_list = list(collection.find({"name": variable_2}))
# #     result = 0
# #     if len(variable_1_list) != 0:
# #         result = result + variable_1_list[0]["value"]

# #     if len(variable_2_list) != 0:
# #         result = result + variable_2_list[0]["value"]
# #     return {"result": result}


# # @app.post("/uploadTask")
# # async def getTask(file: UploadFile = File(...)):
# #     prediction_task = await file.read()
# #     data = json.loads(prediction_task)
# #     task_list = list.append(prediction_task)
# #     result = collection.insert_many([task_list])
# #     return {"inserted_ids": result}


# # i cant make it work with  json file as arrays


# # task_list = []
# # task_list = list.append(prediction_task)
