from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from internal.config.settings import settings


engine = create_async_engine(settings.DATABASE_URL,
                             echo=False, future=True, plugins=['geoalchemy2'])

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW
)


async def session():
    async with SessionLocal() as sess:
        yield sess
