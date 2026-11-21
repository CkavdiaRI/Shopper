from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    supplier_base_url: str
    database_url: str
    groq_api_key: str = ""
    auth_service_url: str
    groq_url: str = "https://api.groq.com/openai/v1/chat/completions"


settings = Settings()