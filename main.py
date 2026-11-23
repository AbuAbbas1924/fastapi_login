import logging
import os
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    new_name: str = Field("no name available", validation_alias="new-name")
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings():
    return Settings()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str


engine = create_async_engine(get_settings().database_url, echo=True, future=True)


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
    return {
        "pydantic name": get_settings().new_name,
        "os name": os.getenv("new-NAME", "no name available"),
    }

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