.PHONY: help install test lint format clean run

help:  ## Show this help message
	@echo "OpenResilience Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package and dependencies
	pip install -e .
	pip install -e ".[dev]"

test:  ## Run test suite
	pytest tests/ -v --tb=short

test-cov:  ## Run tests with coverage report
	pytest tests/ --cov=src/openresilience --cov-report=term-missing

lint:  ## Run linter on src/, tests/, and app.py
	ruff check src/ tests/ app.py

format:  ## Auto-format code
	ruff format src/ tests/ app.py

clean:  ## Remove cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:  ## Start Streamlit app
	streamlit run app.py

docker-up:  ## Start full microservice stack
	docker compose up --build

docker-down:  ## Stop microservice stack
	docker compose down
