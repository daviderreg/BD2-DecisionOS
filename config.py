import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "DecisionOS"
    MONGODB_COLLECTION: str = "decisions"
    GOOGLE_API_KEY: str
    EMBEDDING_MODEL: str = "models/text-embedding-004"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
