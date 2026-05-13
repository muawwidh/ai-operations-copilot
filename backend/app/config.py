from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AI Operations Copilot"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    API_PREFIX: str = "/api"

    DATABASE_URL: str

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    CHROMA_PERSIST_DIR: str = "./chroma_db"

    LOG_LEVEL: str = "info"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()