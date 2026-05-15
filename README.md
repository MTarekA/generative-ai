# Generative AI Portfolio

This repository contains a collection of practical Generative AI projects covering different AI application areas, including text-based RAG systems, vision-language applications, voice/audio assistants, and tool-using AI agents.

The goal of this portfolio is to demonstrate not only isolated model calls, but complete AI application workflows with clean project structure, configuration management, user interfaces, testing, logging, health checks, and documentation.

## Portfolio Overview

| Project | Area | Status | Description |
|---|---|---|---|
| AI Study Assistant | RAG / Text | Completed | A Retrieval-Augmented Generation application for asking questions about uploaded lecture documents. |
| AI Image Understanding Assistant | Vision | Completed | A vision-language application for analyzing uploaded images and answering questions about their visual content. |
| AI Voice Meeting Assistant | Voice / Audio | Completed | A voice/audio application for transcribing audio files and generating structured summaries. |
| MCP Workspace Assistant | MCP / Tools | Planned | A tool-connected AI assistant for interacting with local workspace files and structured tools. |


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

Status: Planned

Location:

```text
mcp-workspace-assistant/
```

This project will focus on connecting an AI assistant with local workspace tools and resources through an MCP-style architecture.

The goal is to show how an LLM can interact with external tools in a structured and controlled way instead of only generating text.

Planned features:

- Workspace file listing
- Safe text file reading
- Note creation and editing
- Task file generation
- Local workspace search
- Tool-calling assistant pipeline
- Streamlit interface
- CLI support
- Logging, tests, and documentation

## Repository Structure

```text
generative-ai/
│
├── ai-study-assistant/
│   ├── app/
│   ├── tests/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── vision-image-analyzer/
│   ├── app/
│   ├── tests/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── voice-meeting-assistant/
│   ├── app/
│   ├── tests/
│   ├── streamlit_app.py
│   ├── run.py
│   ├── health_check.py
│   └── README.md
│
├── mcp-workspace-assistant/
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
- Separation of concerns between loading, processing, pipeline logic, and UI

## Safety and Privacy Notes

- API keys are stored locally in `.env` files and are not committed to GitHub.
- Uploaded files, generated outputs, vector databases, logs, and virtual environments are ignored by Git.
- Demo files should not contain private or sensitive information.
- Each project includes its own README with setup and usage instructions.

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
- Tool-using agents

The focus is on building complete, understandable, and extensible AI applications rather than isolated experiments.