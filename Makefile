.PHONY: help install install-dev dev test test-cov lint format clean docker-build docker-up docker-down docker-logs ollama-tiny ollama-phi db-migrate db-upgrade

# Default target
.DEFAULT_GOAL := help

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)SAGE Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# Installation
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

# Development
dev: ## Run development server with hot reload
	uvicorn sage.main:app --reload --host 0.0.0.0 --port 8000

dev-debug: ## Run development server with debugger
	python -m debugpy --listen 0.0.0.0:5678 -m uvicorn sage.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=sage --cov-report=term-missing --cov-report=html

test-unit: ## Run only unit tests
	pytest tests/ -v -m unit

test-integration: ## Run only integration tests
	pytest tests/ -v -m integration

test-watch: ## Run tests in watch mode
	pytest-watch tests/

# Code Quality
lint: ## Run linting checks
	@echo "$(BLUE)Running flake8...$(NC)"
	flake8 sage/ tests/
	@echo "$(BLUE)Running mypy...$(NC)"
	mypy sage/

format: ## Format code with black and isort
	@echo "$(BLUE)Running isort...$(NC)"
	isort sage/ tests/
	@echo "$(BLUE)Running black...$(NC)"
	black sage/ tests/

format-check: ## Check code formatting without making changes
	@echo "$(BLUE)Checking isort...$(NC)"
	isort --check-only sage/ tests/
	@echo "$(BLUE)Checking black...$(NC)"
	black --check sage/ tests/

check: format-check lint test ## Run all checks (format, lint, test)

# Docker
docker-build: ## Build Docker images
	docker compose build

docker-up: ## Start all Docker services
	docker compose up -d

docker-down: ## Stop all Docker services
	docker compose down

docker-restart: ## Restart all Docker services
	docker compose restart

docker-logs: ## Follow logs for all services
	docker compose logs -f

docker-logs-sage: ## Follow logs for SAGE service only
	docker compose logs -f sage

docker-ps: ## Show running containers
	docker compose ps

docker-clean: ## Remove all containers, volumes, and images
	docker compose down -v
	docker system prune -f

# Ollama
ollama-tiny: ## Pull TinyLlama model
	docker exec -it sage-ollama ollama pull tinyllama

ollama-phi: ## Pull Phi model
	docker exec -it sage-ollama ollama pull phi

ollama-mistral: ## Pull Mistral model (requires 8GB RAM)
	docker exec -it sage-ollama ollama pull mistral

ollama-list: ## List downloaded models
	docker exec -it sage-ollama ollama list

ollama-shell: ## Open shell in Ollama container
	docker exec -it sage-ollama /bin/bash

# Database
db-migrate: ## Create a new database migration
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

db-upgrade: ## Apply database migrations
	alembic upgrade head

db-downgrade: ## Rollback last database migration
	alembic downgrade -1

db-shell: ## Open PostgreSQL shell
	docker exec -it sage-postgres psql -U sage -d sage

# Cleanup
clean: ## Clean up cache files and build artifacts
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	rm -rf build dist htmlcov .coverage

clean-all: clean docker-clean ## Clean everything including Docker

# Environment
env: ## Create .env from .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)Created .env file from .env.example$(NC)"; \
		echo "$(YELLOW)Please update .env with your configuration$(NC)"; \
	else \
		echo "$(YELLOW).env file already exists$(NC)"; \
	fi

# Pre-commit
pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

# Quick start
quickstart: env install-dev docker-up ollama-tiny ## Quick start: setup environment and start services
	@echo ""
	@echo "$(GREEN)✓ Environment setup complete!$(NC)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Update .env with your configuration"
	@echo "  2. Run 'make dev' to start the development server"
	@echo "  3. Visit http://localhost:8000/docs for API documentation"
	@echo ""

# Status check
status: ## Check status of all services
	@echo "$(BLUE)Docker Services:$(NC)"
	@docker compose ps
	@echo ""
	@echo "$(BLUE)Ollama Models:$(NC)"
	@docker exec sage-ollama ollama list 2>/dev/null || echo "Ollama not running"
	@echo ""
	@echo "$(BLUE)Database Status:$(NC)"
	@docker exec sage-postgres pg_isready -U sage 2>/dev/null || echo "PostgreSQL not running"
