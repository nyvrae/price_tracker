import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///price_tracker.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "25c33844187486fcc29d482605ebe8695d68767898ef19807536552b1252a699") # openssl rand -hex 32
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()