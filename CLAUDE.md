# SAGE Development Guide for AI Assistants

This document provides comprehensive guidance for AI assistants (Claude or others) working on the SAGE project. It covers architecture decisions, implementation patterns, development workflow, and future considerations.

## Project Overview

**SAGE (Smart Autonomous General-purpose Engine)** is a privacy-first virtual assistant designed to run entirely on a Raspberry Pi. Unlike cloud-based assistants, SAGE keeps all user data local, providing complete privacy and control.

### Core Mission

Build a personal AI assistant that:
1. **Learns about the user's life** - Projects, preferences, daily routines
2. **Manages practical tasks** - Shopping lists, travel planning, reminders
3. **Controls smart home devices** - Lights, thermostats, locks, etc.
4. **Provides voice interaction** - Natural conversation via STT/TTS
5. **Offers remote access** - Secure API for mobile/web access
6. **Supports extensibility** - Cameras, sensors, custom integrations

### Key Constraints

- **Raspberry Pi deployment** - Resource-limited (4-8GB RAM, ARM64 CPU)
- **100% local processing** - No cloud dependencies
- **Privacy-first** - User data never leaves the device
- **Offline-capable** - Core features work without internet

## Architecture

### System Design Principles

1. **Modular Architecture** - Each component (LLM, STT, TTS, DB) is isolated
2. **Service-Oriented** - Core services can be used independently
3. **API-First** - All functionality accessible via REST API
4. **Database-Backed** - Structured data in PostgreSQL, vectors in ChromaDB
5. **Resource-Aware** - Optimized for Raspberry Pi constraints

### Technology Choices & Rationale

#### FastAPI (Web Framework)
- **Why**: High performance, automatic OpenAPI docs, async support
- **Alternatives considered**: Flask (too simple), Django (too heavy)
- **Trade-off**: Slightly steeper learning curve for better async performance

#### Ollama (LLM Runtime)
- **Why**: Easy model management, good ARM64 support, no GPU required
- **Alternatives considered**: llama.cpp (more complex), transformers (too slow)
- **Trade-off**: Limited model formats (GGUF only), but excellent for edge deployment

#### Faster-Whisper (STT)
- **Why**: Fast CPU inference, good accuracy, quantized models available
- **Alternatives considered**: OpenAI Whisper (too slow), Vosk (less accurate)
- **Trade-off**: First inference is slow (~5s), but subsequent ones are fast

#### Coqui TTS (Text-to-Speech)
- **Why**: Good ARM support, multiple voice options, offline
- **Alternatives considered**: Piper (limited voices), Festival (robotic)
- **Trade-off**: Larger model sizes, but better voice quality

#### ChromaDB (Vector Database)
- **Why**: Easy to use, good for RAG, embedded mode available
- **Alternatives considered**: Pinecone (cloud-only), Weaviate (too heavy)
- **Trade-off**: Less mature than alternatives, but perfect for edge use

#### PostgreSQL (Relational Database)
- **Why**: Reliable, well-tested, good ARM support, pgvector available
- **Alternatives considered**: SQLite (concurrency issues), MySQL (heavier)
- **Trade-off**: Higher resource usage, but better data integrity

### Component Responsibilities

#### `sage/api/` - API Layer
- **Purpose**: HTTP endpoints, request/response handling, validation
- **Pattern**: One router per domain (health, llm, stt, tts, lists, devices)
- **Guidelines**:
  - Keep routes thin - delegate logic to `core/` services
  - Use Pydantic models for all I/O
  - Handle auth/validation here
  - Return standardized response formats

#### `sage/core/` - Business Logic
- **Purpose**: Service implementations, AI integrations, business rules
- **Pattern**: Service classes with dependency injection
- **Guidelines**:
  - Each service should be independently testable
  - Use async/await for I/O operations
  - Handle retries and error recovery
  - Log important operations

#### `sage/db/` - Data Layer
- **Purpose**: Database models, sessions, queries
- **Pattern**: SQLAlchemy ORM with declarative models
- **Guidelines**:
  - One model per table
  - Use relationships for foreign keys
  - Keep queries in model methods or separate query classes
  - Use migrations (Alembic) for schema changes

#### `sage/utils/` - Utilities
- **Purpose**: Logging, configuration, helpers
- **Pattern**: Standalone functions or singleton classes
- **Guidelines**:
  - Keep utilities generic and reusable
  - No business logic here
  - Document all utility functions

### Data Storage Strategy

```
PostgreSQL (Structured Data):
├── conversations (chat history)
├── knowledge_entries (user facts)
├── lists (shopping, travel, etc.)
├── list_items (items within lists)
├── devices (smart home registry)
├── device_states (current state of devices)
└── user_preferences (settings)

ChromaDB (Vector Data):
├── knowledge_embeddings (for semantic search)
├── conversation_context (recent chat context)
└── document_embeddings (uploaded documents)
```

## Development Workflow

### Getting Started

```bash
# 1. Clone and setup
git clone <repo>
cd sage
make install-dev

# 2. Start services
make docker-up

# 3. Pull AI model
make ollama-tiny

# 4. Run development server
make dev

# 5. In another terminal, run tests
make test-watch
```

### Before Committing

Pre-commit hooks will automatically run, but you can manually check:

```bash
make check  # Runs format-check, lint, tests
```

If checks fail:
```bash
make format  # Auto-fix formatting
make lint    # See linting issues
make test    # Run tests
```

### Creating a Pull Request

1. **Create feature branch**: `git checkout -b feature/your-feature`
2. **Make changes** with tests
3. **Run checks**: `make check`
4. **Commit**: Pre-commit hooks run automatically
5. **Push**: `git push origin feature/your-feature`
6. **Create PR**: GitHub Actions will run:
   - CI/CD pipeline (tests, lint, build)
   - Quality check (coverage, security)
   - Claude AI review (code review)

## Implementation Patterns

### Adding a New API Endpoint

```python
# 1. Create Pydantic models in sage/api/routes/<domain>.py
class CreateListRequest(BaseModel):
    name: str
    items: list[str] = []

class ListResponse(BaseModel):
    id: int
    name: str
    items: list[str]
    created_at: datetime

# 2. Create route handler
@router.post("/lists", response_model=ListResponse)
async def create_list(
    request: CreateListRequest,
    list_service: ListService = Depends(get_list_service)
):
    """Create a new list."""
    list_obj = await list_service.create_list(request.name, request.items)
    return ListResponse.from_orm(list_obj)

# 3. Implement service in sage/core/
class ListService:
    def __init__(self, db: Session):
        self.db = db

    async def create_list(self, name: str, items: list[str]) -> List:
        # Business logic here
        pass
```

### Adding a Database Model

```python
# 1. Create model in sage/db/models.py
class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("ListItem", back_populates="list")

# 2. Create migration
make db-migrate -m "Add lists table"

# 3. Apply migration
make db-upgrade
```

### Adding Vector Search (RAG)

```python
# 1. Store knowledge with embedding
embedding_service = EmbeddingService()
vector = await embedding_service.embed(text)

chroma_client.add(
    documents=[text],
    embeddings=[vector],
    metadatas=[{"source": "user", "created_at": str(datetime.utcnow())}],
    ids=[str(uuid4())]
)

# 2. Retrieve relevant context
query_vector = await embedding_service.embed(query)
results = chroma_client.query(
    query_embeddings=[query_vector],
    n_results=5
)

# 3. Use context in LLM prompt
context = "\n".join(results["documents"][0])
prompt = f"Context:\n{context}\n\nQuestion: {query}"
response = await llm_service.generate(prompt)
```

## Implementation Priorities

### Phase 1: Core Functionality (Current)

**Goal**: Get basic conversation working

1. **LLM Integration** (`sage/core/llm.py`)
   - Connect to Ollama API
   - Handle streaming responses
   - Implement error handling and retries
   - Add conversation context management

2. **STT Integration** (`sage/core/stt.py`)
   - Load Faster-Whisper model
   - Process audio files
   - Handle different audio formats
   - Optimize for Raspberry Pi (quantized models)

3. **TTS Integration** (`sage/core/tts.py`)
   - Load Coqui TTS model
   - Generate speech from text
   - Cache generated audio
   - Support multiple voices

4. **Conversation API** (`sage/api/routes/conversation.py`)
   - Text chat endpoint
   - Voice chat endpoint (audio in → text → response → audio out)
   - Conversation history storage
   - Context window management

### Phase 2: Knowledge & Lists

**Goal**: Make SAGE useful for daily tasks

1. **Knowledge Base** (`sage/core/knowledge.py`)
   - Store facts about user's life
   - Semantic search with ChromaDB
   - RAG implementation for context-aware responses
   - CRUD API for knowledge entries

2. **List Management** (`sage/core/lists.py`)
   - CRUD operations for lists
   - Voice commands for list updates
   - List sharing/export
   - Recurring list templates

3. **Voice Commands** (`sage/core/intent.py`)
   - Intent recognition (add to list, search knowledge, etc.)
   - Entity extraction (item names, quantities, etc.)
   - Multi-turn conversations
   - Confirmation flows

### Phase 3: Smart Home

**Goal**: Control physical devices

1. **Device Registry** (`sage/core/devices.py`)
   - Device discovery and registration
   - Device capabilities and states
   - Device groups and scenes

2. **Integrations** (`sage/integrations/`)
   - Home Assistant integration
   - MQTT support for DIY devices
   - Zigbee/Z-Wave bridges
   - Vendor-specific APIs (Philips Hue, Nest, etc.)

3. **Voice Control** (`sage/core/device_control.py`)
   - Natural language device commands
   - Scene activation
   - Automation triggers

### Phase 4: Extensions

**Goal**: Add advanced capabilities

1. **Camera Integration**
   - Motion detection
   - Face recognition
   - Object detection
   - Video doorbell integration

2. **Sensors**
   - Temperature, humidity, motion
   - Data logging and trends
   - Anomaly detection
   - Alerts and notifications

3. **Mobile App**
   - Progressive Web App (PWA)
   - Offline-first with sync
   - Push notifications
   - Remote access via VPN/Tailscale

## Raspberry Pi Considerations

### Resource Management

**Memory**:
- Ollama can use 2-3GB for smaller models (tinyllama, phi)
- Whisper (tiny) uses ~500MB
- TTS uses ~300MB
- Leave 1-2GB for OS and other processes

**CPU**:
- LLM inference is CPU-bound (2-10 tokens/sec)
- Whisper can process audio at ~0.5-2x realtime
- TTS generation is relatively fast (< 1s for short phrases)

**Storage**:
- Models: 1-5GB (depends on model size)
- Database: grows with usage (estimate 100MB/year for typical use)
- Audio cache: limit to 1GB, LRU eviction

### Performance Optimization

1. **Model Selection**:
   - Use quantized models (Q4, Q5) for Ollama
   - Use "tiny" or "base" Whisper models
   - Cache TTS audio for common phrases

2. **Inference Optimization**:
   - Keep models loaded in memory (don't reload)
   - Use batch processing where possible
   - Implement request queuing to prevent overload

3. **Caching Strategy**:
   - Cache LLM responses for common queries
   - Cache embeddings for frequent searches
   - Cache TTS audio for repetitive phrases

4. **Background Processing**:
   - Use async tasks for non-critical operations
   - Queue heavy operations (video processing, etc.)
   - Implement graceful degradation when overloaded

## Testing Strategy

### Test Categories

```python
@pytest.mark.unit        # Fast, isolated, no external dependencies
@pytest.mark.integration # Tests with database, services
@pytest.mark.slow        # Long-running tests (optional in CI)
```

### What to Test

1. **API Endpoints** (`tests/api/`)
   - Request validation
   - Response formats
   - Error handling
   - Authentication

2. **Services** (`tests/core/`)
   - Business logic
   - Service interactions
   - Error recovery
   - Edge cases

3. **Database** (`tests/db/`)
   - Model relationships
   - Queries
   - Transactions
   - Migrations

4. **Integration** (`tests/integration/`)
   - End-to-end workflows
   - Service communication
   - Real AI model inference (optional)

### Test Data

- Use fixtures in `tests/conftest.py`
- Mock external services (Ollama, etc.) for unit tests
- Use test database for integration tests
- Never test against production data

## Security Considerations

### Authentication & Authorization

**Current**: None (device is on local network)

**Future**:
- JWT tokens for API access
- User accounts with roles
- API keys for remote access
- Rate limiting

### Data Privacy

- All data stored locally (never sent to cloud)
- Encryption at rest (optional, via LUKS)
- Secure API access (HTTPS via reverse proxy)
- No telemetry or analytics

### Network Security

- Firewall rules (only expose necessary ports)
- VPN/Tailscale for remote access
- HTTPS only for external access
- Regular security updates

## Common Tasks

### Adding a New LLM Model

```bash
# Pull model
docker exec -it sage-ollama ollama pull <model-name>

# Update .env
OLLAMA_MODEL=<model-name>

# Restart SAGE
docker compose restart sage
```

### Debugging Performance Issues

```bash
# Check resource usage
docker stats

# Check Ollama logs
docker logs sage-ollama

# Profile Python code
python -m cProfile -o profile.prof sage/main.py
```

### Updating Dependencies

```bash
# Update requirements.txt
pip-compile requirements.in

# Rebuild Docker images
make docker-build

# Test
make test
```

## Troubleshooting

### Ollama not responding
- Check if model is loaded: `docker exec sage-ollama ollama list`
- Check logs: `docker logs sage-ollama`
- Restart: `docker compose restart ollama`

### Out of memory
- Use smaller model (tinyllama instead of llama2)
- Reduce concurrent requests
- Lower OLLAMA_MAX_LOADED_MODELS to 1

### Slow inference
- Check CPU temperature (throttling?)
- Verify model quantization (Q4 recommended)
- Reduce context window size

### Database migrations fail
- Check PostgreSQL logs: `docker logs sage-postgres`
- Manually rollback: `make db-downgrade`
- Fix migration file and retry

## API Response Patterns

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  }
}
```

### Pagination
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "pages": 5
  }
}
```

## Environment Variables

Key configurations in `.env`:

```bash
# Application
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://sage:sage@postgres:5432/sage

# AI Services
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=tinyllama
WHISPER_MODEL=tiny
WHISPER_DEVICE=cpu

# Performance
MAX_WORKERS=2
OMP_NUM_THREADS=4
```

## Future Considerations

### Scalability

- Multi-device deployment (SAGE instances per room)
- Distributed knowledge base (sync across instances)
- Federation (share devices across instances)

### Advanced Features

- Wake word detection (Porcupine, Snowboy)
- Speaker identification (voice profiles)
- Emotion detection (from voice)
- Proactive suggestions
- Learning from corrections

### Integration Ideas

- Calendar integration (Google Calendar, CalDAV)
- Email integration (IMAP/SMTP)
- Music streaming (Spotify, local library)
- Weather data
- News feeds
- Recipe databases

## Contributing Guidelines

When implementing new features:

1. **Discuss first** - Open an issue to discuss approach
2. **Write tests** - Aim for >80% coverage
3. **Document** - Update this file and inline docs
4. **Keep it simple** - Avoid over-engineering
5. **Consider constraints** - Remember Raspberry Pi limitations
6. **Privacy first** - No cloud dependencies without explicit user consent

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- [ChromaDB Guide](https://docs.trychroma.com/)

### Raspberry Pi
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed Pi setup
- [Raspberry Pi Forums](https://forums.raspberrypi.com/)

### AI/ML
- [Hugging Face Models](https://huggingface.co/models)
- [Ollama Model Library](https://ollama.ai/library)

---

**Remember**: SAGE is about empowering users with privacy and control. Every decision should prioritize user autonomy and data ownership.
