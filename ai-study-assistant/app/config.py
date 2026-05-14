from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load environment variables from .env file
load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"


class Settings(BaseSettings):
    """
    Central application settings.

    All configurable values should come from environment variables.
    This keeps the code clean, reusable, and safe for deployment.
    """

    app_name: str = Field(default="AI Study Assistant", alias="APP_NAME")
    debug: bool = Field(default=True, alias="DEBUG")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")

    primary_llm_provider: Literal["openai", "gemini"] = Field(
        default="openai",
        alias="PRIMARY_LLM_PROVIDER",
    )
    fallback_llm_provider: Literal["openai", "gemini"] = Field(
        default="gemini",
        alias="FALLBACK_LLM_PROVIDER",
    )

    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    gemini_model: str = Field(default="gemini-1.5-flash", alias="GEMINI_MODEL")

    embedding_provider: Literal["openai", "gemini"] = Field(
        default="openai",
        alias="EMBEDDING_PROVIDER",
    )
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        alias="OPENAI_EMBEDDING_MODEL",
    )
    gemini_embedding_model: str = Field(
        default="models/text-embedding-004",
        alias="GEMINI_EMBEDDING_MODEL",
    )

    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")

    vector_store_type: Literal["chroma", "faiss"] = Field(
        default="faiss",
        alias="VECTOR_STORE_TYPE",
    )
    top_k_retrieval: int = Field(default=4, alias="TOP_K_RETRIEVAL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    """
    Return application settings.

    Keeping this as a function makes it easy to reuse settings
    across all modules without duplicating configuration logic.
    """
    return Settings()


def validate_settings(settings: Settings | None = None) -> None:
    """
    Validate critical settings before running the application.

    This prevents unclear runtime errors later when calling LLMs
    or embedding models.
    """
    settings = settings or get_settings()

    if (
        settings.primary_llm_provider == "openai"
        and not settings.openai_api_key
    ):
        raise ValueError(
            "OPENAI_API_KEY is required when "
            "PRIMARY_LLM_PROVIDER=openai"
        )

    if (
        settings.primary_llm_provider == "gemini"
        and not settings.google_api_key
    ):
        raise ValueError(
            "GOOGLE_API_KEY is required when "
            "PRIMARY_LLM_PROVIDER=gemini"
        )

    if (
        settings.embedding_provider == "openai"
        and not settings.openai_api_key
    ):
        raise ValueError(
            "OPENAI_API_KEY is required when "
            "EMBEDDING_PROVIDER=openai"
        )

    if (
        settings.embedding_provider == "gemini"
        and not settings.google_api_key
    ):
        raise ValueError(
            "GOOGLE_API_KEY is required when "
            "EMBEDDING_PROVIDER=gemini"
        )

    if settings.chunk_overlap >= settings.chunk_size:
        raise ValueError(
            "CHUNK_OVERLAP must be smaller than CHUNK_SIZE"
        )


if __name__ == "__main__":
    settings = get_settings()

    print("Project root:", PROJECT_ROOT)
    print("Raw data dir:", RAW_DATA_DIR)
    print("Vector DB dir:", VECTOR_DB_DIR)
    print("App name:", settings.app_name)
    print("Primary provider:", settings.primary_llm_provider)
    print("Embedding provider:", settings.embedding_provider)
