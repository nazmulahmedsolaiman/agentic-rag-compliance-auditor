from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "agentic-rag-compliance-auditor"
    log_level: str = "INFO"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/compliance_audit"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
