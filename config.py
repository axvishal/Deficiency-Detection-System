"""Application configuration."""

import os
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
except ImportError:
    BaseSettings = None


def _env(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)


class Settings:
    """Application settings loaded from environment."""

    def __init__(self):
        # Database
        self.database_url = _env("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/deficiency_detection"

        # Redis
        self.redis_url = _env("REDIS_URL") or "redis://localhost:6379/0"
        self.redis_ttl_seconds = int(_env("REDIS_TTL_SECONDS") or "7200")
        self.comparison_rules_cache_key = _env("COMPARISON_RULES_CACHE_KEY") or "comparison_rules_v2024"

        # AWS Bedrock
        self.aws_access_key_id = _env("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = _env("AWS_SECRET_ACCESS_KEY")
        self.aws_region = _env("AWS_REGION") or "us-east-1"
        self.bedrock_model_id = _env("BEDROCK_MODEL_ID") or "anthropic.claude-3-sonnet-20240229-v1:0"

        # Application
        self.clarification_days = int(_env("CLARIFICATION_DAYS") or "15")
        self.log_level = _env("LOG_LEVEL") or "INFO"

        # Tolerance thresholds (percentage)
        self.capacity_tolerance_pct = float(_env("CAPACITY_TOLERANCE_PCT") or "5.0")
        self.investment_tolerance_pct = float(_env("INVESTMENT_TOLERANCE_PCT") or "10.0")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
