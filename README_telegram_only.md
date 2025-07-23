# 📱 VPN Bot Checker - Telegram Only Version

Simplified VPN monitoring bot dengan **hanya Telegram notifications**. Dioptimized untuk mobile data usage dan Android deployment.

## ✨ Features

- 🤖 **Telegram-only notifications** (no WhatsApp/Twilio)
- 📱 **Mobile-optimized** dengan data usage minimal
- 🔧 **Simplified configuration** (hanya perlu Telegram + GitHub)
- ⚡ **Lightweight** dan efficient
- 🌍 **Same advanced testing** seperti main branch
- 📊 **Per-file reporting** dengan country flags

## 🚀 Quick Start

### 1. Android Setup (Termux)
```bash
# Install Termux dari F-Droid atau Play Store
pkg update && pkg upgrade
pkg install python git

# Clone repository
git clone https://github.com/Fatttttr/hsjsn.git
cd hsjsn
git checkout bot-vpn-checker

# Install dependencies
pip install -r telegram_requirements.txt
```

### 2. Configuration
```bash
# Copy template
cp bot_config_telegram_only.json.example bot_config_telegram_only.json

# Edit dengan credentials Anda
nano bot_config_telegram_only.json
```

#### Required Configuration:
```json
{
  "github_token": "ghp_your_github_token_here",
  "github_owner": "Fatttttr",
  "github_repo": "fattt",
  "check_interval_minutes": 60,
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

### 3. Get Telegram Credentials

#### Bot Token:
1. Message @BotFather di Telegram
2. Send `/newbot`
3. Follow instructions
4. Copy bot token

#### Chat ID:
1. Start conversation dengan your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Copy `chat.id` from response

### 4. Run Bot
```bash
# Run directly
python bot_telegram_only.py

# Run persistent dengan tmux
pkg install tmux
tmux new -s vpn-bot
python bot_telegram_only.py
# Ctrl+B, D to detach
```

## 📊 Data Usage Optimization

### Mobile-Optimized Settings:
- ✅ **60-minute intervals** (instead of 30)
- ✅ **3 concurrent tests** (instead of 5)
- ✅ **8-second timeouts** (instead of 10)
- ✅ **No WhatsApp/Twilio** dependencies

### Expected Data Usage:
```
Per check: ~200KB
Daily (24 checks): ~4.8MB
Monthly: ~144MB

With Android overhead: ~300MB/month total
```

## 🎯 Perfect For

- 📱 **Android phones** dengan limited data
- 🔒 **Security-conscious** users (no third-party services)
- 💰 **Budget-friendly** hosting (free atau minimal cost)
- 🚀 **Simple deployment** tanpa complex setup

## 📱 Expected Output

```
🔍 VPN Status Report - 14:30:25

✅ testing.json
   Hidup: 50 | Mati: 0 | Total: 50
   Status: 100% berfungsi
   Countries: 🇦🇹 🇩🇪 🇪🇪 🇫🇮 🇫🇷

✅ vpn-config-2025-07-21.json
   Hidup: 5 | Mati: 0 | Total: 5
   Status: 100% berfungsi
   Countries: 🇨🇦 🇩🇪

📊 RINGKASAN TOTAL
✅ Total Hidup: 55
❌ Total Mati: 0
📦 Total Akun: 55
📈 Success Rate: 100%

🔄 Cek otomatis setiap 60 menit
```

## 💡 Pro Tips

### Android Optimization:
- Enable "Stay awake while charging"
- Disable battery optimization untuk Termux
- Use termux-wake-lock untuk prevent sleep
- Monitor data usage dengan operator app

### Cost-Effective:
- Use 500MB-1GB data plan (~Rp 15-25k/month)
- Much cheaper than cloud hosting
- Full control over security
- No monthly subscriptions

## 🔒 Security

- ✅ **No third-party services** (except GitHub + Telegram)
- ✅ **Local execution** on your device
- ✅ **Minimal credentials** required
- ✅ **Full control** over data

Perfect untuk secure, budget-friendly VPN monitoring! 🚀
