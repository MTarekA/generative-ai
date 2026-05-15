from app.config import (
    LOGS_DIR,
    OUTPUTS_DIR,
    PROJECT_ROOT,
    UPLOADED_IMAGES_DIR,
    ensure_directories,
    get_settings,
    validate_settings,
)
from app.image_loader import SUPPORTED_IMAGE_EXTENSIONS


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
        PROJECT_ROOT / "app" / "config.py",
        PROJECT_ROOT / "app" / "image_loader.py",
        PROJECT_ROOT / "app" / "vision_pipeline.py",
        PROJECT_ROOT / "app" / "result_manager.py",
        PROJECT_ROOT / "app" / "prompts.py",
        PROJECT_ROOT / "tests" / "test_image_loader.py",
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
        UPLOADED_IMAGES_DIR,
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


def check_uploaded_images() -> bool:
    """
    Check whether uploaded_images contains supported image files.
    """
    if not UPLOADED_IMAGES_DIR.exists():
        check_warning("Uploaded images directory does not exist.")
        return False

    image_files = [
        path
        for path in UPLOADED_IMAGES_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    ]

    if image_files:
        check_pass(f"Supported uploaded images found: {len(image_files)}")
        for image_path in image_files:
            print(f"      - {image_path.name}")
        return True

    check_warning("No supported images found in data/uploaded_images.")
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
        check_pass(f"Analysis output files found: {len(output_files)}")
        return True

    check_warning("No analysis output JSON files found yet.")
    return False


def run_health_check() -> None:
    """
    Run all health checks and print a summary.
    """
    print("=" * 80)
    print("AI Image Understanding Assistant - Health Check")
    print("=" * 80)

    checks = {
        "env_file": check_env_file(),
        "settings": check_settings(),
        "project_structure": check_project_structure(),
        "directories": check_directories(),
        "uploaded_images": check_uploaded_images(),
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

    if not checks["uploaded_images"]:
        print("Upload an image before running image analysis.")

    if not checks["outputs"]:
        print("Run at least one analysis to generate output files.")


if __name__ == "__main__":
    run_health_check()