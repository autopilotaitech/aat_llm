# aat_llm

> **Experimental** - A local LLM inference server built with FastAPI and llama.cpp. Ollama-compatible API on port 11435.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![Status](https://img.shields.io/badge/status-experimental-orange)

## What is this?

aat_llm is a lightweight local LLM server that loads GGUF models via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) and serves them through a REST API with streaming support. It includes a CLI tool and a dark-themed web UI for chatting with models.

## Features

- REST API for text generation and chat (Ollama-compatible endpoints)
- Streaming token output in real time
- Web UI with three-panel layout (model selector, chat, settings)
- CLI for server management, model pulling, and chatting
- Download models directly from HuggingFace
- Lazy model loading with in-memory caching

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Pull a model from HuggingFace
python cli.py pull bartowski/phi-4-GGUF phi-4-Q4_K_M.gguf

# Start the server
python cli.py serve

# Open the web UI
# http://localhost:11435

# Or chat via CLI
python cli.py run phi-4-Q4_K_M.gguf "Explain quantum computing in one sentence"
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `python cli.py serve` | Start the server |
| `python cli.py list` | List downloaded models |
| `python cli.py run <model> "<prompt>"` | Chat with a model |
| `python cli.py pull <hf_repo> <filename>` | Download a model from HuggingFace |
| `python cli.py delete <model>` | Delete a model |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Text generation (supports streaming) |
| `POST` | `/api/chat` | Chat with message history |
| `GET` | `/api/tags` | List available models |
| `DELETE` | `/api/delete` | Delete a model |
| `POST` | `/api/pull` | Pull model from HuggingFace |
| `GET` | `/health` | Server health check |
| `GET` | `/` | Web UI |
| `GET` | `/docs` | Swagger API docs |

## Project Structure

```
aat_llm/
├── server.py          # FastAPI backend
├── cli.py             # Terminal CLI
├── model_manager.py   # HuggingFace download/list/delete
├── web/
│   └── index.html     # Single-file web UI
├── models/            # GGUF model files (gitignored)
├── test_server.py     # API tests
├── test_cli.py        # CLI tests
├── test_gui.py        # Web UI tests
└── requirements.txt
```

## Running Tests

```bash
pytest test_server.py test_cli.py test_gui.py -v
```

## Requirements

- Python 3.11+
- ~8-10 GB RAM for 14B parameter models (Q4 quantization)
- C++ compiler for llama-cpp-python (auto-detected on most systems)

## Disclaimer

This is an experimental project for learning and personal use. Not intended for production deployments.
