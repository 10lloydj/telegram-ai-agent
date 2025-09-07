# Telegram AI Job Agent

A Python-based Telegram bot that monitors group chats for job postings and uses OpenAI to classify and alert you about relevant opportunities.

## Features
- 🤖 **AI-powered job detection** using OpenAI's API with structured JSON output
- 📱 **Telegram integration** via Telethon (no bot token needed - runs as your user)
- 🗄️ **PostgreSQL storage** for messages and classification results
- 🔔 **Smart notifications** with confidence scoring and quiet hours
- 🎯 **Configurable filtering** for roles, locations, tech stack, and seniority
- 🐳 **Docker support** for easy deployment

## Quick Start

### 1. Prerequisites
- Python 3.10+ with pip
- Docker and Docker Compose
- Telegram API credentials ([get them here](https://my.telegram.org/apps))
- OpenAI API key

### 2. Setup
```bash
# Clone and install
git clone <your-repo-url>
cd telegram-ai-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys and settings
```

### 3. Get Telegram Session
```bash
# Authenticate with Telegram (one-time setup)
python3 quick_login.py
# Follow prompts to enter phone + verification code
```

### 4. Find Your Target Chat ID
```bash
# Listen for messages to get chat IDs
python3 sniff_chat_id.py
# Send a message in your target group, copy the chat ID
# Update TARGET_CHAT_ID in .env with the numeric ID
```

### 5. Run the Agent
```bash
# Start PostgreSQL
docker compose up -d db

# Run the agent
python3 -m app
```

## Configuration

Edit `config/app.yaml` to customize:
- Target job roles and seniority levels
- Preferred locations and remote work
- Tech stack preferences
- Confidence thresholds
- Quiet hours for notifications

## Environment Variables

Key variables in `.env`:
```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
TARGET_CHAT_ID=-100xxxxxxxxxx  # Numeric chat ID
OPENAI_API_KEY=sk-...
MIN_CONFIDENCE=0.70
QUIET_HOURS_START=23
QUIET_HOURS_END=7
```

## How It Works

1. **Listens** to messages in configured Telegram groups
2. **Classifies** each message using OpenAI to determine if it's a relevant job posting
3. **Stores** all messages and classifications in PostgreSQL
4. **Alerts** you via Telegram DM when relevant jobs are found (above confidence threshold, outside quiet hours)
5. **Deduplicates** alerts to avoid spam

## Architecture

- `app/ingestion.py` - Telegram message handling and topic detection
- `app/llm.py` - OpenAI integration with structured JSON output
- `app/notifier.py` - DM formatting and delivery
- `app/models.py` - SQLAlchemy database models
- `app/service.py` - Main application orchestration

## License

MIT