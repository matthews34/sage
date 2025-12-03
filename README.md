# SAGE
**Smart Autonomous General-purpose Engine**

A privacy-first virtual assistant powered by locally-run open source AI models, designed for Raspberry Pi edge deployment. SAGE is your personal AI companion that learns about your life, manages your daily tasks, and controls your smart home - all while keeping your data private and secure on your local network.

## What is SAGE?

SAGE is a comprehensive personal AI assistant that runs entirely on your Raspberry Pi. Unlike cloud-based assistants, your data never leaves your device, giving you complete privacy and control.

### Core Capabilities

🧠 **Personal Knowledge Base**
- Store and recall information about your projects, work, and daily life
- Semantic search through your personal knowledge using vector embeddings
- Context-aware responses based on your stored information

📝 **List Management**
- Shopping lists, travel packing lists, project checklists
- Voice-controlled list creation and updates
- API access to your lists from anywhere

🏠 **Smart Home Integration**
- Control smart home devices through voice commands or API
- Integrate with existing IoT devices
- Expandable architecture for new device types

🎤 **Voice Interface**
- Natural language voice commands (Speech-to-Text)
- Voice responses (Text-to-Speech)
- Hands-free operation

🌐 **Remote API Access**
- REST API for accessing your data remotely
- Secure authentication for remote connections
- Mobile-friendly endpoints

🔮 **Extensible Architecture**
- Ready for camera integration
- Sensor data collection and analysis
- Plugin system for future capabilities

## Features

- **Privacy-First** - All data stored locally, no cloud dependencies
- **FastAPI Backend** - High-performance REST API with automatic documentation
- **Local LLM** - Ollama integration for private AI inference (no internet required)
- **Speech-to-Text** - Faster Whisper for accurate voice recognition
- **Text-to-Speech** - Coqui TTS for natural voice responses
- **Vector Storage** - ChromaDB for semantic search and RAG (Retrieval-Augmented Generation)
- **PostgreSQL** - Reliable storage for structured data (lists, devices, conversations)
- **Raspberry Pi Optimized** - Runs efficiently on resource-constrained hardware

## Use Cases

### Personal Knowledge Management
```
You: "Remember that I'm using Python 3.11 for the home automation project"
SAGE: "Got it. I'll remember that your home automation project uses Python 3.11"

[Later...]
You: "What Python version am I using for home automation?"
SAGE: "You're using Python 3.11 for your home automation project"
```

### List Management
```
You: "Add milk and eggs to my shopping list"
SAGE: "Added milk and eggs to your shopping list. You now have 5 items."

You: "What's on my shopping list?"
SAGE: "Your shopping list has: milk, eggs, bread, cheese, and coffee"
```

### Smart Home Control
```
You: "Turn on the living room lights"
SAGE: "Turning on the living room lights"

You: "Set bedroom temperature to 72 degrees"
SAGE: "Setting bedroom thermostat to 72°F"
```

### Remote Access (via API)
```bash
# Check your shopping list while at the store
curl https://sage.home/api/v1/lists/shopping

# Control devices remotely
curl -X POST https://sage.home/api/v1/devices/garage-door/open
```

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

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 16
- Nginx (reverse proxy - future)

## Quick Start

### Requirements
- **Raspberry Pi 4 (4GB+)** or **Raspberry Pi 5** (8GB recommended)
- **64GB+ microSD card** or USB SSD
- **Docker & Docker Compose** installed
- **Microphone** for voice input (USB or Raspberry Pi audio HAT)
- **Speaker** for voice output
- *(Optional)* Smart home devices for integration

### Deploy with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/sage.git
cd sage

# Configure environment
cp .env.example .env
# Edit .env to customize settings

# Start all services
docker compose up -d

# Pull AI model (choose based on your RAM)
docker exec -it sage-ollama ollama pull tinyllama    # 4GB RAM
# OR
docker exec -it sage-ollama ollama pull phi          # 8GB RAM

# Check service status
docker compose ps

# View logs
docker compose logs -f sage
```

Access the API at `http://localhost:8000`
View documentation at `http://localhost:8000/docs`

## Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete Raspberry Pi setup instructions
- **[Development Guide](CLAUDE.md)** - Architecture, implementation notes, and AI assistant guidance
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      SAGE Core API                       │
│                   (FastAPI - Port 8000)                  │
│                                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  │
│  │  Voice  │  │  Lists  │  │  Smart  │  │Knowledge │  │
│  │Commands │  │   API   │  │  Home   │  │   Base   │  │
│  └─────────┘  └─────────┘  └─────────┘  └──────────┘  │
└───────┬───────────┬──────────┬──────────────┬──────────┘
        │           │          │              │
   ┌────▼────┐  ┌──▼───┐  ┌───▼────┐  ┌──────▼─────┐
   │ Whisper │  │ PG   │  │ Ollama │  │  ChromaDB  │
   │  (STT)  │  │ SQL  │  │  LLM   │  │  (Vectors) │
   └────┬────┘  └──────┘  └────────┘  └────────────┘
        │
   ┌────▼────┐
   │  Piper  │
   │  (TTS)  │
   └─────────┘

External Integrations:
├── Smart Home Devices (Future)
├── Cameras (Future)
└── Sensors (Future)
```

### Data Flow

1. **Voice Input** → Whisper (STT) → Text
2. **Text** → Ollama (LLM) + ChromaDB (Context) → Response
3. **Response** → Piper (TTS) → Voice Output
4. **All interactions** → PostgreSQL (History, Lists, Metadata)

## Resource Usage

Optimized for Raspberry Pi with configurable limits:
- **SAGE App**: 2GB RAM max, 3 CPU cores
- **Ollama**: 3GB RAM max, 2.5 CPU cores
- **PostgreSQL**: 512MB RAM max, 1 CPU core
- **ChromaDB**: 1GB RAM max, 1 CPU core

## Development

### Quick Setup
```bash
make quickstart        # Install everything and start services
make dev               # Run development server
make test              # Run tests
```

See [CLAUDE.md](CLAUDE.md) for detailed development guide.

## Roadmap

### Phase 1: Core Functionality (Current)
- [x] Docker infrastructure optimized for Raspberry Pi
- [x] FastAPI application scaffold
- [x] Development environment (DevContainer, VS Code)
- [x] CI/CD pipelines
- [ ] Ollama LLM integration
- [ ] Whisper STT integration
- [ ] Piper TTS integration
- [ ] Basic conversation handling

### Phase 2: Knowledge & Lists
- [ ] Personal knowledge base with ChromaDB
- [ ] RAG (Retrieval-Augmented Generation) implementation
- [ ] List management (CRUD operations)
- [ ] Voice-controlled list updates
- [ ] Knowledge persistence and retrieval

### Phase 3: Smart Home
- [ ] Device registry and management
- [ ] Smart home device integrations (lights, thermostats, locks)
- [ ] Voice commands for device control
- [ ] Automation rules and schedules
- [ ] Remote device control via API

### Phase 4: Extensions
- [ ] Camera integration and image analysis
- [ ] Sensor data collection (temperature, humidity, motion)
- [ ] Multi-room audio support
- [ ] Mobile app/PWA
- [ ] Wake word detection
- [ ] Continuous conversation mode

### Phase 5: Advanced Features
- [ ] Multi-user support with voice recognition
- [ ] Proactive notifications and reminders
- [ ] Integration with calendar and email
- [ ] Custom skills/plugins system
- [ ] Offline-first mobile app sync

## Privacy & Security

- **100% Local** - All processing happens on your device
- **No Cloud Dependencies** - Works completely offline
- **Your Data Stays Yours** - No telemetry, no tracking
- **Secure by Default** - API authentication built-in
- **Open Source** - Audit the code yourself

## Contributing

This is a personal project, but suggestions and improvements are welcome! Please see [CLAUDE.md](CLAUDE.md) for architecture and development guidelines.

## License

See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for privacy, running on a Raspberry Pi**
