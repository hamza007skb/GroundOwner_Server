from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.automap import automap_base
from .database_url import DB_ASYNC_URL

# Initialize the async engine
async_engine = create_async_engine(DB_ASYNC_URL, echo=True)

metadata = MetaData()
AutomapBase = automap_base(metadata=metadata)



async def init_async_db():
    async with async_engine.begin() as conn:  # opens asynchronous context manager and creates transaction
        await conn.run_sync(metadata.reflect)
        AutomapBase.prepare()


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # for storing data to cache
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:  # Create an instance of AsyncSession
        yield session


