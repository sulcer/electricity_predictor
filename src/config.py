import pathlib
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    window_size: int = 24
    features: List[str] = [
        'temperature',
        'humidity',
        'precipitation',
        'cloud_cover',
        'wind_speed'
    ]
    production_types: List[str] = [
        'cross',
        'nuclear',
        'hydro',
        'fossil',
    ]

    # dagshub configuration
    mlflow_tracking_username: str
    mlflow_tracking_uri: str
    mlflow_tracking_password: str
    dagshub_user_token: str
    dagshub_repo_name: str

    __project_root = pathlib.Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(env_file=f"{__project_root}/.env")


settings = Settings()
