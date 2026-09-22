from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trader's Inc Terminal API"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    cors_origins: str = (
        "https://nesh34chavan-cyber.github.io,"
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    market_data_provider: str = "twelve_data"
    twelve_data_api_key: str = ""
    twelve_data_base_url: str = "https://api.twelvedata.com"

    database_url: str = (
        "postgresql+psycopg://trader:trader_dev"
        "@localhost:5432/traders_inc"
    )

    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            x.strip()
            for x in self.cors_origins.split(",")
            if x.strip()
        ]


settings = Settings()
