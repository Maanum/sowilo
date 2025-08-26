import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file from the backend directory
backend_dir = Path(__file__).parent.parent
load_dotenv(backend_dir / ".env")


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./opportunities.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174",
    )
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    class Config:
        env_file = backend_dir / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
