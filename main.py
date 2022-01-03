# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(...,min_length=1,max_length=50,example="Pasto")
    state: str = Field(...,min_length=1,max_length=50,example="Nariño")
    country: str = Field(...,min_length=1,max_length=50,example="Colombia")

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Andres"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Insuasty Delgado"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example = 26
        )
    hair_color: Optional[HairColor] = Field(default=None,example="Black")
    is_married: Optional[bool] = Field(default=None,example=False)

    # class Config:
    #     schema_extra = {
    #         "example":{
    #             "first_name":"Andres",
    #             "last_name":"Insuasty Delgado",
    #             "age":21,
    #             "hair_color":"brown",
    #             "is_married":False
    #         }
    #     }


@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, 
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's requerid"
        )
):
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person Id, It's an integer"
        )
):
    return {person_id: "It exist"}

# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
        ),
        person:Person = Body(...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results