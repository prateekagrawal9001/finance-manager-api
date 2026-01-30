from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    DATABASE_USER: str = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "")
    JWT_TOKEN_SECRET_KEY: str = os.getenv("JWT_TOKEN_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    CURRENCY_API_URL: str = os.getenv("CURRENCY_API_URL", "")
    CURRENCY_API_KEY: str = os.getenv("CURRENCY_API_KEY", "")
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class ConfigDict:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()