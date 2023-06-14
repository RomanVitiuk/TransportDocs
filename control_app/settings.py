from pydantic import BaseSettings


class Settings(BaseSettings):
    ADMIN_NAME: str
    ADMIN_PASSWORD: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    DB_URL: str = "sqlite:///db_app.sqlite"
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
