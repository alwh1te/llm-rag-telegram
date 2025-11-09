#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== RAG Telegram Bot Setup ===${NC}\n"

if [ ! -d "data" ]; then
    echo -e "${YELLOW}Creating data folder...${NC}"
    mkdir -p data
fi

if [ -z "$(ls -A data)" ]; then
    echo -e "${YELLOW}data folder is empty. Documents already created.${NC}"
else
    echo -e "${GREEN}✓ Found documents in data folder${NC}"
fi

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${GREEN}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -d "faiss_index" ]; then
    echo -e "${GREEN}Creating FAISS index...${NC}"
    python app/ingest.py
else
    echo -e "${YELLOW}FAISS index already exists. Recreate? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf faiss_index
        python app/ingest.py
    fi
fi

echo -e "\n${GREEN}=== Setup complete! ===${NC}\n"
echo "To start the bot choose an option:"
echo ""
echo "1. Local run:"
echo "   make run"
echo "   or"
echo "   cd app && uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "2. Docker run:"
echo "   make docker-up"
echo "   or"
echo "   docker-compose up --build"
echo ""
echo -e "${YELLOW}Note: For webhook to work, set BASE_URL in .env${NC}"
