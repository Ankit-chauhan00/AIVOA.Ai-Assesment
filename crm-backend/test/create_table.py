import asyncio

from app.db.session import engine
from app.db.base import Base

# Import ALL models
from app.models.hcp_model import HCP
from app.models.intraction_model import Interaction
from app.models.followUp_model import FollowUpTask


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())