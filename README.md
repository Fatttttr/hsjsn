# VPN Bot Checker

Simple VPN monitoring bot dengan Telegram notifications.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure:**
   ```bash
   cp config.json config.json.example
   # Edit config.json dengan credentials Anda
   ```

3. **Run:**
   ```bash
   python bot.py
   ```

## Config

Edit `config.json`:
```json
{
  "github_token": "your_github_token_here",
  "github_owner": "your_github_owner",
  "github_repo": "your_repo_name",
  "check_interval_minutes": 60,
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

## Files

- `bot.py` - Main bot script
- `config.json` - Configuration file
- `core/` - VPN testing logic
- `requirements.txt` - Dependencies