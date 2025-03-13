import os

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


def find_dotenv():
    """
    Находит путь до файла .env в корне проекта.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Директория текущего файла (config.py)
    dotenv_path = os.path.join(current_dir, ".env")  # Путь до .env
    return dotenv_path


class Settings(BaseSettings):
    BROWSERSTACK_USER_NAME: str = Field(..., alias="BROWSERSTACK_USER_NAME")
    BROWSERSTACK_ACCESS_KEY: str = Field(..., alias="BROWSERSTACK_ACCESS_KEY")
    BROWSERSTACK_URL: str = Field(..., alias="BROWSERSTACK_URL")

    model_config = ConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
    )


# Проверка пути до файла .env
print("Ищем .env по пути:", find_dotenv())

settings = Settings()
