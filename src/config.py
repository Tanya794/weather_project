import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    CITY = "Moscow"

    # Database
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
    }
