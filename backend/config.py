import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./opportunities.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 