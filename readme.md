# SupportEng AI

SupportEng AI is an intelligent Technical Support Assistant that leverages Retrieval-Augmented Generation (RAG) and LLMs to analyze historical tickets and provide structured, automated resolutions to user queries. It integrates seamlessly with both Google Chat (via FastAPI webhooks) and Telegram.

## Features

- **FastAPI Backend**: Provides an API and webhook endpoints to integrate directly with Google Chat.
- **Telegram Bot Integration**: A dedicated Telegram bot (`@support`) for on-the-go query resolution.
- **RAG System**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to create text embeddings and find similar historical tickets.
- **Automated Solutions**: Integrates with OpenRouter (using models like `gpt-4o`) to generate structured Root Cause Analysis (RCA) and resolution steps.
- **Screenshot Hashing**: Image comparison features for identifying similar screenshot attachments in tickets.
- **MongoDB Storage**: Stores embedded incidents, ticket histories, and image hashes for quick vector-like retrieval.

## Prerequisites

- Python 3.8+
- MongoDB (running locally or a cloud cluster)

## Setup Instructions

### 1. Python Environment Setup
Create and activate a Python virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
*Make sure to select this virtual environment as your Python interpreter in your IDE.*

### 2. Install Dependencies
Install the required Python libraries. *(Ensure you have your `requirements.txt` ready or install FastAPI, Uvicorn, Telebot, SentenceTransformers, OpenRouter, Pydantic, etc. manually if they present any squiggles).*

### 3. Environment Variables
Create a `.env` file in the root directory and configure the following required variables:
```env
# OpenRouter API Key (Used for the LLM)
ANTHROPIC_API_KEY=your_openrouter_or_anthropic_api_key_here

# Telegram Bot Token (from @BotFather)
TELEGRAM_KEY=your_telegram_bot_token_here

# MongoDB Variables
MONGO_URI=your_mongodb_connection_string
```

### 4. Running the Application

**To start the FastAPI server & Swagger UI:**
```bash
uvicorn main:app --reload
```
You can access the Swagger documentation at `http://127.0.0.1:8000/docs`.

**To start the Telegram Bot:**
Open a separate terminal, activate the virtual environment, and run:
```bash
python tele.py
```