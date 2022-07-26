import uvicorn
from decouple import config

HOST = config("HOST")
PORT = config("PORT", default=8000, cast=int)
DEBUG = config("DEBUG", default=False, cast=bool)

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=DEBUG)

# @josdanind
# Twitter Project - Platzi
