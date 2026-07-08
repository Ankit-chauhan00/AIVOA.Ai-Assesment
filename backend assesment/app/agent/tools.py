import json
from datetime import datetime, timedelta
from typing import Optional, List

from langchain_core.tools import tool
from app.db.session import get_db

from sqlalchemy import select
from app.agent.llm import extraction_llm, reasoning_llm


# ---------------------------------------------------------------------------
# Tool 1: log_interaction
# ---------------------------------------------------------------------------
