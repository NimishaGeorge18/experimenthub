from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These must exist in your .env file
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"                    # Default value
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60       # Default: 1 hour

    class Config:
        env_file = ".env"   # Tells pydantic where to read from

# Single instance used across the whole app
settings = Settings()