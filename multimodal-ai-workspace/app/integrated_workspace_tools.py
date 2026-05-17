from dataclasses import asdict

from app.integrated_workspace_manager import IntegratedWorkspaceManager


class IntegratedWorkspaceTools:
    """
    MCP-style tools for the integrated workspace demo.
    """

    def __init__(
        self,
        manager: IntegratedWorkspaceManager | None = None,
    ) -> None:
        self.manager = manager or IntegratedWorkspaceManager()

    def list_workspace_files(self) -> list[dict]:
        """
        List all files inside the integrated workspace.
        """
        files = self.manager.list_files()
        return [asdict(file) for file in files]

    def read_workspace_file(self, relative_path: str) -> dict:
        """
        Read a text file from the integrated workspace.
        """
        content = self.manager.read_text_file(
            relative_path=relative_path,
            max_chars=8000,
        )

        return {
            "relative_path": relative_path,
            "content": content,
            "truncated_to_chars": 8000,
        }

    def write_workspace_note(
        self,
        file_name: str,
        content: str,
        overwrite: bool = False,
    ) -> dict:
        """
        Write a Markdown note inside integrated_workspace/notes.
        """
        safe_file_name = self._normalize_markdown_file_name(file_name)
        relative_path = f"notes/{safe_file_name}"

        path = self.manager.write_text_file(
            relative_path=relative_path,
            content=content,
            overwrite=overwrite,
        )

        return {
            "status": "success",
            "relative_path": str(path.relative_to(self.manager.workspace_dir)),
            "message": "Note written successfully.",
        }

    def append_workspace_note(
        self,
        file_name: str,
        content: str,
    ) -> dict:
        """
        Append content to a Markdown note.
        """
        safe_file_name = self._normalize_markdown_file_name(file_name)
        relative_path = f"notes/{safe_file_name}"

        path = self.manager.append_text_file(
            relative_path=relative_path,
            content=content,
        )

        return {
            "status": "success",
            "relative_path": str(path.relative_to(self.manager.workspace_dir)),
            "message": "Content appended successfully.",
        }

    def create_task_file(
        self,
        file_name: str,
        title: str,
        tasks: list[str],
        overwrite: bool = False,
    ) -> dict:
        """
        Create a Markdown task file inside integrated_workspace/tasks.
        """
        safe_file_name = self._normalize_markdown_file_name(file_name)
        relative_path = f"tasks/{safe_file_name}"

        task_lines = "\n".join(f"- [ ] {task}" for task in tasks)
        content = f"# {title}\n\n{task_lines}\n"

        path = self.manager.write_text_file(
            relative_path=relative_path,
            content=content,
            overwrite=overwrite,
        )

        return {
            "status": "success",
            "relative_path": str(path.relative_to(self.manager.workspace_dir)),
            "message": "Task file created successfully.",
            "task_count": len(tasks),
        }

    def search_workspace(self, query: str) -> list[dict]:
        """
        Search supported text files inside the integrated workspace.
        """
        return self.manager.search_text_files(
            query=query,
            max_results=10,
        )

    def _normalize_markdown_file_name(self, file_name: str) -> str:
        """
        Normalize a user-provided name into a safe Markdown file name.
        """
        clean_name = file_name.strip().replace("\\", "/").split("/")[-1]

        if not clean_name:
            raise ValueError("File name cannot be empty.")

        if not clean_name.endswith(".md"):
            clean_name = f"{clean_name}.md"

        return clean_name