"""Database setup and initialization."""


from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from router_agent.config import load_settings
from router_agent.models import Base
from router_agent.seed import seed_routers_if_empty

settings = load_settings()
BASE_DIR = Path(__file__).resolve().parent.parent
SEED_JSON_PATH = BASE_DIR / "data" / "router_configs.json"

server_engine = create_engine(settings.mysql_server_url, pool_pre_ping=True)
app_engine = create_engine(settings.mysql_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=app_engine, autoflush=False, autocommit=False)


def initialize_database() -> None:
    """Create database, tables, and seed initial data."""
    create_database_if_needed()
    Base.metadata.create_all(bind=app_engine)
    with SessionLocal() as session:
        seed_routers_if_empty(session=session, seed_path=SEED_JSON_PATH)


def create_database_if_needed() -> None:
    """Create target MySQL database when missing."""
    db_name = settings.mysql_database
    with server_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
        connection.commit()


def get_session() -> Session:
    """Return a SQLAlchemy session."""
    return SessionLocal()

