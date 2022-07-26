from datetime import datetime

# SQLAlchemy
from tokenize import Token
from sqlalchemy.orm import Session
from database.models import User, Trader

# Schemas
from schemas import UserInDB, Login, TraderInDB, UserResponse
from schemas import TraderResponse, TradeOut, TraderUpdate


# Database Queries
from database.queries import check_existence, write_row, delete_row, get_all
from database import models
from schemas.user import UserOut, UserUpdate

# Utils
from utils.encrypt_password import context
from utils.http_errors import incorrect_password, no_permissions
from utils.OAuth import decode_access_token


# -------
#  UTILS
# -------
def validate_user(db: Session, token: Token):
    payload = decode_access_token(token)
    is_trader = True if payload.get("access_level") else False

    model = "Trader" if is_trader else "User"
    key = "id"
    value = payload["id"]

    return check_existence(db, model, error_message="User don't  Exists!", id=value)


def check_permits(db: Session, token: Token, access_level) -> None:
    db_user = validate_user(db, token)

    if type(db_user) == models.Trader:
        level = db_user.trader_data["access_level"]

        if level <= access_level:
            return
    else:
        raise no_permissions


def response_model(db_user):
    user_dict = db_user.__dict__
    user_dict.pop("_sa_instance_state")

    if type(db_user) == models.Trader:
        return TraderResponse(**user_dict)
    else:
        return UserResponse(**user_dict)


# ---------
#  QUERIES
# ---------

# --// JWT LOGIN
def login_user(db: Session, login: Login, is_trader: bool):

    model = "Trader" if is_trader else "User"

    db_user = check_existence(
        db,
        model=model,
        error_message="User don't Exist!",
        **{"username": login.username},
    )

    if context.verify(login.password, db_user.hashed_password):
        db_user.message = "Login Success!"
        return db_user
    else:
        raise incorrect_password


# --// CREATE A USER
def create_user(
    db: Session, token: Token, userModel: UserInDB | TraderInDB
) -> User | Trader:
    check_permits(db, token, 1)

    model = type(userModel).__name__.replace("InDB", "")

    conditions = [
        ("username", "The user exists!"),
        ("email", "There is a user with that email!"),
    ]

    for field, message in conditions:
        check_existence(
            db,
            model=model,
            error_message=message,
            error_if_exist=True,
            **{f"{field}": eval(f"userModel.{field}")},
        )

    user_dict = userModel.dict()
    user_dict["hashed_password"] = user_dict.pop("password")

    if model == "User":
        user_dict["user_data"]["birth_date"] = str(user_dict["user_data"]["birth_date"])
    else:
        user_dict["trader_data"]["birth_date"] = str(
            user_dict["trader_data"]["birth_date"]
        )

    db_user = write_row(db, model, with_dict=user_dict)

    user_schema = response_model(db_user)
    user_schema.message = "The user was created"
    return user_schema


# --// GET A USER
def get_user(db: Session, token: Token, username: str, db_traders: bool):
    if db_traders:
        check_permits(db, token, 1)
        model = "Trader"
        is_trader = True
    else:
        db_user = validate_user(db, token)
        model = "User"
        is_trader = type(db_user) == models.Trader

    if db_user.username == username or is_trader:
        db_user = check_existence(
            db,
            model=model,
            error_message="User don't Exist!",
            **{"username": username},
        )
        db_user.message = "User Exists!"
        return response_model(db_user)
    else:
        raise no_permissions


# --// GET ALL USERS
def get_all_users(db: Session, token: Token, page: str, limit: str, db_traders: bool):
    check_permits(db, token, 1)
    model = "Trader" if db_traders else "User"

    db_users = get_all(db, model, skip=page, limit=limit)

    response = []

    for user in db_users:
        user_dict = user.__dict__
        user_dict.pop("_sa_instance_state")

        if model == "User":
            response.append(UserOut(**user_dict))
        else:
            response.append(TradeOut(**user_dict))

    return response


# --// DELETE A USER
def delete_user(db: Session, token: Token, username: str, rol: bool):
    check_permits(db, token, 1)

    model = "Trader" if rol else "User"

    db_user = check_existence(
        db, model, error_message="User don't  Exists!", **{"username": username}
    )

    delete_row(db, model, id=db_user.id)
    db_user.message = "The user was deleted!"

    return response_model(db_user)


# --// UPDATE A USER
def update_user(
    db: Session,
    token: Token,
    toUpdate: UserUpdate | TraderUpdate,
    username: str,
):
    check_permits(db, token, 1)

    db_traders = type(toUpdate) == TraderUpdate
    model = "Trader" if db_traders else "User"

    db_user = check_existence(
        db, model, error_message="User don't  Exists!", **{"username": username}
    )

    to_update = toUpdate.dict()

    user_data = ["first_name", "last_name", "birth_date"]
    trader_data = user_data + ["position", "access_level"]

    data = trader_data if model == "Trader" else user_data

    for k in to_update.keys():
        value = to_update[k]

        if value:
            if k in data:
                if model == "Trader":
                    exec(f"db_user.trader_data['{k}'] = '{value}'")
                else:
                    exec(f"db_user.user_data['{k}'] = '{value}'")

            if k != "password" and not k in data:
                exec(f"db_user.{k} = '{value}'")

            if k == "password":
                db_user.set_password(value)

    db_user.updated_at = datetime.now()

    db_user = write_row(db, "Trader", withModel=db_user)
    db_user.message = "The user data was updated!"

    return db_user
