# Generative AI Portfolio

This repository contains a collection of practical Generative AI projects covering multiple AI application areas, including text-based RAG systems, vision-language applications, voice/audio assistants, tool-using AI agents, and a unified portfolio dashboard.

The goal of this portfolio is to demonstrate not only isolated model calls, but complete AI application workflows with clean project structure, configuration management, user interfaces, testing, logging, health checks, documentation, and portfolio-level system presentation.

## Portfolio Overview

| Project | Area | Status | Description |
|---|---|---|---|
| Multimodal AI Workspace | Portfolio Hub | Completed | A unified dashboard that presents all Generative AI projects, capability matrix, health overview, architecture, screenshots, and run commands. |
| AI Study Assistant | RAG / Text | Completed | A Retrieval-Augmented Generation application for asking questions about uploaded lecture documents. |
| AI Image Understanding Assistant | Vision | Completed | A vision-language application for analyzing uploaded images and answering questions about their visual content. |
| AI Voice Meeting Assistant | Voice / Audio | Completed | A voice/audio application for transcribing audio files and generating structured summaries. |
| MCP Workspace Assistant | MCP / Tools | Completed | A tool-connected workspace assistant for safely interacting with local files through MCP-style tools. |

## Unified Portfolio Hub

### Multimodal AI Workspace

Location:

```text
multimodal-ai-workspace/
```

Multimodal AI Workspace is the unified dashboard for this Generative AI portfolio.

It brings the four core projects together in one professional Streamlit interface and provides a system-level overview of the complete portfolio.

The hub includes:

- Portfolio overview
- Project cards
- Capability matrix
- Health overview
- Architecture overview
- Detailed project pages
- Demo screenshots
- Local run commands
- Shared engineering practices

Run locally:

```bash
cd multimodal-ai-workspace
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

The hub does not replace the individual projects. Each project remains independently runnable and maintainable.

## Projects

### 1. AI Study Assistant

Location:

```text
ai-study-assistant/
```

AI Study Assistant is a Retrieval-Augmented Generation application for studying lecture materials. Users can upload PDF or TXT files, build a local FAISS knowledge base, and ask questions grounded in the uploaded documents.

Main features:

- PDF and TXT document upload
- Document loading and chunking
- Embedding generation
- FAISS vector storage
- RAG-based question answering
- Source previews for generated answers
- Streamlit chat interface
- Arabic RTL support
- Chat history export
- Evaluation script
- Unit tests
- Health check
- Demo screenshot support

Run locally:

```bash
cd ai-study-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

### 2. AI Image Understanding Assistant

Location:

```text
vision-image-analyzer/
```

AI Image Understanding Assistant is a vision-language application that allows users to upload images and ask questions about their visual content. The system uses a vision-capable language model to describe images, interpret screenshots or slides, and answer user questions.

Main features:

- PNG, JPG, JPEG, and WEBP image upload
- Image validation and metadata extraction
- Base64 image encoding
- Vision model prompting
- Image question answering
- Streamlit chat interface
- Arabic RTL support
- Analysis history export
- Automatic JSON result saving
- CLI support
- Unit tests
- Health check
- Demo screenshot support

Run locally:

```bash
cd vision-image-analyzer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

### 3. AI Voice Meeting Assistant

Location:

```text
voice-meeting-assistant/
```

AI Voice Meeting Assistant is a voice/audio Generative AI application that allows users to upload audio files, transcribe speech into text, and generate structured summaries.

Main features:

- MP3, WAV, M4A, WEBM, and MP4 audio upload
- Audio validation and metadata extraction
- Speech-to-text transcription
- Transcript summarization
- Structured summaries with key points, action items, decisions, open questions, and keywords
- Streamlit interface
- Arabic RTL support
- JSON result export
- Automatic result saving
- CLI support
- Unit tests
- Health check
- Demo screenshot support

Run locally:

```bash
cd voice-meeting-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

### 4. MCP Workspace Assistant

Location:

```text
mcp-workspace-assistant/
```

MCP Workspace Assistant is a tool-connected Generative AI application that demonstrates how an assistant can safely interact with a local workspace through structured tools.

The assistant can list files, read text files, write notes, append content, search workspace files, and create task files. All file operations are restricted to a controlled local workspace to prevent unsafe path access.

Main features:

- Safe local workspace interaction
- Workspace file listing
- Safe text file reading
- Markdown note creation
- Note appending
- Workspace text search
- Markdown task file generation
- MCP-style tool abstraction
- Deterministic assistant pipeline
- Path traversal protection
- Streamlit chat interface
- Tool details shown as JSON
- Chat history export
- CLI support
- Unit tests
- Health check
- Demo screenshot support

Run locally:

```bash
cd mcp-workspace-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Repository Structure

```text
generative-ai/
│
├── multimodal-ai-workspace/
│   ├── app/
│   ├── tests/
│   ├── assets/
│   ├── streamlit_app.py
│   ├── health_check.py
│   └── README.md
│
├── ai-study-assistant/
│   ├── app/
│   ├── tests/
│   ├── assets/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── vision-image-analyzer/
│   ├── app/
│   ├── tests/
│   ├── assets/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── voice-meeting-assistant/
│   ├── app/
│   ├── tests/
│   ├── assets/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── mcp-workspace-assistant/
│   ├── app/
│   ├── tests/
│   ├── assets/
│   ├── workspace/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
└── README.md
```

## Common Engineering Practices Used

Across the projects, the portfolio follows a consistent software engineering approach:

- Clear project structure
- Environment-based configuration
- `.env.example` files for safe setup
- `.gitignore` protection for secrets and generated files
- Logging
- Health checks
- Unit tests
- Streamlit interfaces
- CLI entry points
- Documentation
- Demo screenshot support
- Separation of concerns between loading, processing, pipeline logic, tools, and UI
- Independent project execution
- Portfolio-level dashboard for unified presentation

## Safety and Privacy Notes

- API keys are stored locally in `.env` files and are not committed to GitHub.
- Uploaded files, generated outputs, vector databases, logs, workspace files, and virtual environments are ignored by Git.
- Demo files should not contain private or sensitive information.
- Each project includes its own README with setup and usage instructions.
- The MCP Workspace Assistant restricts file operations to a controlled local workspace.

## Tech Stack

The portfolio uses different tools depending on the project, including:

- Python
- Streamlit
- OpenAI API
- LangChain
- FAISS
- Pillow
- Pydantic
- pytest
- Git / GitHub

## Purpose

This repository is intended as a practical Generative AI portfolio. It is designed to show applied AI development skills across multiple modalities and system types:

- Text and retrieval systems
- Vision-language systems
- Audio and speech systems
- Tool-connected agents
- Unified portfolio dashboards

The focus is not only on using AI models, but on building complete, understandable, maintainable, and extensible AI applications.

The repository demonstrates how Generative AI systems can be structured with user interfaces, command-line entry points, testing, health checks, logging, documentation, safe configuration, and clear separation between application layers.