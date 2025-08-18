from pydantic_settings import BaseSettings, SettingsConfigDict


VALIDATE_TOKEN_URL = "http://user_service:8000/verify/auth/validate_token"
HASH_SERVICE_URL = "http://hash_service:8000/posts/hash"

BASE_URL = "http://localhost:8002"


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


database_settings = DatabaseSettings()
