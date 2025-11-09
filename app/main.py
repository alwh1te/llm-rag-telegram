import logging
import os
from contextlib import asynccontextmanager

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import answer_question, answer_question_direct

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
BASE_URL = os.getenv("BASE_URL")
PORT = int(os.getenv("PORT", "8000"))

if not TELEGRAM_BOT_TOKEN:
    raise Exception("Set TELEGRAM_BOT_TOKEN in .env")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    if BASE_URL:
        url = BASE_URL.rstrip("/") + WEBHOOK_PATH
        try:
            resp = requests.post(f"{TELEGRAM_API}/setWebhook", json={"url": url})
            logger.info(f"setWebhook response: {resp.text}")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
    else:
        logger.warning("BASE_URL not set - webhook not configured")
    
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(
    title="RAG Telegram Bot API",
    description="Telegram bot with RAG capabilities using LangChain and FAISS",
    version="1.0.0",
    lifespan=lifespan
)


class TelegramUpdate(BaseModel):
    update_id: int
    message: dict = None


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "RAG Telegram Bot",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post(WEBHOOK_PATH)
async def telegram_webhook(update: dict):
    logger.info(f"Received update: {update.get('update_id')}")
    
    if "message" not in update:
        return {"ok": True}
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    user_text = message.get("text", "")
    
    if not user_text:
        send_message(chat_id, "Я понимаю только текстовые сообщения.")
        return {"ok": True}

    if user_text.startswith("/start"):
        welcome_msg = (
            "Привет! Я RAG-бот.\n\n"
            "Я отвечаю на вопросы на основе загруженных документов.\n"
            "Просто задайте мне вопрос, и я постараюсь найти ответ!"
        )
        send_message(chat_id, welcome_msg)
        return {"ok": True}
    
    if user_text.startswith("/help"):
        help_msg = (
            "Как использовать бота:\n\n"
            "1. Задайте любой вопрос\n"
            "2. Я найду релевантные фрагменты в документах\n"
            "3. Сформирую ответ на основе найденной информации\n\n"
            "Команды:\n"
            "/start - начать работу\n"
            "/help - показать эту справку"
        )
        send_message(chat_id, help_msg)
        return {"ok": True}

    try:
        logger.info(f"Processing question from chat {chat_id}: {user_text}")
        send_message(chat_id, "Ищу ответ...")
        
        try:
            result = answer_question(user_text, k=3)
            answer = result["answer"]
            logger.info(f"Answer generated using RAG")
        except FileNotFoundError:
            logger.info(f"FAISS index not found, using direct LLM response")
            result = answer_question_direct(user_text)
            answer = result["answer"]
        
        if not answer.strip():
            answer = "Не удалось сформировать ответ."
        
        send_message(chat_id, answer)
        logger.info(f"Response sent to chat {chat_id}")
        
    except Exception as e:
        error_msg = f"Ошибка при обработке запроса: {str(e)}"
        send_message(chat_id, error_msg)
        logger.error(f"Error processing question: {e}", exc_info=True)
    
    return {"ok": True}


def send_message(chat_id: int, text: str):
    try:
        resp = requests.post(
            f"{TELEGRAM_API}/sendMessage", 
            json={"chat_id": chat_id, "text": text}
        )
        if resp.status_code != 200:
            logger.error(f"Telegram sendMessage failed: {resp.text}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
