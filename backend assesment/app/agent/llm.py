"""
LLM Setup
using this gemini model as this is free and i dont have tokens
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


google_api_key = settings.GOOGLE_API_KEY
llm_model = settings.LLM_MODEL

extraction_llm = ChatGoogleGenerativeAI(model=llm_model)

reasoning_llm =  ChatGoogleGenerativeAI(model=llm_model)

response =  extraction_llm.invoke("hello")
print(response.content)

