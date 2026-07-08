import asyncio

from app.agent.tools import log_interaction

async def main():
    response = await log_interaction.ainvoke(
        {
            "text": """
            Met Dr. Raj Sharma today.

            Discussed CardioX Phase III trial.

            Shared product brochure.

            Distributed 10 sample packs.

            Doctor showed positive interest and requested additional clinical literature.

            Schedule a follow-up visit next week.
            """
        }
    )

    print(response)

if __name__ == "__main__":
    asyncio.run(main())