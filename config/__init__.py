from decouple import config

# APP
APP_VERSION = config("APP_VERSION")

# Uvicorn settings
HOST = config("HOST", cast=str, default="localhost")
PORT = config("PORT", cast=int, default=8000)
DEBUG = config("DEBUG", cast=bool, default=True)

# Postgres
DB_USER = config("DB_USER")
DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")

# JWT
JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = config("ACCESS_TOKEN_EXPIRE_DAYS", cast=int)

# Binance
API_KEY = config("API_KEY")
API_SECRET_KEY = config("API_SECRET_KEY")
