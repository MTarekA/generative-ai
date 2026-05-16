from dataclasses import dataclass
from typing import Any

from app.tools import WorkspaceTools


@dataclass
class AssistantResponse:
    """
    Structured response returned by the assistant pipeline.

    message:
        Human-readable response.

    tool_name:
        Name of the tool that was used.

    tool_result:
        Raw structured result returned by the tool.
    """

    message: str
    tool_name: str
    tool_result: Any


class AssistantPipeline:
    """
    Simple MCP-style assistant pipeline.

    This pipeline maps user commands to safe workspace tools.
    It is intentionally deterministic at this stage, so the behavior is
    testable, explainable, and safe before adding LLM tool-calling.
    """

    def __init__(self, tools: WorkspaceTools | None = None) -> None:
        self.tools = tools or WorkspaceTools()

    def handle_message(self, message: str) -> AssistantResponse:
        """
        Handle a user message and route it to the appropriate tool.
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

        return AssistantResponse(
            message=(
                "I could not understand the command. "
                "Type 'help' to see supported commands."
            ),
            tool_name="none",
            tool_result=None,
        )

    def _help_response(self) -> AssistantResponse:
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
        return AssistantResponse(
            message=message.strip(),
            tool_name="help",
            tool_result=None,
        )

    def _handle_list_files(self) -> AssistantResponse:
        """
        Handle file listing.
        """
        files = self.tools.list_workspace_files()

        if not files:
            message = "No files found in the workspace."
        else:
            lines = ["Workspace files:"]
            for file in files:
                lines.append(
                    f"- {file['relative_path']} "
                    f"({file['size_bytes']} bytes)"
                )
            message = "\n".join(lines)

        return AssistantResponse(
            message=message,
            tool_name="list_workspace_files",
            tool_result=files,
        )

    def _handle_read_file(self, relative_path: str) -> AssistantResponse:
        """
        Handle reading a file.
        """
        if not relative_path:
            raise ValueError("Please provide a file path to read.")

        result = self.tools.read_workspace_file(relative_path)

        message = (
            f"Content of {relative_path}:\n\n"
            f"{result['content']}"
        )

        return AssistantResponse(
            message=message,
            tool_name="read_workspace_file",
            tool_result=result,
        )

    def _handle_search(self, query: str) -> AssistantResponse:
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

        return AssistantResponse(
            message=message,
            tool_name="search_workspace",
            tool_result=results,
        )

    def _handle_write_note(self, command: str) -> AssistantResponse:
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

        return AssistantResponse(
            message=(
                f"Note written successfully: "
                f"{result['relative_path']}"
            ),
            tool_name="write_workspace_note",
            tool_result=result,
        )

    def _handle_append_note(self, command: str) -> AssistantResponse:
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

        return AssistantResponse(
            message=(
                f"Content appended successfully: "
                f"{result['relative_path']}"
            ),
            tool_name="append_workspace_note",
            tool_result=result,
        )

    def _handle_create_task(self, command: str) -> AssistantResponse:
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

        return AssistantResponse(
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
        Split a command payload separated by pipe characters.
        """
        parts = [part.strip() for part in payload.split("|")]

        if len(parts) != expected_parts or any(not part for part in parts):
            raise ValueError(f"Invalid command format. Use: {usage}")

        return parts


if __name__ == "__main__":
    assistant = AssistantPipeline()

    demo_commands = [
        "help",
        "write note demo | This note was created by the assistant pipeline.",
        "append note demo | This line was appended later.",
        "create task demo_tasks | Demo Tasks | Build tools; Add UI; Write tests",
        "list files",
        "read notes/demo.md",
        "search assistant",
    ]

    for command in demo_commands:
        print("=" * 80)
        print("User:", command)

        response = assistant.handle_message(command)

        print("Tool:", response.tool_name)
        print("Assistant:")
        print(response.message)