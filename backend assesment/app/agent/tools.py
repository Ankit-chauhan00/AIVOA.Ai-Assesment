import asyncio
import json
from datetime import datetime, timedelta
from typing import List, cast

from app.agent.llm import extraction_llm, reasoning_llm
from app.db.session import async_session_factory
from app.models.followUp_model import FollowUpTask
from app.models.hcp_model import HCP
from app.models.intraction_model import Interaction
from langchain_core.tools import tool
from sqlalchemy import or_, select

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
            return json.dumps(
                {
                    "status": "error",
                    "message": "Interaction not found",
                }
            )

        if notes is not None:
            interaction.notes = notes  # type: ignore[assignment]
        if interaction_type is not None:
            interaction.interaction_type = interaction_type  # type: ignore[assignment]

        if products_discussed is not None:
            interaction.products_discussed = products_discussed  # type: ignore[assignment]

        await db.commit()
        await db.refresh(interaction)

        return json.dumps(
            {
                "status": "success",
                "interaction_id": interaction.id,
                "message": "Interaction updated successfully.",
            }
        )


# ---------------------------------------------------------------------------
# Tool 3: Search HCP
# ---------------------------------------------------------------------------
@tool("search_hcp")
async def search_hcp(query: str) -> str:
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

            hcps = result.scalars().all()

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


def _suggest_followups_raw(
    hcp_name: str,
    topic: str,
    sentiments: str,
    outcomes: str,
    speciality: str,
    hospital: str,
    city: str,
) -> List[str]:

    prompt = FOLLOWUP_PROMPT.format(
        hcp_name=hcp_name,
        topics=topic,
        sentiment=sentiments,
        outcomes=outcomes,
        speciality=speciality,
        hospital=hospital,
        city=city,
    )
    raw = reasoning_llm.invoke(prompt).content
    if isinstance(raw, list):
        raw = "".join(
            item if isinstance(item, str) else json.dumps(item) for item in raw
        )
    print(raw)

    data = _safe_json(raw)
    if isinstance(data, list):
        return data[:3]
    return []


# ---------------------------------------------------------------------------
# Tool 4: Suggest follow ups on the basi of the interaction-> notes
# ---------------------------------------------------------------------------


@tool("suggest_followups")
async def suggest_followups(interaction_id: int) -> str:
    """
    Generate AI Suggestion follow-ups action for alredy logged interaction
    """

    async with async_session_factory() as db:
        try:
            result = await db.execute(
                select(Interaction).where(Interaction.id == interaction_id)
            )

            interaction = result.scalar_one_or_none()

            if interaction is None:
                return json.dumps(
                    {"status": "error", "message": "Interaction not found"}
                )

            # Fetch HCP
            result = await db.execute(select(HCP).where(HCP.id == interaction.hcp_id))

            hcp = result.scalar_one_or_none()

            if hcp is None:
                return json.dumps(
                    {
                        "status": "error",
                        "message": "HCP not found",
                    }
                )

            # Re-extract details from interaction notes
            prompt = EXTRACTION_PROMPT.format(text=interaction.notes)

            raw = extraction_llm.invoke(prompt).content

            if isinstance(raw, list):
                raw = "".join(
                    item if isinstance(item, str) else json.dumps(item) for item in raw
                )

            data = _safe_json(raw) or {}

            suggestions = _suggest_followups_raw(
                hcp_name=cast(str, hcp.name),
                topic=data.get("topics_discussed", ""),
                sentiments=data.get("sentiment", "neutral"),
                outcomes=data.get("outcomes", ""),
                speciality=cast(str, hcp.specialty or ""),
                hospital=cast(str, hcp.hospital or ""),
                city=cast(str, hcp.city or ""),
            )

            return json.dumps(
                {
                    "status": "success",
                    "interaction_id": interaction.id,
                    "hcp_name": hcp.name,
                    "suggestions": suggestions,
                }
            )
        except Exception as e:
            return json.dumps(
                {
                    "status": "error",
                    "message": str(e),
                }
            )


# ---------------------------------------------------------------------------
# Tool 5: Add a follow up
# ---------------------------------------------------------------------------


@tool("schedule_followup")
async def schedule_followup(
    interaction_id: int,
    task_from_interaction: str,
    days_from_now: int = 14,
    status: str = "Pending",
) -> str:
    """
    Schedule a follow-up
    task -> String
    due_date -> time
    status -> default pending else Complected
    """

    async with async_session_factory() as db:
        try:
            result = await db.execute(
                select(Interaction).where(Interaction.id == interaction_id)
            )

            interaction = result.scalar_one_or_none()

            if interaction is None:
                return json.dumps(
                    {"status": "error", "message": "Interaction not found"}
                )

            due_date = (datetime.utcnow() + timedelta(days=days_from_now)).date()

            task = FollowUpTask(
                interaction_id=interaction_id,
                task=task_from_interaction,
                due_date=due_date,
                status=status,
            )
            db.add(task)
            await db.commit()
            await db.refresh(task)

            return json.dumps(
                {
                    "status": "success",
                    "task_id": task.id,
                    "interaction_id": interaction_id,
                    "task": task.task,
                    "due_date": task.due_date.isoformat(),
                    "message": "Follow-up scheduled successfully.",
                }
            )
        except Exception as e:
            await db.rollback()
            return json.dumps({"status": "error", "message": str(e)})

ALL_TOOLS = [log_interaction,edit_interaction, search_hcp, suggest_followups, schedule_followup]