"""
LLM Setup
using this gemini model as this is free and i dont have tokens
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.core.config import settings


google_api_key = settings.GOOGLE_API_KEY
google_llm_model = settings.LLM_MODEL

grok_api_key = settings.GROK_API_KEY
grack_llm_model = settings.GROK_MODEL

extraction_llm = ChatGoogleGenerativeAI(model=google_llm_model)

reasoning_llm = ChatGoogleGenerativeAI(model=google_llm_model)

# reasoning_llm =  ChatOpenAI(
#     model=grack_llm_model,
#     api_key=grok_api_key, # type: ignore
#     base_url="https://api.x.ai/v1"
# )

google_response =  extraction_llm.invoke("hello google")
print(google_response.content)

grok_response = reasoning_llm.invoke("hello grok")
print(grok_response.content)

