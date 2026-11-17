from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@test_postgres:5432/postgres"
)

app = FastAPI()

@app.get("/test-db")
async def test_db():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            return {"result": result.scalar()}
    except Exception as e:
        return {"error": f"{str(e)} OR postgres isn't run"}