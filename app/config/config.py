from pydantic import BaseSettings

class Setting(BaseSettings):
    # sqlmodel database settings name

    database_name: str

    class Config:
        env_file = ".env"

setting = Setting()