from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """App settings class"""

    environment: str = "development"
    secret_key: str
    database_url: PostgresDsn
    test_database_url: PostgresDsn


settings = Settings()
