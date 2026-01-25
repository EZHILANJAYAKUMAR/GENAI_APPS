import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ## GROQ and Model configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")

    ## Database configuration
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

config = Config()