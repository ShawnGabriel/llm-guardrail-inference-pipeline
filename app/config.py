from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    hf_api_token: str = ""
    database_url: str = "sqlite:///./interactions.db"
    app_env: str = "local"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()