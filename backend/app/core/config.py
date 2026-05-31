import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


def get_env(key: str) -> str:
    """
    Helper function for fetching environment variables.
    Raises RuntimeError if environment variable key is missing.
    """
    try:
        return os.environ[key]
    except KeyError:
        raise RuntimeError(f"Missing required environment variable: {key}")


@dataclass(frozen=True)
class Config:
    """
    Project configuration settings.
    """

    DB_USER: str = get_env("DB_USER")
    DB_PASSWORD: str = get_env("DB_PASSWORD")
    DB_HOSTNAME: str = get_env("DB_HOSTNAME")
    DB_NAME: str = get_env("DB_NAME")
    NEON_AUTH: str = get_env("NEON_AUTH_URL")

    @property
    def db_url(self) -> str:
        """
        Construct the SQLAlchemy connection string.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}/{self.DB_NAME}"

    def __repr__(self) -> str:
        """
        String that get's printed when user calls print(). Prevents password from being printed.
        """
        return f"Config(user='{self.DB_USER}', host='{self.DB_HOSTNAME}', password='**********')"


config = Config()
