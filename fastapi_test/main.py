from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from fastapi_test.api import router
from fastapi_test.config import Config
from fastapi_test.data.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config()
    engine = create_async_engine(config.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # TODO: use alembic
    app.state.engine = engine
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
