from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_MINS: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
