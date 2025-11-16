# RAG Telegram Bot

Telegram bot with RAG for answering questions based on uploaded documents using **Ollama** for local LLM inference.

## Architecture

- **FastAPI** - Web framework
- **LangChain** - RAG framework
- **FAISS** - Vector database
- **Ollama** - Local LLM inference
- **Docker** - Containerization

## Quick Start

### 1. Environment Setup

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TEMPERATURE=0.0
```

### 2. Prepare Documents

Add your documents (.txt or .pdf) to the `data/` folder:

```bash
mkdir -p data
# Copy your documents to data/
```

### 3. Create FAISS Index

```bash
python app/ingest.py
```

### 4. Run with Docker

```bash
docker-compose up --build
```

This will start:
- **Ollama** service on port 11434
- **Telegram bot** service on port 8000

### 5. Pull Ollama Model

After starting the services, pull the model:

```bash
docker exec -it ollama ollama pull llama3.2
```

Or use any other model:
```bash
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull llama2
docker exec -it ollama ollama pull codellama
```

### 6. Local Run (without Docker)

First, install and start Ollama locally:

```bash
# Install Ollama (macOS)
brew install ollama

# Or download from https://ollama.ai

# Start Ollama service
ollama serve

# Pull a model
ollama pull llama3.2
```

Then run the bot:

```bash
pip install -r requirements.txt
python app/ingest.py

# Update .env with local Ollama URL
# OLLAMA_BASE_URL=http://localhost:11434

cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Webhook Setup

If deploying on a server with a public domain:

1. Set `BASE_URL` in `.env`:
   ```
   BASE_URL=https://your-domain.com
   ```

2. Webhook will be automatically configured when the application starts

For local development, use **ngrok**:

```bash
ngrok http 8000
# Copy URL
# Set it in .env
BASE_URL=https://abc123.ngrok.io
```

## Using the Bot

1. Find your bot in Telegram
2. Send `/start` to begin
3. Ask questions - the bot will answer based on loaded documents

## API Endpoints

- `GET /` - Service status check
- `GET /health` - Health check
- `POST /telegram/webhook` - Webhook for Telegram

## Available Ollama Models

Popular models you can use:
- `llama3.2` - Latest Llama model (recommended)
- `llama3.1` - Previous Llama version
- `mistral` - Mistral AI model
- `codellama` - Code-specialized model
- `phi3` - Microsoft's small model
- `gemma2` - Google's model

To change the model, update `OLLAMA_MODEL` in `.env` and pull the model:
```bash
docker exec -it ollama ollama pull <model-name>
```

## Configuration

Environment variables:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)
- `OLLAMA_BASE_URL` - Ollama API URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model name (default: llama3.2)
- `OLLAMA_TEMPERATURE` - Temperature for generation (default: 0.0)
- `EMBEDDING_MODEL` - HuggingFace embedding model (default: sentence-transformers/all-MiniLM-L6-v2)
- `BASE_URL` - Public URL for webhook
- `FAISS_INDEX_DIR` - FAISS index directory (default: faiss_index)
- `DOCS_PATH` - Documents directory (default: data)