"""Determining a central system for import"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SUPERBASE_DATABASE_URL: str
    GOOGLE_API_KEY:str
    LLM_MODEL: str = "gemini-2.5-flash"
    GROK_API_KEY: str 
    GROK_MODEL:str =  "grok-4"

    model_config = {"env_file": ".env", "extra": "ignore"}



settings = Settings() # type: ignore