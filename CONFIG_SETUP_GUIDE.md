# ⚙️ Bot Configuration Setup Guide

Panduan setup `bot_config.json` dengan token dan info repository yang sebenarnya.

## 📋 Step-by-Step Setup

### 1. Copy Template
```bash
cp bot_config.json.example bot_config.json
```

### 2. Edit Configuration
Buka `bot_config.json` dan ganti semua placeholder dengan info asli:

## 🔧 Configuration Fields

### **GitHub Settings (WAJIB)**
```json
{
  "github_token": "ghp_your_github_personal_access_token",
  "github_owner": "Fatttttr",
  "github_repo": "hsjsn"
}
```

**Cara dapat GitHub Token:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Pilih scope: `repo` (full control of private repositories)
4. Copy token yang dimulai dengan `ghp_`

### **Telegram Settings (WAJIB)**
```json
{
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

**Cara dapat Telegram Token & Chat ID:**
- Lihat panduan lengkap di `TELEGRAM_BOT_SETUP.md`
- Atau jalankan: `python test_telegram.py`

### **Testing Settings (OPSIONAL)**
```json
{
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "timeout_seconds": 10,
  "send_summary": true
}
```

### **WhatsApp Settings (OPSIONAL)**
```json
{
  "twilio_account_sid": "your_twilio_account_sid",
  "twilio_auth_token": "your_twilio_auth_token",
  "twilio_whatsapp_from": "whatsapp:+14155238886",
  "whatsapp_to": "whatsapp:+6281234567890"
}
```

## 📋 Complete Example

### Minimal Configuration (Hanya Telegram)
```json
{
  "github_token": "ghp_your_github_token_here",
  "github_owner": "Fatttttr",
  "github_repo": "hsjsn",
  
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "timeout_seconds": 10,
  
  "send_summary": true,
  
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

### Full Configuration (Telegram + WhatsApp)
```json
{
  "github_token": "ghp_your_github_token_here",
  "github_owner": "Fatttttr", 
  "github_repo": "hsjsn",
  
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "timeout_seconds": 10,
  
  "send_only_failures": false,
  "send_summary": true,
  
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id",
  
  "twilio_account_sid": "your_twilio_account_sid",
  "twilio_auth_token": "your_twilio_auth_token",
  "twilio_whatsapp_from": "whatsapp:+14155238886",
  "whatsapp_to": "whatsapp:+6281234567890"
}
```

## 🔒 Security Notes

### ❌ JANGAN COMMIT bot_config.json
```bash
# Add to .gitignore
echo "bot_config.json" >> .gitignore
```

### ✅ Yang Aman di-commit:
- `bot_config.json.example` (template)
- File dengan placeholder values
- Panduan dan dokumentasi

### ❌ Yang TIDAK boleh di-commit:
- `bot_config.json` (dengan token asli)
- File dengan token/password asli
- Credentials apapun

## 🧪 Testing Configuration

### 1. Test File Valid
```bash
python -c "import json; print('✅ Valid JSON' if json.load(open('bot_config.json')) else '❌ Invalid')"
```

### 2. Test Telegram Connection
```bash
python test_telegram.py
```

### 3. Test Full Bot
```bash
python test_bot.py
```

## 📋 Checklist

Before running the bot, pastikan:

- [ ] ✅ `bot_config.json` exists (copied from example)
- [ ] ✅ GitHub token valid dan punya akses repo
- [ ] ✅ Telegram bot token valid
- [ ] ✅ Chat ID benar (test dengan test_telegram.py)
- [ ] ✅ Repository "hsjsn" accessible
- [ ] ✅ Ada file JSON di repository untuk di-monitor
- [ ] ✅ bot_config.json ada di .gitignore

## 🐛 Common Issues

### ❌ "Missing required GitHub configuration!"
**Solusi:**
- Pastikan `bot_config.json` exists
- Check semua field wajib terisi
- Pastikan tidak ada typo di field names

### ❌ "FileNotFoundError: bot_config.json"
**Solusi:**
```bash
cp bot_config.json.example bot_config.json
# Then edit bot_config.json
```

### ❌ "Invalid JSON format"
**Solusi:**
- Check JSON syntax (comma, quotes, brackets)
- Test dengan: `python -c "import json; json.load(open('bot_config.json'))"`
- Use JSON validator online

### ❌ "GitHub API rate limit"
**Solusi:**
- Pastikan pakai token (bukan anonymous)
- Check token permissions
- Wait jika rate limit exceeded

---

**🎯 Setelah setup, bot akan monitor semua file JSON di repository dan kirim laporan per file ke Telegram!** 🤖