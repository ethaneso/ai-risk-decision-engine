from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.app.config import settings

sqlalchemy_database_url = settings.database_url
if sqlalchemy_database_url and sqlalchemy_database_url.startswith(
    "postgresql://"
):
    sqlalchemy_database_url = sqlalchemy_database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(
    sqlalchemy_database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
