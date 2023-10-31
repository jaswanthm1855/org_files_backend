import pathlib

from pydantic import BaseSettings


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class EnvironmentVariablesConfig(BaseSettings):
    DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


env_variables = EnvironmentVariablesConfig()
