# Python
from datetime import datetime
from email.policy import default

# Utils
from utils.encrypt_password import context

# SQLAlchemy
from sqlalchemy import (
    Column,
    ForeignKey,
    Identity,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
)
from sqlalchemy_json import MutableJson
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    user_data = Column(MutableJson, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime)

    def set_password(self, password):
        self.hashed_password = context.hash(password)


class Trader(Base):
    __tablename__ = "traders"

    username = Column(String(50), primary_key=True, unique=True, nullable=False)
    id = Column(Integer, Identity(start=1, cycle=True))
    email = Column(String(50), unique=True, nullable=False)
    trader_data = Column(MutableJson, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime)

    def set_password(self, password):
        self.hashed_password = context.hash(password)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ticker = Column(String(10), unique=True, nullable=False)
    amount = Column(Float)
    order_id = Column(ForeignKey("orders.id"))
    user_id = Column(ForeignKey("users.id"))


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    t_operation = Column(String(10), unique=True, nullable=False)


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    entries = Column(MutableJson, nullable=False)
    take_profit = Column(MutableJson, nullable=False)
    stop_loss = Column(Integer, unique=True, nullable=False)
    t_assets = Column(Integer, nullable=False)
    t_inversion = Column(Integer, nullable=False)
    f_loss = Column(Integer, nullable=False)
    f_profif = Column(Integer, nullable=False)
    f_assets = Column(Integer, nullable=False)
    loss = Column(Integer, nullable=False)
    profif = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    trader_id = Column(ForeignKey("traders.username"))
    operation_id = Column(ForeignKey("operations.id"))
