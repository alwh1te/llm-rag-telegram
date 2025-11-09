.PHONY: help install ingest run docker-build docker-up docker-down logs clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make ingest       - Create FAISS index from documents"
	@echo "  make run          - Run application locally"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Run in Docker"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make logs         - Show Docker logs"
	@echo "  make clean        - Remove temporary files"

install:
	pip install -r requirements.txt

ingest:
	python app/ingest.py

run:
	cd app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
