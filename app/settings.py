from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings class"""

    environment: str = "development"
    secret_key: str
    database_url: str
    test_database_url: str


settings = Settings()
