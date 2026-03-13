from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Guias API"
    app_env: str = "dev"
    debug: bool = True
    default_source: str = "mock"
    google_sheet_id: str = ""
    google_service_account_file: str = ""
    database_url: str = "sqlite:///./guias.db"
    carrier_base_url: str = ""
    carrier_username: str = ""
    carrier_password: str = ""
    default_notification_email: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
