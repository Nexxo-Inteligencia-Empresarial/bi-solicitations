from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DB_", case_sensitive=False, extra="allow")
    user: str
    password: str
    host: str
    port: str
    database: str    

class Settings(BaseSettings):
    database: Optional[DatabaseSettings] = DatabaseSettings()

settings = Settings()