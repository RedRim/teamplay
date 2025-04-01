from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    """
    Данные для подключения к базе данных
    """

    db_host: str | None = None
    db_out_port: str | None = None
    postgres_connection_port: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_db: str | None = None

    class Config:
        env_prefix = ""

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.postgres_connection_port}/{self.postgres_db}"


class Config:
    db: DatabaseConfig = DatabaseConfig()

def setup_config() -> Config:
    return Config()
