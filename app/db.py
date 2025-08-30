import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def _database_url() -> str:
    user = os.environ["PG_USER"]
    pwd = os.environ["PG_PASSWORD"]
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5432")
    db = os.environ["PG_DB"]
    return f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{db}"


engine = create_async_engine(_database_url(), pool_size=5, max_overflow=5, future=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


