from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """
    Подгрузка глобальных переменных из файла .env
    """
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
