from dataclasses import dataclass
from pathlib import Path

from app.config import PROJECT_ROOT


INTEGRATED_WORKSPACE_DIR = PROJECT_ROOT / "integrated_workspace"
INTEGRATED_NOTES_DIR = INTEGRATED_WORKSPACE_DIR / "notes"
INTEGRATED_TASKS_DIR = INTEGRATED_WORKSPACE_DIR / "tasks"
INTEGRATED_DOCUMENTS_DIR = INTEGRATED_WORKSPACE_DIR / "documents"

ALLOWED_TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".json",
    ".csv",
}


@dataclass
class IntegratedWorkspaceFile:
    """
    Structured representation of a file inside the integrated workspace.
    """

    name: str
    relative_path: str
    size_bytes: int
    extension: str


def ensure_integrated_workspace() -> None:
    """
    Create integrated workspace folders if they do not exist.
    """
    INTEGRATED_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    INTEGRATED_TASKS_DIR.mkdir(parents=True, exist_ok=True)
    INTEGRATED_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


class IntegratedWorkspaceManager:
    """
    Safe file manager for the integrated workspace.

    This manager restricts all file operations to integrated_workspace/.
    """

    def __init__(self, workspace_dir: Path | None = None) -> None:
        ensure_integrated_workspace()
        self.workspace_dir = (
            workspace_dir or INTEGRATED_WORKSPACE_DIR
        ).resolve()

    def list_files(self) -> list[IntegratedWorkspaceFile]:
        """
        List all files inside the integrated workspace.
        """
        files = []

        for path in self.workspace_dir.rglob("*"):
            if path.is_file():
                relative_path = path.relative_to(self.workspace_dir)

                files.append(
                    IntegratedWorkspaceFile(
                        name=path.name,
                        relative_path=str(relative_path),
                        size_bytes=path.stat().st_size,
                        extension=path.suffix.lower(),
                    )
                )

        return sorted(files, key=lambda file: file.relative_path)

    def read_text_file(
        self,
        relative_path: str,
        max_chars: int = 8000,
    ) -> str:
        """
        Read a supported text file safely.
        """
        path = self._resolve_safe_path(relative_path)
        self._validate_readable_text_file(path)

        content = path.read_text(encoding="utf-8")

        return content[:max_chars]

    def write_text_file(
        self,
        relative_path: str,
        content: str,
        overwrite: bool = False,
    ) -> Path:
        """
        Write a supported text file safely.
        """
        path = self._resolve_safe_path(relative_path)

        if path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension for writing: {path.suffix}"
            )

        if path.exists() and not overwrite:
            raise FileExistsError(
                f"File already exists and overwrite=False: {relative_path}"
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return path

    def append_text_file(
        self,
        relative_path: str,
        content: str,
    ) -> Path:
        """
        Append text to a supported text file safely.
        """
        path = self._resolve_safe_path(relative_path)

        if path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension for appending: {path.suffix}"
            )

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding="utf-8") as file:
            file.write(content)

        return path

    def search_text_files(
        self,
        query: str,
        max_results: int = 10,
    ) -> list[dict]:
        """
        Search supported text files inside the integrated workspace.
        """
        clean_query = query.strip().lower()

        if not clean_query:
            raise ValueError("Search query cannot be empty.")

        results = []

        for file_info in self.list_files():
            if file_info.extension not in ALLOWED_TEXT_EXTENSIONS:
                continue

            try:
                content = self.read_text_file(file_info.relative_path)
            except UnicodeDecodeError:
                continue

            lower_content = content.lower()

            if clean_query in lower_content:
                results.append(
                    {
                        "file_name": file_info.name,
                        "relative_path": file_info.relative_path,
                        "snippet": self._create_snippet(
                            content=content,
                            query=clean_query,
                        ),
                    }
                )

            if len(results) >= max_results:
                break

        return results

    def _resolve_safe_path(self, relative_path: str) -> Path:
        """
        Resolve a relative path and block access outside the workspace.
        """
        if not relative_path or not relative_path.strip():
            raise ValueError("Relative path cannot be empty.")

        path = (self.workspace_dir / relative_path).resolve()

        if self.workspace_dir not in path.parents and path != self.workspace_dir:
            raise ValueError(
                f"Unsafe path access blocked: {relative_path}"
            )

        return path

    def _validate_readable_text_file(self, path: Path) -> None:
        """
        Validate that the path is an existing supported text file.
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        if path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension for reading: {path.suffix}"
            )

    def _create_snippet(
        self,
        content: str,
        query: str,
        radius: int = 80,
    ) -> str:
        """
        Create a small snippet around the first query occurrence.
        """
        lower_content = content.lower()
        index = lower_content.find(query)

        if index == -1:
            return content[: radius * 2].strip()

        start = max(0, index - radius)
        end = min(len(content), index + len(query) + radius)

        snippet = content[start:end].strip()

        if start > 0:
            snippet = "..." + snippet

        if end < len(content):
            snippet = snippet + "..."

        return snippet