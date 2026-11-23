import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel

logger = logging.getLogger(__name__)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@test_postgres:5432/postgres"
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    try:
        await init_db()
    except Exception as e:
        logger.error("DB not connected", type(e).__name__, e)
        os._exit(1)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

@app.get("/env")
async def env():
    return {"name": os.getenv("NAME", "no-name")}

@app.get("/test-db")
async def test_db():
    try:
        async with engine.begin() as conn:
            result = (await conn.execute(text("SELECT 1"))).scalar()
            if result == 1:
                return {"result": "postgres runs and are connected"}
    except Exception as e:
        # logger.exception(f"DB error: {e}")
        # raise HTTPException(status_code=503, detail="postgres are not available")
        return {"err": "postgres are not available"}