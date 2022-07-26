# FastAPI
from fastapi import APIRouter, Depends, status, Body, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

#  Database
from sqlalchemy.orm import Session
from database import SessionLocal

from .db import login_user, create_user, delete_user
from .db import get_user, get_all_users, update_user


# Utils
from utils.OAuth import create_access_token, oauth2_schema

# Schemas
from schemas import UserInDB, Login, Token
from schemas import TraderUpdate, TraderInDB, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------
#  Login JWT to account
# ----------------------
@router.post(path="/login", response_model=Token, status_code=status.HTTP_200_OK)
async def user_auth(
    db: Session = Depends(get_db),
    login: OAuth2PasswordRequestForm = Depends(),
    is_trader: bool = Query(default=False),
):
    credentials = Login(username=login.username, password=login.password)

    db_user = login_user(db, credentials, is_trader)

    return {"access_token": create_access_token(db_user), "token_type": "Bearer"}


# ------------
#  Get a user
# ------------
@router.get(
    path="/{username}",
    status_code=status.HTTP_200_OK,
    summary="Get a User",
)
async def get_a_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    username: str = Path(...),
    db_traders: bool = Query(default=False),
):

    return get_user(db, token, username, db_traders)


# --------------
#  Get all user
# --------------
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get Users",
)
async def get_users(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    page: int = Query(default=0),
    limit: int = Query(default=10),
    db_traders: bool = Query(default=False),
):
    users = get_all_users(db, token, page, limit, db_traders)

    return users


# ------------------
#  Signup a account
# ------------------
@router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
)
async def sign_up(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    userRequest: UserInDB | TraderInDB = Body(...),
):
    return create_user(db, token, userRequest)


# ----------------
#  Update user
# ----------------
@router.put(
    path="/update/user/{username}",
    status_code=status.HTTP_200_OK,
    summary="update a user's information",
)
async def update_data_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    userRequest: UserUpdate = Body(...),
    username: str = Path(...),
):
    return update_user(db, token, userRequest, username)


# ----------------
#  Update Trader
# ----------------
@router.put(
    path="/update/trader/{username}",
    status_code=status.HTTP_200_OK,
    summary="update a user's information",
)
async def update_data_trader(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    userRequest: TraderUpdate = Body(...),
    username: str = Path(...),
):
    return update_user(db, token, userRequest, username)


# --------------
# Delete a users
# --------------
@router.delete(
    path="/delete/{username}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
)
async def user_delete(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
    username: str = Path(...),
    db_traders: bool = Query(default=False),
):

    return delete_user(db, token, username, db_traders)
