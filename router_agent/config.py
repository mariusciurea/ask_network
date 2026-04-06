"""Application configuration."""


import os
from pydantic_settings import BaseSettings
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    """Environment-backed settings."""
    google_api_key: str
    adk_model: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str

    @property
    def mysql_server_url(self) -> str:
        """Return SQLAlchemy URL for server-level connection."""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/mysql"
        )

    @property
    def mysql_database_url(self) -> str:
        """Return SQLAlchemy URL for app database connection."""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


def load_settings() -> Settings:
    """Load runtime settings from environment variables."""
    return Settings()
