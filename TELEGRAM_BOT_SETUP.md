# 📱 Telegram Bot Setup Guide

Panduan lengkap untuk mendapatkan Telegram Bot Token dan Chat ID untuk VPN Bot Checker.

## 🤖 Part 1: Membuat Bot & Mendapatkan Token

### 1. Chat dengan BotFather
1. Buka Telegram
2. Search: **@BotFather**
3. Start chat dengan BotFather

### 2. Buat Bot Baru
```
Kirim: /newbot

BotFather akan tanya:
"Alright, a new bot. How are we going to call it? Please choose a name for your bot."

Contoh jawab: VPN Status Bot
```

### 3. Pilih Username Bot
```
BotFather akan tanya:
"Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot."

Contoh jawab: vpn_status_checker_bot
(Harus unik, kalau sudah ada coba yang lain)
```

### 4. Dapatkan Token
```
BotFather akan kirim pesan seperti ini:

"Done! Congratulations on your new bot. You will find it at t.me/vpn_status_checker_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890

Keep your token secure and store it safely, it can be used by anyone to control your bot."
```

**✅ Copy token yang panjang itu (contoh: `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890`)**

## 💬 Part 2: Mendapatkan Chat ID

### Method 1: Via Bot langsung (Mudah)

#### 1. Start Bot Anda
1. Click link yang diberikan BotFather (contoh: `t.me/vpn_status_checker_bot`)
2. Click **"START"** atau ketik `/start`

#### 2. Kirim Pesan Test
```
Kirim pesan apa saja ke bot, contoh:
"Hello bot!"
```

#### 3. Ambil Chat ID via API
1. Buka browser
2. Masukkan URL ini (ganti `YOUR_BOT_TOKEN` dengan token Anda):
```
https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890/getUpdates
```

#### 4. Cari Chat ID
Anda akan lihat response JSON seperti ini:
```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456789,
      "message": {
        "message_id": 1,
        "from": {
          "id": 987654321,
          "is_bot": false,
          "first_name": "Your Name",
          "username": "yourusername"
        },
        "chat": {
          "id": 987654321,
          "first_name": "Your Name",
          "username": "yourusername",
          "type": "private"
        },
        "date": 1234567890,
        "text": "Hello bot!"
      }
    }
  ]
}
```

**✅ Copy angka di `"chat": {"id": 987654321}` - itu adalah Chat ID Anda**

### Method 2: Via @userinfobot (Alternatif)

#### 1. Chat dengan @userinfobot
1. Search: **@userinfobot**
2. Start chat
3. Kirim pesan apa saja

#### 2. Dapatkan User ID
Bot akan reply dengan info Anda termasuk **User ID** yang sama dengan Chat ID untuk private chat.

### Method 3: Via @chatidbot (Alternatif)

#### 1. Chat dengan @chatidbot
1. Search: **@chatidbot**
2. Start chat

#### 2. Dapatkan Chat ID
Bot akan langsung kirim Chat ID Anda.

## 🔧 Part 3: Konfigurasi Bot

### Edit bot_config.json
```json
{
  "github_token": "ghp_your_github_token",
  "github_owner": "Fatttttr",
  "github_repo": "hsjsn",
  
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "timeout_seconds": 10,
  
  "send_summary": true,
  
  "telegram_token": "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890",
  "telegram_chat_id": "987654321"
}
```

## 🧪 Part 4: Test Bot

### Test Manual
```bash
python test_bot.py
```

Pilih "y" ketika ditanya kirim test notification untuk memastikan bot berfungsi.

### Test via Python Script
Buat file `test_telegram.py`:
```python
import requests

bot_token = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890"
chat_id = "987654321"
message = "🧪 Test message from VPN Bot!"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": message
}

response = requests.post(url, data=data)
print("Response:", response.json())
```

```bash
python test_telegram.py
```

## 📋 Troubleshooting

### ❌ "Unauthorized" Error
- **Masalah**: Token salah atau tidak valid
- **Solusi**: Copy ulang token dari BotFather, pastikan lengkap

### ❌ "Chat not found" Error  
- **Masalah**: Chat ID salah atau bot belum di-start
- **Solusi**: 
  1. Pastikan sudah start bot di Telegram
  2. Kirim pesan dulu ke bot
  3. Check ulang Chat ID via `/getUpdates`

### ❌ "Forbidden" Error
- **Masalah**: Bot di-block atau tidak punya permission
- **Solusi**: Unblock bot di Telegram, start ulang bot

### ❌ Bot tidak respond
- **Masalah**: Bot mungkin tidak active
- **Solusi**: 
  1. Check bot masih ada di @BotFather
  2. Pastikan token masih valid
  3. Restart bot jika perlu

## 💡 Tips

### Keamanan Token
- ❌ **Jangan share** token di public
- ❌ **Jangan commit** token ke git
- ✅ **Simpan aman** di `bot_config.json`
- ✅ **Add ke .gitignore**: `bot_config.json`

### Multiple Chats
Untuk kirim ke group atau multiple users:
```json
{
  "telegram_chat_id": "group_chat_id_atau_channel_id"
}
```

### Bot Commands (Optional)
Tambah commands via @BotFather:
```
/setcommands

status - Check VPN status now
help - Show help message
```

## 🎯 Quick Summary

### Yang Anda Butuhkan:
1. **Bot Token**: Dari @BotFather (format: `number:letters`)
2. **Chat ID**: Dari `/getUpdates` API (format: `number`)

### Langkah Cepat:
1. Chat @BotFather → `/newbot` → dapat token
2. Start bot Anda → kirim pesan
3. Buka `https://api.telegram.org/botTOKEN/getUpdates`
4. Copy Chat ID dari response
5. Masukkan ke `bot_config.json`
6. Test dengan `python test_bot.py`

---

**🤖 Setelah setup, bot akan kirim laporan VPN status otomatis ke Telegram Anda!** 📱