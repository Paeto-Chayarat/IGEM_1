from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str

    class Config:
        env_file = ".env"


config = Settings()
