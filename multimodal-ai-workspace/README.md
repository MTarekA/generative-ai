# Multimodal AI Workspace

Multimodal AI Workspace is a unified Generative AI portfolio dashboard that brings together multiple AI application areas in one professional Streamlit interface.

The project acts as a system-level hub for four independently built Generative AI projects:

- Retrieval-Augmented Generation / Text
- Vision-Language Understanding
- Voice / Audio Processing
- MCP-style Tool-Connected Workspace Assistant

Instead of merging all projects into one large and fragile codebase, this workspace provides a clean overview layer that presents capabilities, architecture, health status, screenshots, and local run instructions for each project.

## Project Goal

The goal of this project is to demonstrate portfolio-level system thinking.

This project shows how multiple Generative AI applications can be organized, documented, compared, and presented through one unified dashboard while keeping each project independently runnable and maintainable.

The dashboard highlights:

- Project overview
- Capability matrix
- Health overview
- Architecture overview
- Project details
- Demo screenshots
- Run commands
- Shared engineering practices

## Demo

### Portfolio Overview

![Multimodal AI Workspace - Overview](assets/screenshots/screenshot_overview.png)

### Portfolio Health Overview

![Multimodal AI Workspace - Health Overview](assets/screenshots/screenshot_health_overview.png)

### Project Details

![Multimodal AI Workspace - Project Details](assets/screenshots/screenshot_project_details.png)

## Why This Project Exists

The four individual projects demonstrate practical Generative AI implementation across different modalities.

This hub demonstrates a higher-level engineering perspective:

```text
Individual AI Applications
        ↓
Consistent Engineering Standards
        ↓
Unified Portfolio Dashboard
        ↓
System-Level Presentation
```

This makes the portfolio easier to review, easier to present, and easier to extend.

## Included Projects

| Project | Area | Status | Description |
|---|---|---|---|
| AI Study Assistant | RAG / Text | Completed | A Retrieval-Augmented Generation application for asking questions about uploaded lecture documents. |
| AI Image Understanding Assistant | Vision | Completed | A vision-language application for analyzing uploaded images and answering questions about their visual content. |
| AI Voice Meeting Assistant | Voice / Audio | Completed | A voice/audio application for transcribing audio files and generating structured summaries. |
| MCP Workspace Assistant | MCP / Tools | Completed | A tool-connected workspace assistant for safely interacting with local files through MCP-style tools. |

## Dashboard Sections

The Streamlit dashboard includes the following sections:

### Overview

Shows the complete portfolio at a glance, including:

- Number of projects
- Number of completed projects
- Number of covered AI areas
- Portfolio readiness score
- Project cards
- Shared engineering practices

### Projects

Displays all project cards with:

- Project name
- AI area
- Status
- Folder name
- Description
- Key features
- Local run commands

### Capability Matrix

Provides a compact comparison of the main capabilities across all projects.

### Health Overview

Checks whether each project includes important portfolio-quality elements:

- README
- Streamlit app
- CLI entry point
- Health check
- Tests
- Requirements file
- `.env.example`
- Screenshots

### Architecture

Shows the high-level architecture across the full Generative AI portfolio.

### Project Details

Displays detailed information and screenshots for each individual project.

### Integrated Demo

Provides the first step toward a real unified multimodal workspace.

The currently implemented integrated capabilities are:

- Workspace Tools
- Image Understanding

The remaining planned integrated capabilities are:

- Audio Summary
- Document RAG

## Integrated Demo

The dashboard now includes an `Integrated Demo` section.

This section represents phase two of the portfolio: gradually turning the portfolio hub from a presentation dashboard into a real unified multimodal workspace.

Current integrated capabilities:

- Workspace Tools: implemented
- Image Understanding: implemented
- Audio Summary: planned
- Document RAG: planned

### Workspace Tools

The Workspace Tools tab is fully implemented and runs locally without external API calls.

It supports:

- Listing integrated workspace files
- Writing Markdown notes
- Reading notes
- Appending content to existing notes
- Searching workspace content
- Creating Markdown task files
- Showing structured tool results as JSON
- Safe path handling inside `integrated_workspace/`

Supported commands:

```text
help
list files
write note file_name | note content
append note file_name | content to append
read notes/example.md
search keyword
create task file_name | Task title | task 1; task 2; task 3
```

Generated workspace files are stored inside:

```text
integrated_workspace/
```

Private and generated workspace content is ignored by Git, while `.gitkeep` files preserve the folder structure.

### Image Understanding

The Image Understanding tab is also implemented as part of the integrated demo.

It allows users to upload an image and ask questions about its visual content directly inside the Multimodal AI Workspace.

It supports:

- PNG, JPG, JPEG, and WEBP image upload
- Image preview inside the dashboard
- Vision-language question answering
- Image metadata display
- Chat-style interaction
- Arabic and English questions
- Local image storage inside `integrated_uploads/images/`

The integrated vision backend is implemented through:

```text
app/integrated_image_loader.py
app/integrated_vision_pipeline.py
```

The local image loader handles:

- Image validation
- Metadata extraction
- MIME type detection
- Base64 encoding

The vision pipeline uses an OpenAI vision-capable model configured through:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_VISION_MODEL=gpt-4o-mini
```

Uploaded integrated demo images are ignored by Git.

Planned next integrations:

- Audio Summary tab
- Document RAG tab

## System Architecture

```text
Multimodal AI Workspace
│
├── Project Registry
│   └── Defines all portfolio projects and their metadata
│
├── Health Overview
│   └── Checks project structure, screenshots, tests, and documentation
│
├── Integrated Workspace Tools
│   └── Provides local MCP-style tools inside the integrated demo
│
├── Integrated Vision Backend
│   └── Provides image loading, metadata extraction, Base64 encoding, and vision model access
│
├── UI Components
│   └── Reusable Streamlit rendering components
│
└── Streamlit Dashboard
    └── Unified portfolio interface
```

## Portfolio Architecture

```text
Generative AI Portfolio
│
├── RAG / Text
│   └── Document upload → Chunking → Embeddings → FAISS → LLM answer + sources
│
├── Vision
│   └── Image upload → Validation → Base64 encoding → Vision model → Answer + metadata
│
├── Voice / Audio
│   └── Audio upload → Transcription → Summarization → Structured result
│
├── MCP / Tools
│   └── User command → Assistant router → Tools → Workspace manager → Safe file operations
│
└── Multimodal Workspace Hub
    └── Project registry → Health overview → Integrated demo → Unified presentation
```

## Project Structure

```text
multimodal-ai-workspace/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── project_registry.py
│   ├── health_overview.py
│   ├── integrated_workspace_manager.py
│   ├── integrated_workspace_tools.py
│   ├── integrated_assistant.py
│   ├── integrated_image_loader.py
│   ├── integrated_vision_pipeline.py
│   ├── ui_components.py
│   ├── logger.py
│   └── utils.py
│
├── assets/
│   ├── screenshots/
│   │   └── .gitkeep
│   └── diagrams/
│       └── .gitkeep
│
├── data/
│   └── .gitkeep
│
├── integrated_workspace/
│   ├── documents/
│   │   └── .gitkeep
│   ├── notes/
│   │   └── .gitkeep
│   └── tasks/
│       └── .gitkeep
│
├── integrated_uploads/
│   └── images/
│       └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
├── logs/
│
├── tests/
│   ├── test_project_registry.py
│   ├── test_health_overview.py
│   ├── test_integrated_workspace.py
│   └── test_integrated_image_loader.py
│
├── streamlit_app.py
├── health_check.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
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
APP_NAME=Multimodal AI Workspace
DEBUG=True

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_VISION_MODEL=gpt-4o-mini
```

Important: never commit `.env` to GitHub.

## Usage

Run the dashboard:

```bash
python -m streamlit run streamlit_app.py
```

Then use the sidebar to navigate between:

- Overview
- Projects
- Capability Matrix
- Health Overview
- Architecture
- Project Details
- Integrated Demo

To test the integrated workspace tools, open:

```text
Integrated Demo → Workspace Tools
```

Then try commands such as:

```text
help
list files
write note demo | This note was created inside the integrated workspace.
read notes/demo.md
search integrated
create task demo_tasks | Demo Tasks | Test chat; Check files; Export results
```

To test the integrated vision demo, open:

```text
Integrated Demo → Image Understanding
```

Then upload an image and ask a question such as:

```text
Describe this image briefly.
What is visible in this image?
اشرحلي الصورة دي ببساطة.
```

## Health Check

Run:

```bash
python health_check.py
```

The script checks whether:

- The hub project structure is valid
- Required directories exist
- The project registry contains the four portfolio projects
- The portfolio health overview can be generated
- Registered projects have screenshots

## Tests

Run:

```bash
python -m pytest
```

Expected result:

```text
All tests passed
```

The test suite includes checks for:

- Project registry
- Portfolio health overview
- Integrated workspace file handling
- Integrated workspace tools
- Assistant command routing
- Path traversal protection
- Integrated image loading
- Image metadata extraction
- Base64 image encoding
- Unsupported image validation

## Engineering Practices Demonstrated

Across the full portfolio, the projects follow consistent engineering practices:

- Modular Python structure
- Streamlit user interfaces
- Command-line entry points
- Environment-based configuration
- `.env.example` files
- `.gitignore` protection
- Structured logging
- Health checks
- Unit tests
- README documentation
- Demo screenshots
- Safe handling of generated and private files
- Separation of UI, pipeline logic, tools, and utility layers

## Design Decision

This project intentionally keeps the four main AI projects independent.

Instead of copying all functionality into one large app, the workspace acts as a clean orchestration and presentation layer.

This has several advantages:

- Lower complexity
- Easier debugging
- Independent project execution
- Clearer portfolio structure
- Better maintainability
- Easier future extension

The integrated demo is added incrementally.

The first implemented capability is the local Workspace Tools tab because it is safe, deterministic, testable, and does not require external API calls.

The second implemented capability is the Image Understanding tab, which introduces model-based multimodal analysis while keeping image loading, validation, and metadata extraction separated from the Streamlit UI.

## Future Improvements

- Integrate Audio Transcription and Summary tab
- Integrate Document RAG tab
- Add shared export layer for integrated demos
- Add integrated demo screenshots
- Add more end-to-end tests for integrated tabs
- Add direct launch buttons for local projects
- Add automated subprocess-based health checks
- Add project dependency status checks
- Add combined demo mode
- Add Docker support
- Add deployment instructions
- Add generated architecture diagrams
- Add portfolio export as PDF
- Add CI workflow for tests

## Tech Stack

- Python
- Streamlit
- OpenAI API
- Pillow
- Pydantic
- pytest
- Git / GitHub

## License

This project is intended for educational and portfolio purposes.