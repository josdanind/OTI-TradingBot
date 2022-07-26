# Python
from datetime import datetime, timedelta

# PyJWT
import jwt

# FastAPI
from fastapi.security import OAuth2PasswordBearer

# Models
from database import models

# Environment Variables
from config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, APP_VERSION

# Utils
from utils.http_errors import token_invalid

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"/api/v{APP_VERSION}/users/login")


def create_access_token(
    db_user: models.User, expire_days: timedelta = timedelta(ACCESS_TOKEN_EXPIRE_DAYS)
):
    payload = {
        "id": db_user.id,
        "username": db_user.username,
        "exp": datetime.utcnow() + expire_days,
        "iat": datetime.utcnow(),
    }

    is_trader = type(db_user) == models.Trader

    if is_trader:
        payload["access_level"] = db_user.trader_data["access_level"]

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if payload is None:
            raise token_invalid

        return payload
    except jwt.DecodeError:
        print("JWT Error")
        return None
