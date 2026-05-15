# Generative AI Portfolio

This repository contains a collection of practical Generative AI projects covering different AI application areas, including text-based RAG systems, vision-language applications, voice/audio assistants, and tool-using AI agents.

The goal of this portfolio is to demonstrate not only isolated model calls, but complete AI application workflows with clean project structure, configuration management, user interfaces, testing, logging, health checks, and documentation.

## Portfolio Overview

| Project | Area | Status | Description |
|---|---|---|---|
| AI Study Assistant | RAG / Text | Completed | A Retrieval-Augmented Generation application for asking questions about uploaded lecture documents. |
| AI Image Understanding Assistant | Vision | Completed | A vision-language application for analyzing uploaded images and answering questions about their visual content. |
| Voice Meeting Assistant | Voice / Audio | Planned | A speech-to-text and summarization assistant for audio recordings and meetings. |
| MCP Workspace Agent | MCP / Tools | Planned | An AI agent connected to external tools and local workspace resources using an MCP-style architecture. |

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

### 3. Voice Meeting Assistant

Status: Planned

This project will focus on voice and audio processing. The planned system will allow users to upload or record audio, transcribe speech into text, summarize the content, extract action items, and generate structured notes.

Planned features:

- Audio upload
- Speech-to-text transcription
- Meeting summarization
- Action item extraction
- Multilingual support
- Exportable summaries
- Streamlit interface
- Health check and tests

### 4. MCP Workspace Agent

Status: Planned

This project will focus on connecting AI models with external tools and local workspace resources. The goal is to build an agent that can interact with files, structured data, and tools through a clean tool-using architecture.

Planned features:

- Tool-using AI agent
- Local file interaction
- JSON and CSV reading
- Task execution through tools
- Workspace assistant interface
- MCP-style architecture
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
│
├── mcp-workspace-agent/
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