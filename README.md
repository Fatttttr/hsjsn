# 🤖 VPN Bot Checker

Automated VPN account monitoring bot yang secara otomatis mengecek status VPN accounts dari repository ini dan mengirim laporan melalui Telegram/WhatsApp.

## 📍 Overview

Bot ini dirancang untuk:
- 🔄 **Monitor otomatis** VPN accounts dari file `template.json` di repository ini
- ⏰ **Scheduled checking** dengan interval yang bisa diatur (dalam menit)
- 📱 **Notifikasi real-time** via Telegram & WhatsApp
- 📊 **Laporan sederhana** jumlah akun hidup/mati
- 🚀 **Menggunakan logic testing** yang sama dengan VortexVPN Manager

## 🏗️ Repository Structure

### **Branch Strategy:**
- **`main`**: VortexVPN Manager (Web interface untuk manual testing)
- **`bot-vpn-checker`**: Bot VPN Checker (Branch ini - Automated monitoring)

### **Bot Purpose:**
Bot ini akan monitor file `template.json` di repository ini dan mengirim laporan status VPN accounts secara otomatis.

## 🚀 Quick Start

### 1. Clone & Switch Branch
```bash
git clone https://github.com/Fatttttr/hsjsn.git
cd hsjsn
git checkout bot-vpn-checker
```

### 2. Install Dependencies
```bash
pip install -r bot_requirements.txt
```

### 3. Setup Configuration
```bash
cp bot_config.json.example bot_config.json
# Edit bot_config.json dengan credentials Anda
```

### 4. Test Bot
```bash
python test_bot.py
```

### 5. Run Bot
```bash
python bot_vpn_checker.py
```

## ⚙️ Configuration

Edit `bot_config.json`:

```json
{
  "github_token": "ghp_your_github_token",
  "github_owner": "Fatttttr",
  "github_repo": "hsjsn",
  "config_file": "template.json",
  
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "timeout_seconds": 10,
  
  "send_summary": true,
  
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

### Configuration Details:
- **`github_token`**: Personal Access Token untuk akses repository ini
- **`github_owner`**: "Fatttttr" (fixed)
- **`github_repo`**: "hsjsn" (repository ini)
- **`config_file`**: "template.json" (file yang dimonitor)
- **`check_interval_minutes`**: Interval pengecekan (default: 5 menit)
- **`telegram_token`**: Bot token dari @BotFather
- **`telegram_chat_id`**: Chat ID untuk notifikasi

## 📱 Setup Telegram Bot

### 1. Create Bot
1. Chat dengan [@BotFather](https://t.me/BotFather)
2. Gunakan `/newbot` dan ikuti instruksi
3. Simpan **token** yang diberikan

### 2. Get Chat ID
1. Start bot Anda di Telegram
2. Kirim pesan ke bot
3. Akses: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Cari `"chat":{"id":CHAT_ID}`

## 🧪 Testing

### Manual Test
```bash
python test_bot.py
```

Test ini akan:
- ✅ Load konfigurasi
- 🔍 Test koneksi ke repository ini
- 📊 Load dan test VPN accounts dari template.json
- 📱 Format sample notification message
- 🚀 Optional: kirim test notification

## 🔄 Bot Workflow

1. **Load config** dari `bot_config.json`
2. **Monitor** file `template.json` di repository ini
3. **Extract VPN accounts** menggunakan logic yang sama dengan VortexVPN Manager
4. **Test accounts** secara concurrent
5. **Send notification** dengan format sederhana:

```
🔍 VPN Status Report - 14:30:25

✅ Akun Hidup: 12
❌ Akun Mati: 3
📦 Total: 15

📊 80% akun masih berfungsi

🔄 Cek otomatis setiap 5 menit
```

## 📁 File Structure

```
bot-vpn-checker branch/
├── bot_vpn_checker.py          # Main bot script
├── bot_config.json.example     # Configuration template
├── bot_config.json             # Your configuration (create this)
├── bot_requirements.txt        # Python dependencies
├── test_bot.py                 # Manual testing script
├── README.md                   # This documentation
└── core/                       # VPN testing logic
    ├── __init__.py            # Package initialization
    ├── github_client.py       # GitHub API client
    ├── core.py                # VPN testing core
    ├── extractor.py           # Account extraction
    └── converter.py           # Config conversion
```

## 🔧 Advanced Usage

### Run as Service (Linux)
```bash
# Create systemd service
sudo nano /etc/systemd/system/vpn-bot.service

[Unit]
Description=VPN Bot Checker
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/hsjsn
ExecStart=/usr/bin/python3 bot_vpn_checker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable vpn-bot
sudo systemctl start vpn-bot
```

### Environment Variables
Alternatif konfigurasi:
```bash
export GITHUB_TOKEN="ghp_your_token"
export GITHUB_OWNER="Fatttttr"
export GITHUB_REPO="hsjsn"
export CONFIG_FILE="template.json"
export CHECK_INTERVAL_MINUTES="5"
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## 🐛 Troubleshooting

### Common Issues

**❌ "Missing required GitHub configuration!"**
- Pastikan `bot_config.json` ada dan terisi lengkap
- Cek GitHub token masih valid dan punya akses ke repository ini

**❌ "No VPN accounts found"**  
- Pastikan file `template.json` ada di repository
- Cek format JSON valid
- Pastikan ada VPN accounts di dalam config

**❌ "Failed to send Telegram notification"**
- Cek Telegram token valid
- Pastikan bot sudah di-start di Telegram
- Cek chat ID benar

### Debug Mode
```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('bot_vpn_checker.py').read())
"
```

## 🔗 Related Branches

- **[main branch](../../tree/main)**: VortexVPN Manager - Web interface untuk manual testing
- **[bot-vpn-checker branch](../../tree/bot-vpn-checker)**: Branch ini - Automated monitoring bot

## 📄 License

MIT License - Feel free to use and modify.

---

**🤖 Bot akan monitor template.json di repository ini dan kirim laporan hidup/mati otomatis via Telegram!** 🚀