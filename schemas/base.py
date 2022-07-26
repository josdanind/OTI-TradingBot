# Python
from datetime import date

# Pydantic
from pydantic import BaseModel, Field


class OrmActive(BaseModel):
    class Config:
        orm_mode = True


class PersonalInformation(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    birth_date: date


class Login(BaseModel):
    username: str
    password: str
