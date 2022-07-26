# FastAPI
from fastapi import FastAPI
from routers import api

# Environment Variables
from config import APP_VERSION

# Database
from database import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTI - Trading Bot", version=APP_VERSION)
app.include_router(api)


@app.on_event("startup")
def startup():
    print("Welcome to OTI")
