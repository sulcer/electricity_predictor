import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    window_size: int = 24

    # dagshub configuration
    mlflow_tracking_username: str
    mlflow_tracking_uri: str
    mlflow_tracking_password: str
    dagshub_user_token: str
    dagshub_repo_name: str

    __project_root = pathlib.Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(env_file=f"{__project_root}/.env")


settings = Settings()
