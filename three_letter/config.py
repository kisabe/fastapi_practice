from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///3letter.db"
    message_length: int = 3
