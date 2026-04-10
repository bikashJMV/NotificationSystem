from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Extra

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Email Microservice"
    API_KEY: str

    # Mail Settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str = "Asset Manager"
    MAIL_SERVER: str
    MAIL_PORT: int = 587
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_DEFAULT_CC: str | None = None

    # Supabase Settings
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Configuration for pydantic-settings to read from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
