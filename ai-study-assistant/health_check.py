from pathlib import Path

from app.config import (
    PROJECT_ROOT,
    RAW_DATA_DIR,
    VECTOR_DB_DIR,
    get_settings,
    validate_settings,
)


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}
FAISS_INDEX_DIR = VECTOR_DB_DIR / "faiss_index"


def check_pass(message: str) -> None:
    """
    Print a successful health check message.
    """
    print(f"[OK] {message}")


def check_warning(message: str) -> None:
    """
    Print a warning health check message.
    """
    print(f"[WARNING] {message}")


def check_fail(message: str) -> None:
    """
    Print a failed health check message.
    """
    print(f"[FAIL] {message}")


def check_env_file() -> bool:
    """
    Check whether the .env file exists.
    """
    env_path = PROJECT_ROOT / ".env"

    if env_path.exists():
        check_pass(".env file found.")
        return True

    check_fail(".env file is missing.")
    return False


def check_settings() -> bool:
    """
    Validate project settings.
    """
    try:
        settings = get_settings()
        validate_settings(settings)
        check_pass("Settings validation passed.")
        return True
    except Exception as error:
        check_fail(f"Settings validation failed: {error}")
        return False


def check_raw_data_dir() -> bool:
    """
    Check whether the raw data directory exists.
    """
    if RAW_DATA_DIR.exists():
        check_pass("data/raw directory exists.")
        return True

    check_fail("data/raw directory is missing.")
    return False


def check_supported_files() -> bool:
    """
    Check whether data/raw contains supported lecture files.
    """
    if not RAW_DATA_DIR.exists():
        check_fail("Cannot check files because data/raw is missing.")
        return False

    supported_files = [
        path
        for path in RAW_DATA_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if supported_files:
        check_pass(f"Supported files found: {len(supported_files)}")
        for file_path in supported_files:
            print(f"      - {file_path.name}")
        return True

    check_warning("No PDF or TXT files found in data/raw.")
    return False


def check_faiss_index() -> bool:
    """
    Check whether a FAISS index exists.
    """
    index_file = FAISS_INDEX_DIR / "index.faiss"
    metadata_file = FAISS_INDEX_DIR / "index.pkl"

    if index_file.exists() and metadata_file.exists():
        check_pass("FAISS index found.")
        return True

    check_warning(
        "FAISS index not found. Run: python run.py build"
    )
    return False


def check_project_structure() -> bool:
    """
    Check important project files.
    """
    required_files = [
        PROJECT_ROOT / "run.py",
        PROJECT_ROOT / "streamlit_app.py",
        PROJECT_ROOT / "evaluate.py",
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / ".env.example",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "app" / "config.py",
        PROJECT_ROOT / "app" / "rag_pipeline.py",
        PROJECT_ROOT / "app" / "vector_store.py",
    ]

    missing_files = [
        file_path
        for file_path in required_files
        if not file_path.exists()
    ]

    if not missing_files:
        check_pass("Project structure looks good.")
        return True

    check_fail("Some required files are missing:")
    for file_path in missing_files:
        print(f"      - {file_path}")

    return False


def run_health_check() -> None:
    """
    Run all health checks and print a summary.
    """
    print("=" * 80)
    print("AI Study Assistant - Health Check")
    print("=" * 80)

    checks = {
        "env_file": check_env_file(),
        "settings": check_settings(),
        "project_structure": check_project_structure(),
        "raw_data_dir": check_raw_data_dir(),
        "supported_files": check_supported_files(),
        "faiss_index": check_faiss_index(),
    }

    passed = sum(1 for result in checks.values() if result)
    total = len(checks)

    print("=" * 80)
    print("Summary")
    print(f"Passed checks: {passed}/{total}")

    if checks["settings"] and checks["project_structure"]:
        print("Core project setup is valid.")
    else:
        print("Core project setup needs attention.")

    if not checks["faiss_index"]:
        print("Build the knowledge base before asking questions:")
        print("python run.py build")


if __name__ == "__main__":
    run_health_check()