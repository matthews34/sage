# SAGE
**Smart Autonomous General-purpose Engine**

An AI-powered application framework built for edge devices, specifically optimized for Raspberry Pi.

## Features

- **FastAPI Backend** - High-performance REST API
- **Local LLM** - Ollama integration for private AI inference
- **Speech-to-Text** - Faster Whisper for voice input
- **Text-to-Speech** - Coqui TTS for voice output
- **Vector Storage** - ChromaDB for semantic search
- **PostgreSQL** - Reliable data persistence

## Tech Stack

### Backend
- Python 3.11+
- FastAPI (API server)
- SQLAlchemy (ORM)
- ChromaDB (vector storage)
- Pydantic (validation)

### AI/ML
- Ollama (LLM runtime)
- Faster-Whisper (STT)
- Coqui TTS (speech synthesis)
- Sentence-Transformers (embeddings)

## Quick Start

### Requirements
- Raspberry Pi 4 (4GB+) or Raspberry Pi 5
- Docker & Docker Compose installed
- 32GB+ storage

### Deploy with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/sage.git
cd sage

# Configure environment
cp .env.example .env

# Start services
docker compose up -d

# Pull AI model
docker exec -it sage-ollama ollama pull tinyllama

# Check status
docker compose ps
```

Access the API at `http://localhost:8000`

## Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete Raspberry Pi setup instructions
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

## Architecture

```
┌─────────────────┐
│   SAGE API      │  FastAPI application
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    │         │         │          │
┌───▼───┐ ┌──▼──┐ ┌────▼────┐ ┌───▼────┐
│Ollama │ │PG   │ │ChromaDB │ │Models  │
│LLM    │ │SQL  │ │Vectors  │ │& Data  │
└───────┘ └─────┘ └─────────┘ └────────┘
```

## Resource Usage

Optimized for Raspberry Pi with configurable limits:
- **SAGE App**: 2GB RAM max
- **Ollama**: 3GB RAM max
- **PostgreSQL**: 512MB RAM max
- **ChromaDB**: 1GB RAM max

## License

See [LICENSE](LICENSE) file for details.
