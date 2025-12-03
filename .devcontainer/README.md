# SAGE Development Container

This directory contains the VS Code DevContainer configuration for developing SAGE.

## Features

- **Python 3.11** development environment
- **All dependencies** pre-installed
- **Connected services**: PostgreSQL, Ollama, ChromaDB
- **VS Code extensions**: Python, Docker, SQLTools, and more
- **Debugger support**: Remote debugging with debugpy

## Quick Start

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Opening in DevContainer

1. Open this project in VS Code
2. Press `F1` or `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows/Linux)
3. Select **"Dev Containers: Reopen in Container"**
4. Wait for the container to build (first time takes ~5-15 minutes)

VS Code will reload and you'll be inside the container!

## Available Commands

### Launch Configurations (F5 / Run & Debug)
- **FastAPI: Debug** - Run FastAPI with hot reload
- **FastAPI: Debug (No Reload)** - Run without reload for breakpoint debugging
- **Python: Current File** - Debug the currently open Python file
- **Pytest: Current File** - Debug tests in current file
- **Pytest: All Tests** - Debug all tests
- **Docker: Attach to FastAPI** - Attach to running FastAPI container

### Tasks (Terminal → Run Task)
- **Run FastAPI Dev Server** - Start development server
- **Run Tests** - Execute pytest
- **Run Tests with Coverage** - Tests with coverage report
- **Format & Lint All** - Format code with Black and isort, then lint
- **Docker: Build/Up/Down** - Manage Docker services
- **Ollama: Pull Models** - Download AI models
- **DB: Run Migrations** - Apply Alembic migrations

## Development Workflow

### 1. Start Services
```bash
# Services auto-start with devcontainer
# Or manually:
docker compose up -d
```

### 2. Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### 3. Run the Application
- **Method 1**: Press `F5` and select "FastAPI: Debug"
- **Method 2**: Run task "Run FastAPI Dev Server"
- **Method 3**: Terminal: `uvicorn sage.main:app --reload`

### 4. Access Services
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (use SQLTools extension)
- **Ollama**: http://localhost:11434
- **ChromaDB**: http://localhost:8001

### 5. Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=sage

# Specific file
pytest tests/test_api.py

# Or use F5 → "Pytest: All Tests"
```

## Debugging

### Breakpoint Debugging
1. Set breakpoints in your code (click left of line number)
2. Press `F5` → Select "FastAPI: Debug"
3. Make requests to your API
4. Debugger will pause at breakpoints

### Remote Debugging
If FastAPI is running in Docker:
1. Start container with debugpy: `python -m debugpy --listen 0.0.0.0:5678 ...`
2. Press `F5` → Select "Docker: Attach to FastAPI"
3. Set breakpoints and debug

## Database Management

### Using SQLTools Extension
1. Open SQLTools panel (database icon in activity bar)
2. Connect to "SAGE Database"
3. Browse tables, run queries

### Running Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Or use task: "DB: Run Migrations"
```

## Troubleshooting

### Container Won't Start
```bash
# Rebuild container
Dev Containers: Rebuild Container

# Or from terminal
docker compose down -v
docker compose build --no-cache
```

### Services Not Available
```bash
# Check service status
docker compose ps

# View logs
docker compose logs sage
docker compose logs postgres
```

### Python Packages Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Port Already in Use
Edit `.devcontainer/docker-compose.dev.yml` and change port mappings.

## Tips

- **IntelliSense**: Works automatically with installed packages
- **Auto-formatting**: Saves automatically format with Black
- **Import sorting**: Auto-sorts imports with isort on save
- **Type checking**: Pylance provides type hints and checking
- **SQL queries**: Use SQLTools to query database directly from VS Code

## Customization

### Add VS Code Extensions
Edit `.devcontainer/devcontainer.json`:
```json
"customizations": {
  "vscode": {
    "extensions": [
      "your-extension-id"
    ]
  }
}
```

### Change Python Version
Edit `Dockerfile` and rebuild container.

### Add System Dependencies
Edit `Dockerfile`, add to `apt-get install` section, rebuild.
