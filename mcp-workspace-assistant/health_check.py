from app.config import (
    DOCUMENTS_DIR,
    LOGS_DIR,
    NOTES_DIR,
    OUTPUTS_DIR,
    PROJECT_ROOT,
    TASKS_DIR,
    WORKSPACE_DIR,
    ensure_directories,
    get_settings,
    validate_settings,
)
from app.workspace_manager import WorkspaceManager


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
        PROJECT_ROOT / "app" / "workspace_manager.py",
        PROJECT_ROOT / "app" / "tools.py",
        PROJECT_ROOT / "app" / "assistant_pipeline.py",
        PROJECT_ROOT / "app" / "logger.py",
        PROJECT_ROOT / "app" / "prompts.py",
        PROJECT_ROOT / "tests" / "test_workspace_manager.py",
        PROJECT_ROOT / "tests" / "test_tools.py",
        PROJECT_ROOT / "tests" / "test_assistant_pipeline.py",
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
        WORKSPACE_DIR,
        NOTES_DIR,
        TASKS_DIR,
        DOCUMENTS_DIR,
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


def check_workspace_access() -> bool:
    """
    Check whether WorkspaceManager can list workspace files.
    """
    try:
        manager = WorkspaceManager()
        files = manager.list_files()

        check_pass(f"Workspace access works. Files found: {len(files)}")

        if files:
            for file in files[:10]:
                print(f"      - {file.relative_path}")

        return True

    except Exception as error:
        check_fail(f"Workspace access failed: {error}")
        return False


def check_workspace_safety() -> bool:
    """
    Check whether unsafe path traversal is blocked.
    """
    try:
        manager = WorkspaceManager()
        manager.read_text_file("../../secret.txt")
    except ValueError:
        check_pass("Workspace path traversal protection works.")
        return True
    except Exception as error:
        check_fail(f"Unexpected safety check error: {error}")
        return False

    check_fail("Unsafe path traversal was not blocked.")
    return False


def check_outputs() -> bool:
    """
    Check whether output files exist.
    """
    if not OUTPUTS_DIR.exists():
        check_warning("Outputs directory does not exist.")
        return False

    output_files = [
        path
        for path in OUTPUTS_DIR.iterdir()
        if path.is_file() and path.name != ".gitkeep"
    ]

    if output_files:
        check_pass(f"Output files found: {len(output_files)}")
        return True

    check_warning("No generated output files found yet.")
    return False


def run_health_check() -> None:
    """
    Run all health checks and print a summary.
    """
    print("=" * 80)
    print("MCP Workspace Assistant - Health Check")
    print("=" * 80)

    checks = {
        "env_file": check_env_file(),
        "settings": check_settings(),
        "project_structure": check_project_structure(),
        "directories": check_directories(),
        "workspace_access": check_workspace_access(),
        "workspace_safety": check_workspace_safety(),
        "outputs": check_outputs(),
    }

    passed = sum(1 for result in checks.values() if result)
    total = len(checks)

    print("=" * 80)
    print("Summary")
    print(f"Passed checks: {passed}/{total}")

    if (
        checks["settings"]
        and checks["project_structure"]
        and checks["workspace_safety"]
    ):
        print("Core project setup is valid.")
    else:
        print("Core project setup needs attention.")

    if not checks["outputs"]:
        print("No generated output files yet. This is normal at this stage.")


if __name__ == "__main__":
    run_health_check()