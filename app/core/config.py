from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "API QRKot"
    app_description: str = "Фонд собирает пожертвования"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
