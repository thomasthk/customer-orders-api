"""Application configuration loaded from environment variables"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from .env file"""

    database_url: str = "sqlite:///customers_orders.db"
    data_dir: str = "data"
    output_dir: str = "output"

    model_config = {"env_file": ".env"}


settings = Settings()
