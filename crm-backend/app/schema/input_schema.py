from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    history: list[tuple[str, str]] | None = None

class ChatResponse(BaseModel):
    reply: str
    tool_calls: list
    tool_results: list
    execution_trace: list


