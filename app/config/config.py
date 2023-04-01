from pydantic import BaseSettings

class Setting(BaseSettings):
    # sqlmodel database settings name

    database_name: str
    algorithm: str
    secret_key: str
    expiry_time: int

    class Config:
        env_file = ".env"

setting = Setting()