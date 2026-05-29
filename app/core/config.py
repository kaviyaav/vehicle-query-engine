from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://vqe_user:vqe_pass@localhost:5432/vqe_db"
    app_title: str = "Vehicle Query Engine"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
