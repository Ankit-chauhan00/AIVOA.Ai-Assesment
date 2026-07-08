from sqlalchemy import text

from app.db.session import engine


async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(result.scalar())
            print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Database connection failed!")
        print(e)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())