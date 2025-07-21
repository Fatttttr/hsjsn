# 🚀 Quick Bot Setup - Test Mode

Bot VPN checker dengan interval menit (untuk testing cepat) dan pesan sederhana hidup/mati.

## ⚡ **Setup Cepat (5 Menit)**

### **1. Copy Config**
```bash
cp bot_config.json.example bot_config.json
```

### **2. Edit Minimal Config**
Edit `bot_config.json`:
```json
{
  "github_token": "ghp_your_token_here",
  "github_owner": "your-username", 
  "github_repo": "your-repo-name",
  "config_file": "template.json",
  
  "check_interval_minutes": 5,
  
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_chat_id"
}
```

### **3. Install Dependencies**
```bash
pip install schedule pyTelegramBotAPI requests
```

### **4. Test Bot**
```bash
python3 test_bot.py
```

### **5. Run Bot**
```bash
python3 bot_vpn_checker.py
```

## 📱 **Telegram Setup Cepat**

### **Buat Bot:**
1. Chat **@BotFather** di Telegram
2. Send: `/newbot`
3. Nama: `VPN Monitor Bot`
4. Username: `your_vpn_monitor_bot`
5. **Copy token** yang diberikan

### **Get Chat ID:**
1. Start chat dengan bot Anda
2. Send message apa saja
3. Open: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Cari `"chat":{"id":123456789}` - ini Chat ID Anda

## 📊 **Sample Message Output**

Bot akan kirim pesan seperti ini setiap 5 menit:

```
🔍 VPN Status Report - 14:30:25

✅ Akun Hidup: 12
❌ Akun Mati: 3  
📦 Total: 15

📊 80% akun masih berfungsi

🔄 Cek otomatis setiap 5 menit
```

## ⚙️ **Interval Settings**

Edit `check_interval_minutes` di config:
- `1` = Setiap 1 menit (testing intensif)
- `5` = Setiap 5 menit (default testing)
- `15` = Setiap 15 menit 
- `60` = Setiap 1 jam (production)

## 🧪 **Testing Commands**

```bash
# Test format pesan saja
python3 test_bot.py

# Test single check manual
python3 -c "
import asyncio
from bot_vpn_checker import VPNBotChecker, load_bot_config
config = load_bot_config()
config.check_interval_minutes = 1
bot = VPNBotChecker(config) 
asyncio.run(bot.run_check())
"

# Run bot dengan log
python3 bot_vpn_checker.py 2>&1 | tee bot.log
```

## 🛑 **Stop Bot**
```bash
# Press Ctrl+C atau
pkill -f bot_vpn_checker.py
```

Bot siap test dengan interval menit dan pesan simple! 🎉