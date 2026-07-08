"""
engine is used to connect to PostgreSQL.
async_session_factory creates a session pooler.
get_db() yields a fresh session per request via FastAPI's dependency system.
"""

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from app.core.config import settings

engine = create_async_engine(
    settings.SUPERBASE_DATABASE_URL,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
