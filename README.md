# RAG Telegram Bot

Telegram bot with RAG for answering questions based on uploaded documents.

## Architecture

- **FastAPI**
- **LangChain**
- **FAISS**
- **OpenAI GPT**
- **Docker**

## Quick Start

### 1. Environment Setup

```env
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
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

### 5. Local Run (without Docker)

```bash
pip install -r requirements.txt
python app/ingest.py
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
