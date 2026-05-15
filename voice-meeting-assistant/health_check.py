from app.audio_loader import SUPPORTED_AUDIO_EXTENSIONS
from app.config import (
    LOGS_DIR,
    OUTPUTS_DIR,
    PROJECT_ROOT,
    UPLOADED_AUDIO_DIR,
    ensure_directories,
    get_settings,
    validate_settings,
)


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


def check_project_structure() -> bool:
    """
    Check important project files.
    """
    required_files = [
        PROJECT_ROOT / "run.py",
        PROJECT_ROOT / "streamlit_app.py",
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / ".env.example",
        PROJECT_ROOT / ".gitignore",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "pytest.ini",
        PROJECT_ROOT / "app" / "config.py",
        PROJECT_ROOT / "app" / "audio_loader.py",
        PROJECT_ROOT / "app" / "transcription_pipeline.py",
        PROJECT_ROOT / "app" / "summarization_pipeline.py",
        PROJECT_ROOT / "app" / "result_manager.py",
        PROJECT_ROOT / "app" / "prompts.py",
        PROJECT_ROOT / "tests" / "test_audio_loader.py",
        PROJECT_ROOT / "tests" / "test_result_manager.py",
        PROJECT_ROOT / "tests" / "test_text_direction.py",
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


def check_directories() -> bool:
    """
    Check whether required directories exist.
    """
    ensure_directories()

    required_dirs = [
        UPLOADED_AUDIO_DIR,
        OUTPUTS_DIR,
        LOGS_DIR,
    ]

    missing_dirs = [
        directory
        for directory in required_dirs
        if not directory.exists()
    ]

    if not missing_dirs:
        check_pass("Required directories exist.")
        return True

    check_fail("Some required directories are missing:")
    for directory in missing_dirs:
        print(f"      - {directory}")

    return False


def check_uploaded_audio() -> bool:
    """
    Check whether uploaded_audio contains supported audio files.
    """
    if not UPLOADED_AUDIO_DIR.exists():
        check_warning("Uploaded audio directory does not exist.")
        return False

    audio_files = [
        path
        for path in UPLOADED_AUDIO_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    ]

    if audio_files:
        check_pass(f"Supported uploaded audio files found: {len(audio_files)}")
        for audio_path in audio_files:
            print(f"      - {audio_path.name}")
        return True

    check_warning("No supported audio files found in data/uploaded_audio.")
    return False


def check_outputs() -> bool:
    """
    Check whether analysis outputs exist.
    """
    if not OUTPUTS_DIR.exists():
        check_warning("Outputs directory does not exist.")
        return False

    output_files = [
        path
        for path in OUTPUTS_DIR.iterdir()
        if path.is_file() and path.suffix.lower() == ".json"
    ]

    if output_files:
        check_pass(f"Audio analysis output files found: {len(output_files)}")
        return True

    check_warning("No audio analysis output JSON files found yet.")
    return False


def run_health_check() -> None:
    """
    Run all health checks and print a summary.
    """
    print("=" * 80)
    print("AI Voice Meeting Assistant - Health Check")
    print("=" * 80)

    checks = {
        "env_file": check_env_file(),
        "settings": check_settings(),
        "project_structure": check_project_structure(),
        "directories": check_directories(),
        "uploaded_audio": check_uploaded_audio(),
        "outputs": check_outputs(),
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

    if not checks["uploaded_audio"]:
        print("Upload an audio file before running audio analysis.")

    if not checks["outputs"]:
        print("Run at least one analysis to generate output files.")


if __name__ == "__main__":
    run_health_check()