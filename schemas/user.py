# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Base Schema
from .base import OrmActive, PersonalInformation


class UserOut(BaseModel):
    id: str
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    user_data: PersonalInformation


class UserInDB(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    user_data: PersonalInformation


class UserResponse(OrmActive, UserOut):
    message: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    # user_data
    first_name: str | None = None
    last_name: str | None = None
    birth_date: str | None = None
