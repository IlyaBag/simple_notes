from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_v1 import router as api_router
from database.db import engine
from database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan, title='Simple Notes')

app.include_router(api_router)
