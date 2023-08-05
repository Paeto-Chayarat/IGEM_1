from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA: str

    class Config:
        env_file = ".env"


config = Settings()
