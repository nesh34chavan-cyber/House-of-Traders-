from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "House of Traders API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "https://nesh34chavan-cyber.github.io,http://localhost:5173,http://127.0.0.1:5173"
    market_data_provider: str = "none"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

settings = Settings()
