"""
LLM Setup
using this gemini model as this is free and i dont have tokens
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


google_api_key = settings.GOOGLE_API_KEY
google_llm_model = settings.LLM_MODEL

grok_api_key = settings.GROK_API_KEY
grack_llm_model = settings.GROK_MODEL

extraction_llm = ChatGoogleGenerativeAI(model=google_llm_model)

reasoning_llm = ChatGoogleGenerativeAI(model=google_llm_model)




