from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel


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
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/test-db")
async def test_db():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            return {"result": result.scalar()}
    except Exception as e:
        return {"error": f"{str(e)} OR postgres isn't run"}