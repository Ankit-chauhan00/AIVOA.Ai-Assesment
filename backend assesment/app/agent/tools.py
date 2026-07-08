import json
from datetime import datetime

from app.agent.llm import extraction_llm
from app.db.session import async_session_factory
from app.models.hcp_model import HCP
from app.models.intraction_model import Interaction
from langchain_core.tools import tool
from sqlalchemy import select

import asyncio

EXTRACTION_PROMPT = """You are a data-extraction assistant for a pharma CRM.
Given a free-text note or transcript of a sales rep describing an HCP (Healthcare Professional)
interaction, extract a strict JSON object with these fields:

•⁠  hcp_name (string)
•⁠  interaction_type (one of: Meeting, Call, Email, Conference)
•⁠  topics_discussed (string, concise)
•⁠  materials_shared (list of strings)
•⁠  samples_distributed (list of strings)
•⁠  sentiment (one of: positive, neutral, negative)
•  outcomes (string, concise)
•⁠  follow_up_actions (string, concise)
•⁠  speciality on the hcp in just one word string
•⁠  hospital just the name of hospital
•⁠  city just the name of the city

Only output the JSON object, no other text. If a field isn't mentioned, use an empty
string, empty list, or "neutral" for sentiment as appropriate.

Text:
{text}
"""

FOLLOWUP_PROMPT = """You are a pharma sales-enablement assistant. Based on the interaction
details below, suggest up to 3 concrete, specific follow-up actions the rep should take
(e.g. scheduling a follow-up meeting, sending a specific piece of literature, adding the
HCP to a program). Return ONLY a JSON list of short strings.

Interaction:
HCP: {hcp_name}
Topics: {topics}
Sentiment: {sentiment}
Outcomes: {outcomes}
Speciality: {speciality}
hospital: {hospital}
city: {city}
"""


"""Safe chcking for json and converting"""


def _safe_json(raw: str):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.split("\n", 1)[-1] if raw.lower().startswith("json") else raw
    try:
        return json.loads(raw)
    except Exception:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(raw[start : end + 1])
            except Exception:
                return None
        return None


# ---------------------------------------------------------------------------
# Tool 1: log_interaction
# ---------------------------------------------------------------------------
@tool("log_interaction")
async def log_interaction(text: str) -> str:
    """
    »» Log a new HCP interaction
    »» use LLM to extract names, topics and other fields
    »» describing teh intraction and storing it to the intraction model
    """
    prompt = EXTRACTION_PROMPT.format(text=text)
    raw = extraction_llm.invoke(prompt).content

    if isinstance(raw, list):
        raw = "".join(
            item if isinstance(item, str) else json.dumps(item) for item in raw
        )

    data = _safe_json(raw) or {}

    hcp_name = data.get("hcp_name") or "Unknown HCP"
    interaction_type = data.get("interaction_type") or "Meeting"
    materials = data.get("materials_shared") or []
    samples = data.get("samples_distributed") or []
    speciality = data.get("speciality", "")
    hospital = data.get("hospital", "")
    city = data.get("city", "")

    # suggestion = _suggest_follow_ups(hcp_name,topics,sentiment, outcomes)

    async with async_session_factory() as db:
        try:
            # -------------------------------
            # Find existing HCP
            # -------------------------------
            result = await db.execute(
                select(HCP).where(HCP.name.ilike(f"%{hcp_name}%"))
            )
            hcp = result.scalar_one_or_none()

            # -------------------------------
            # Create HCP if not found
            # -------------------------------

            if hcp is None:
                hcp = HCP(
                    name=hcp_name,
                    specialty=speciality,
                    hospital=hospital,
                    city=city,
                )

                db.add(hcp)
                await db.flush()  # Generates hcp.id

            # -------------------------------
            # Create Interaction
            # -------------------------------
            interaction = Interaction(
                hcp_id=hcp.id,
                interaction_type=interaction_type,
                interaction_date=datetime.utcnow().date(),
                notes=text,
                products_discussed=", ".join(materials + samples),
            )

            db.add(interaction)
            await db.commit()
            await db.refresh(interaction)

            return json.dumps(
                {
                    "status": "success",
                    "interaction_id": interaction.id,
                    "hcp_id": hcp.id,
                    "hcp_name": hcp.name,
                    "message": "Interaction logged successfully.",
                }
            )
        except Exception as e:
            await db.rollback()
            return json.dumps({"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# Tool 2: Edit_transaction
# ---------------------------------------------------------------------------
@tool("edit_interaction")
async def edit_interaction(
    interaction_id: int,
    notes: str | None = None,
    interaction_type: str | None = None,
    products_discussed: str | None = None,
):
    """
    Edit an existing HCP interaction.

    Updates only the fields that are provided. If a field is None,
    its current value is left unchanged.

    Args:
        interaction_id: ID of the interaction to edit.
        notes: Updated interaction notes.
        interaction_type: Updated interaction type.
        products_discussed: Updated products discussed.
    """
    async with async_session_factory() as db:
        result = await db.execute(
            select(Interaction).where(Interaction.id == interaction_id)
        )

        interaction = result.scalar_one_or_none()

        if interaction is None:
            return json.dumps({"status": "error", "message": "Interaction not found"})

        if interaction is None:
            return json.dumps(
                {
                    "status": "error",
                    "message": "Interaction not found",
                }
            )

        if notes is not None:
            interaction.notes = notes # type: ignore[assignment]
        if interaction_type is not None:
            interaction.interaction_type = interaction_type # type: ignore[assignment]

        if products_discussed is not None:
            interaction.products_discussed = products_discussed # type: ignore[assignment]

        
        await db.commit()
        await db.refresh(interaction)

        return json.dumps(
        {
            "status": "success",
            "interaction_id": interaction.id,
            "message": "Interaction updated successfully.",
        }
    )


@tool("search_hcp")
async def search_hcp(query: str)->str:
    """
    Search for HCPs (Health care proffesional) by name speciality or hospital
    used to auto complete the HCP name field and pull to prior context
    """

    async with async_session_factory() as db:
        try:
            result = await db.execute(
                select(HCP).where(
                    or_(
                        HCP.name.ilike(f"%{query}%"),
                        HCP.specialty.ilike(f"%{query}%"),
                        HCP.hospital.ilike(f"%{query}%"),
                        HCP.city.ilike(f"%{query}%"),
                    )
                )
            )

            hcps = result.scalar().all()

            return json.dumps(
                [
                    {
                        "id": hcp.id,
                        "name": hcp.name,
                        "specialty": hcp.specialty,
                        "hospital": hcp.hospital,
                        "city": hcp.city,
                    }
                    for hcp in hcps
                ]
            )
        except Exception as e:
            return json.dumps(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


def 




# async def main():
#     result = await log_interaction.ainvoke(
#         {
#             "text": """
#             Visited Dr. Ankit Chauhan, Neurologist at Manipal Hospital, Bengaluru.

# Presented NeuroPlus and discussed its benefits in neuropathic pain management. Shared a product brochure and clinical comparison sheet. The doctor was not convinced due to concerns about pricing and availability and declined sample packs.

# Need to send pharmacoeconomic evidence and revisit after a month.
#             """
#         }
#     )
#     print(result)


# async def main():
#     result = await edit_interaction.ainvoke(
#         {
#             "interaction_id": 1,  # Change to an existing interaction ID
#             "notes": """
#             Follow-up meeting with Dr. Priya Chauhan.
#             Discussed NeuroPlus in detail and answered pricing concerns.
#             The doctor requested additional clinical evidence.
#             """,
#             "interaction_type": "AppointMent",
#             "products_discussed": "NeuroPlus, Clinical Evidence Brochure",
#         }
#     )

#     print(result)



# if __name__ == "__main__":
    # asyncio.run(main())
