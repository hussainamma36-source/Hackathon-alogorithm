from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./reelmind.db"
    
    # AI Provider
    AI_PROVIDER: str = "local"  # "local", "openai", "gemini", "anthropic"
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o-mini"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # App
    APP_NAME: str = "ReelMind AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self):
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]
    
    @property
    def effective_ai_provider(self):
        if self.AI_API_KEY:
            return self.AI_PROVIDER if self.AI_PROVIDER != "local" else "openai"
        return "local"


settings = Settings()
