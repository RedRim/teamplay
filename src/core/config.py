from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


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


class AuthJWT(BaseModel):
    """
    Ключи для шифрования
    """

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    TOKEN_TYPE_FIELD: str = 'type'
    ACCESS_TOKEN_TYPE: str = 'access'
    REFRESH_TOKEN_TYPE: str = 'refresh'
    access_token_expire: int = 15 # minutes
    refresh_token_expire_days: int = 60 * 24 * 30


class Config:
    db: DatabaseConfig = DatabaseConfig()
    auth_jwt: AuthJWT = AuthJWT()

def setup_config() -> Config:
    return Config()
