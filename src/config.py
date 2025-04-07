from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import (
    PostgresDsn,
    SecretStr,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(str(BASE_DIRECTORY / ".env")))


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    user: str | None = None
    password: SecretStr
    host: str | None = None
    port: int | None = None
    database: str | None = None

    driver: str = "asyncpg"
    database_system: str = "postgresql"
    echo: bool = False

    def url(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.database_system}+{self.driver}",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.database,
        )
        return dsn.unicode_string()


class Config(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()


config = Config()
