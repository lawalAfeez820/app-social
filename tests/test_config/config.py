from pydantic import BaseSettings

class Setting(BaseSettings):
    database_test_name: str

    class Config:
        env_file = ".env"