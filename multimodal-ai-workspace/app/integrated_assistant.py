from dataclasses import dataclass
from typing import Any

from app.integrated_workspace_tools import IntegratedWorkspaceTools


@dataclass
class IntegratedAssistantResponse:
    """
    Structured response returned by the integrated assistant.
    """

    message: str
    tool_name: str
    tool_result: Any


class IntegratedWorkspaceAssistant:
    """
    Deterministic integrated assistant for workspace tools.
    """

    def __init__(
        self,
        tools: IntegratedWorkspaceTools | None = None,
    ) -> None:
        self.tools = tools or IntegratedWorkspaceTools()

    def handle_message(self, message: str) -> IntegratedAssistantResponse:
        """
        Handle a user command and route it to the appropriate tool.
        """
        clean_message = message.strip()

        if not clean_message:
            raise ValueError("Message cannot be empty.")

        lowered = clean_message.lower()

        if lowered in {"help", "commands", "مساعدة", "الاوامر", "الأوامر"}:
            return self._help_response()

        if lowered in {"list files", "list", "files", "show files"}:
            return self._handle_list_files()

        if lowered.startswith("read "):
            relative_path = clean_message[5:].strip()
            return self._handle_read_file(relative_path)

        if lowered.startswith("search "):
            query = clean_message[7:].strip()
            return self._handle_search(query)

        if lowered.startswith("write note "):
            return self._handle_write_note(clean_message)

        if lowered.startswith("append note "):
            return self._handle_append_note(clean_message)

        if lowered.startswith("create task "):
            return self._handle_create_task(clean_message)

        return IntegratedAssistantResponse(
            message=(
                "I could not understand the command. "
                "Type 'help' to see supported commands."
            ),
            tool_name="none",
            tool_result=None,
        )

    def _help_response(self) -> IntegratedAssistantResponse:
        """
        Return supported command examples.
        """
        message = """
Supported commands:

- help
- list files
- read notes/example.md
- search keyword
- write note file_name | note content
- append note file_name | content to append
- create task file_name | Task title | task 1; task 2; task 3

Examples:
- write note project_idea | This is my project idea.
- append note project_idea | More details here.
- create task next_steps | Next Steps | Build UI; Add tests; Write README
"""
        return IntegratedAssistantResponse(
            message=message.strip(),
            tool_name="help",
            tool_result=None,
        )

    def _handle_list_files(self) -> IntegratedAssistantResponse:
        """
        Handle file listing.
        """
        files = self.tools.list_workspace_files()

        if not files:
            message = "No files found in the integrated workspace."
        else:
            lines = ["Integrated workspace files:"]
            for file in files:
                lines.append(
                    f"- {file['relative_path']} "
                    f"({file['size_bytes']} bytes)"
                )
            message = "\n".join(lines)

        return IntegratedAssistantResponse(
            message=message,
            tool_name="list_workspace_files",
            tool_result=files,
        )

    def _handle_read_file(
        self,
        relative_path: str,
    ) -> IntegratedAssistantResponse:
        """
        Handle reading a file.
        """
        if not relative_path:
            raise ValueError("Please provide a file path to read.")

        result = self.tools.read_workspace_file(relative_path)

        return IntegratedAssistantResponse(
            message=(
                f"Content of {relative_path}:\n\n"
                f"{result['content']}"
            ),
            tool_name="read_workspace_file",
            tool_result=result,
        )

    def _handle_search(self, query: str) -> IntegratedAssistantResponse:
        """
        Handle workspace search.
        """
        if not query:
            raise ValueError("Please provide a search query.")

        results = self.tools.search_workspace(query)

        if not results:
            message = f"No results found for: {query}"
        else:
            lines = [f"Search results for '{query}':"]
            for result in results:
                lines.append(
                    f"- {result['relative_path']}: "
                    f"{result['snippet']}"
                )
            message = "\n".join(lines)

        return IntegratedAssistantResponse(
            message=message,
            tool_name="search_workspace",
            tool_result=results,
        )

    def _handle_write_note(
        self,
        command: str,
    ) -> IntegratedAssistantResponse:
        """
        Handle note creation.

        Expected format:
        write note file_name | note content
        """
        payload = command[len("write note "):].strip()

        file_name, content = self._split_pipe_payload(
            payload=payload,
            expected_parts=2,
            usage="write note file_name | note content",
        )

        result = self.tools.write_workspace_note(
            file_name=file_name,
            content=content,
            overwrite=True,
        )

        return IntegratedAssistantResponse(
            message=(
                f"Note written successfully: "
                f"{result['relative_path']}"
            ),
            tool_name="write_workspace_note",
            tool_result=result,
        )

    def _handle_append_note(
        self,
        command: str,
    ) -> IntegratedAssistantResponse:
        """
        Handle appending to a note.

        Expected format:
        append note file_name | content to append
        """
        payload = command[len("append note "):].strip()

        file_name, content = self._split_pipe_payload(
            payload=payload,
            expected_parts=2,
            usage="append note file_name | content to append",
        )

        result = self.tools.append_workspace_note(
            file_name=file_name,
            content=f"\n\n{content}",
        )

        return IntegratedAssistantResponse(
            message=(
                f"Content appended successfully: "
                f"{result['relative_path']}"
            ),
            tool_name="append_workspace_note",
            tool_result=result,
        )

    def _handle_create_task(
        self,
        command: str,
    ) -> IntegratedAssistantResponse:
        """
        Handle task file creation.

        Expected format:
        create task file_name | Task title | task 1; task 2; task 3
        """
        payload = command[len("create task "):].strip()

        file_name, title, tasks_text = self._split_pipe_payload(
            payload=payload,
            expected_parts=3,
            usage=(
                "create task file_name | Task title | "
                "task 1; task 2; task 3"
            ),
        )

        tasks = [
            task.strip()
            for task in tasks_text.split(";")
            if task.strip()
        ]

        if not tasks:
            raise ValueError("Please provide at least one task.")

        result = self.tools.create_task_file(
            file_name=file_name,
            title=title,
            tasks=tasks,
            overwrite=True,
        )

        return IntegratedAssistantResponse(
            message=(
                f"Task file created successfully: "
                f"{result['relative_path']} "
                f"({result['task_count']} tasks)"
            ),
            tool_name="create_task_file",
            tool_result=result,
        )

    def _split_pipe_payload(
        self,
        payload: str,
        expected_parts: int,
        usage: str,
    ) -> list[str]:
        """
        Split a pipe-separated command payload.
        """
        parts = [part.strip() for part in payload.split("|")]

        if len(parts) != expected_parts or any(not part for part in parts):
            raise ValueError(f"Invalid command format. Use: {usage}")

        return parts