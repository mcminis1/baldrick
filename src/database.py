import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_DATABASE = os.environ.get("DB_DATABASE")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

connection_string = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
)
engine = create_async_engine(connection_string, future=True, echo=True)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
