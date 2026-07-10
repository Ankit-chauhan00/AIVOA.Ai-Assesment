from fastapi import FastAPI
from app.schema.input_schema import ChatRequest, ChatResponse


from app.agent.graph import run_agent

#===Fast API===#

app = FastAPI(
    title="AI-First CRM - HCP Module",
    description="AI-powered CRM assistant for managing HCP interactions.",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "AI-First CRM - HCP Module",
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    result = await run_agent(
        user_message=request.message,
        history=request.history,
    )

    return result
