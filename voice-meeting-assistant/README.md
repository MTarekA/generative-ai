# AI Voice Meeting Assistant

AI Voice Meeting Assistant is a Generative AI voice/audio project that allows users to upload audio files, transcribe speech into text, and generate structured summaries.

The application is designed for short meetings, study recordings, voice notes, and audio explanations. It combines speech-to-text transcription with LLM-based summarization to produce useful outputs such as key points, action items, decisions, open questions, and keywords.

## Project Goal

The goal of this project is to demonstrate a practical Voice / Audio Generative AI workflow that combines:

- Audio upload and validation
- Audio metadata extraction
- Speech-to-text transcription
- Transcript summarization
- Structured meeting notes
- Action item extraction
- Result saving as JSON
- Streamlit user interface
- Command-line interface
- Local logging
- Health checks
- Unit testing

This project is part of a larger Generative AI portfolio.

## Features

- Upload MP3, WAV, M4A, WEBM, and MP4 audio files
- Validate audio files before processing
- Extract basic audio metadata
- Transcribe audio using OpenAI transcription models
- Summarize transcripts using an LLM
- Generate structured summaries
- Extract key points, action items, decisions, open questions, and keywords
- Display transcript and summary in a Streamlit UI
- Arabic RTL rendering support
- Save complete analysis results automatically as JSON
- Download the latest result as JSON
- Command-line interface for audio analysis
- Structured logging
- Health check script
- Unit tests with pytest

## System Architecture

```text
User uploads audio
        ↓
Audio Loader
        ↓
Audio validation + metadata
        ↓
Transcription Pipeline
        ↓
Transcript
        ↓
Summarization Pipeline
        ↓
Structured Summary
        ↓
Result Manager
        ↓
Saved JSON Result
```

## Project Structure

```text
voice-meeting-assistant/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── audio_loader.py
│   ├── transcription_pipeline.py
│   ├── summarization_pipeline.py
│   ├── result_manager.py
│   ├── logger.py
│   ├── prompts.py
│   └── utils.py
│
├── data/
│   └── uploaded_audio/
│       └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
├── logs/
│
├── tests/
│   ├── test_audio_loader.py
│   ├── test_result_manager.py
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

TRANSCRIPTION_PROVIDER=openai
SUMMARIZATION_PROVIDER=openai

OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
OPENAI_SUMMARY_MODEL=gpt-4o-mini

APP_NAME=AI Voice Meeting Assistant
DEBUG=True
```

Important: never commit `.env` to GitHub.

## Usage

### Option 1: Run the Streamlit app

```bash
python -m streamlit run streamlit_app.py
```

Then:

1. Upload a short audio file from the sidebar.
2. Play the audio inside the app if needed.
3. Click `Analyze Audio`.
4. Review the transcript.
5. Review the structured summary.
6. Download the JSON result if needed.

### Option 2: Run from the command line

Analyze an audio file:

```bash
python run.py analyze data\uploaded_audio\test_audio.mp3
```

The CLI will:

- Transcribe the audio
- Summarize the transcript
- Print the result
- Save the full analysis as JSON inside `outputs/`

## Example Use Cases

- Meeting note generation
- Study recording summarization
- Voice note transcription
- Lecture audio summarization
- Extracting action items from discussions
- Creating structured notes from short audio files

## Example Output Sections

The generated summary is designed to include:

1. Short summary
2. Key points
3. Action items
4. Decisions
5. Open questions
6. Keywords

If the transcript does not contain action items, decisions, or open questions, the assistant should say that clearly instead of inventing them.

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
- Uploaded audio files are available
- Analysis output files exist

## Tests

Run unit tests:

```bash
python -m pytest
```

Expected result:

```text
6 passed
```

## Logging

The project writes logs to:

```text
logs/app.log
```

Log files are ignored by Git.

## Saved Results

Each audio analysis is saved automatically as a JSON file inside:

```text
outputs/
```

Example result structure:

```json
{
  "result_id": "...",
  "created_at": "...",
  "audio_path": "...",
  "audio_metadata": {
    "file_name": "...",
    "file_extension": ".mp3",
    "file_size_bytes": 255265,
    "file_size_mb": 0.24
  },
  "transcription_model": "gpt-4o-mini-transcribe",
  "summary_model": "gpt-4o-mini",
  "transcript": "...",
  "summary": "..."
}
```

Generated output files are ignored by Git.

## Supported Audio Types

```text
.mp3
.wav
.m4a
.webm
.mp4
```

## Quality and Safety Behavior

The assistant is instructed to summarize only the provided transcript.

If the transcript does not contain action items, decisions, or open questions, the assistant should state that clearly instead of inventing details.

## Limitations

- The quality of transcription depends on audio clarity.
- Noisy audio may reduce transcription accuracy.
- Long audio files may take more time and cost more to process.
- The current version is designed for local single-user use.
- The project currently uses OpenAI models by default.
- API usage may incur costs depending on the provider.

## Future Improvements

- Add audio duration extraction
- Add automatic audio compression
- Add long-audio chunking
- Add speaker diarization
- Add multilingual language detection
- Add persistent session history
- Add batch audio processing
- Add local Whisper / faster-whisper option
- Add Docker support
- Add deployment instructions
- Add demo screenshot

## Tech Stack

- Python
- Streamlit
- OpenAI API
- Pydantic
- pydub
- pytest

## License

This project is intended for educational and portfolio purposes.