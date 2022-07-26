# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Base Schema
from .base import OrmActive, PersonalInformation


class TraderData(PersonalInformation):
    position: str
    access_level: int


class TradeOut(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    trader_data: TraderData


class TraderInDB(TradeOut):
    password: str = Field(min_length=8)


class TraderResponse(OrmActive, TradeOut):
    id: int
    message: str | None = None


class TraderUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    # trader_data
    first_name: str | None = None
    last_name: str | None = None
    birth_date: str | None = None
    position: str | None = None
    access_level: int | None = None
