.PHONY: help install ingest run docker-build docker-up docker-down logs clean test-model test-rag ollama-pull ollama-list ollama-logs

help:
	@echo "Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make ingest       - Create FAISS index from documents"
	@echo ""
	@echo "Run:"
	@echo "  make run          - Run application locally"
	@echo "  make docker-up    - Start all services with Docker"
	@echo "  make docker-down  - Stop Docker containers"
	@echo ""
	@echo "Ollama:"
	@echo "  make ollama-pull  - Pull Ollama model (default: llama3.2)"
	@echo "  make ollama-list  - List installed Ollama models"
	@echo "  make ollama-logs  - Show Ollama logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test-model   - Test Ollama model"
	@echo "  make test-rag     - Test RAG system"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make logs         - Show all Docker logs"
	@echo "  make clean        - Remove temporary files"

install:
	pip install -r requirements.txt

ingest:
	python app/ingest.py

run:
	cd app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker compose build

docker-up:
	docker compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "Pulling Ollama model... (this may take a while)"
	@sleep 5
	@make ollama-pull || true
	@echo ""
	@echo "Bot is ready! Check status with: make logs"

docker-down:
	docker compose down

logs:
	docker compose logs -f

ollama-pull:
	docker exec ollama ollama pull $${OLLAMA_MODEL:-deepseek-r1:1.5b}

ollama-list:
	docker exec ollama ollama list

ollama-logs:
	docker logs ollama -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
