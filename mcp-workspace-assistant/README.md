# MCP Workspace Assistant

MCP Workspace Assistant is a tool-connected Generative AI project that demonstrates how an AI assistant can interact with a local workspace through safe, structured tools.

The project follows an MCP-style architecture, where the assistant does not directly access files. Instead, it uses controlled tools for listing files, reading text files, writing notes, appending content, searching the workspace, and creating task files.

## Project Goal

The goal of this project is to demonstrate a practical tool-using AI assistant that can interact with external resources in a controlled and safe way.

This project focuses on:

- Local workspace interaction
- Safe file access
- Tool-based architecture
- Deterministic command routing
- MCP-style tool design
- Workspace search
- Note creation
- Task file generation
- Streamlit user interface
- Command-line interface
- Logging
- Health checks
- Unit testing

This project is part of a larger Generative AI portfolio.

## Features

- List files inside a local workspace
- Read supported text files safely
- Write Markdown notes
- Append content to existing notes
- Search inside workspace text files
- Create Markdown task files
- Prevent access outside the workspace
- MCP-style tool abstraction
- Deterministic assistant pipeline
- Interactive CLI mode
- Streamlit chat interface
- Tool details shown as JSON
- Chat history export
- Arabic RTL rendering support
- Structured logging
- Health check script
- Unit tests with pytest

## System Architecture

```text
User command
        ↓
Assistant Pipeline
        ↓
Intent routing
        ↓
Workspace Tools
        ↓
Workspace Manager
        ↓
Safe local workspace
        ↓
Tool result
        ↓
Assistant response
```

## Safety Design

The assistant never performs direct file operations from the UI or CLI.

All file access goes through `WorkspaceManager`, which restricts paths to:

```text
workspace/
```

Unsafe paths such as:

```text
../../secret.txt
```

are blocked by design.

This prevents path traversal and keeps all operations inside the controlled project workspace.

## Project Structure

```text
mcp-workspace-assistant/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── workspace_manager.py
│   ├── tools.py
│   ├── assistant_pipeline.py
│   ├── logger.py
│   ├── prompts.py
│   ├── result_manager.py
│   └── utils.py
│
├── workspace/
│   ├── documents/
│   │   └── .gitkeep
│   ├── notes/
│   │   └── .gitkeep
│   └── tasks/
│       └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
├── logs/
│
├── tests/
│   ├── test_workspace_manager.py
│   ├── test_tools.py
│   ├── test_assistant_pipeline.py
│   └── test_text_direction.py
│
├── streamlit_app.py
├── run.py
├── health_check.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## Supported Commands

```text
help
list files
read notes/example.md
search keyword
write note file_name | note content
append note file_name | content to append
create task file_name | Task title | task 1; task 2; task 3
```

## Example Commands

```text
write note project_idea | This is my project idea.
append note project_idea | More details about the project.
read notes/project_idea.md
search project
create task next_steps | Next Steps | Build UI; Add tests; Write README
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

Windows PowerShell:

```bash
.venv\Scripts\activate
```

If activation is blocked:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=your_openai_api_key_here

PRIMARY_LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini

APP_NAME=MCP Workspace Assistant
DEBUG=True

MAX_FILE_READ_CHARS=8000
MAX_SEARCH_RESULTS=10
```

Important: never commit `.env` to GitHub.

## Usage

### Option 1: Run the Streamlit app

```bash
python -m streamlit run streamlit_app.py
```

Then use the chat interface to run commands such as:

```text
help
list files
write note demo | This note was created from the UI.
read notes/demo.md
search demo
create task demo_tasks | Demo Tasks | Build UI; Add tests
```

### Option 2: Run one command from the CLI

```bash
python run.py ask "list files"
```

Write a note:

```bash
python run.py ask "write note cli_test | This note was created from the CLI."
```

Read a note:

```bash
python run.py ask "read notes/cli_test.md"
```

Create a task file:

```bash
python run.py ask "create task next_steps | Next Steps | Build UI; Add tests; Write README"
```

### Option 3: Run interactive CLI chat

```bash
python run.py chat
```

Then type commands interactively.

## Health Check

Run:

```bash
python health_check.py
```

The script checks whether:

- `.env` exists
- Settings are valid
- Important project files exist
- Required directories exist
- Workspace access works
- Unsafe path traversal is blocked
- Output files exist, if generated

A warning about missing output files is acceptable if no outputs have been generated yet.

## Tests

Run unit tests:

```bash
python -m pytest
```

Expected result:

```text
13 passed
```

## Logging

The project writes logs to:

```text
logs/app.log
```

Log files are ignored by Git.

## Workspace Policy

Files created during local use are stored inside:

```text
workspace/
```

The `.gitignore` prevents generated or private workspace files from being committed, while keeping the folder structure through `.gitkeep` files.

Ignored generated workspace content includes:

```text
workspace/notes/*
workspace/tasks/*
workspace/documents/*
```

Only these placeholder files are tracked:

```text
workspace/notes/.gitkeep
workspace/tasks/.gitkeep
workspace/documents/.gitkeep
```

## Quality and Safety Behavior

The assistant uses deterministic command routing in the current version. This makes the system predictable, testable, and safe before adding more advanced LLM tool-calling behavior.

If the assistant does not understand a command, it asks the user to type `help` instead of performing unsafe or unclear actions.

## Limitations

- The current assistant uses deterministic command routing, not full OpenAI function calling yet.
- Only local text-based workspace operations are supported.
- Supported readable and writable file types are `.txt`, `.md`, `.json`, and `.csv`.
- Workspace content is local and not intended for deployment storage.
- The current version is designed for local single-user use.

## Future Improvements

- Add OpenAI function calling / tool calling
- Add full MCP server-client protocol implementation
- Add file upload from the UI
- Add better natural language command interpretation
- Add workspace summarization
- Add CSV analysis tools
- Add JSON inspection tools
- Add persistent session history
- Add Docker support
- Add deployment instructions
- Add demo screenshots

## Tech Stack

- Python
- Streamlit
- Pydantic
- pytest
- OpenAI API-ready configuration
- Local workspace tools

## License

This project is intended for educational and portfolio purposes.