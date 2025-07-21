# 🤖 VPN Bot Testing Repository

Repository khusus untuk VPN Bot Checker yang akan monitor akun VPN dari repository lain secara otomatis.

## 📁 **Repository Structure**

```
bot_testing/
├── README.md                    # This file
├── bot_vpn_checker.py          # Main bot script
├── bot_config.json.example     # Configuration template
├── bot_config.json             # Your actual config (gitignored)
├── bot_requirements.txt        # Python dependencies
├── test_bot.py                 # Test script
├── core/                       # VPN testing logic
│   ├── __init__.py
│   ├── github_client.py        # GitHub API client
│   ├── core.py                 # VPN testing functions
│   ├── extractor.py            # Config extraction
│   └── converter.py            # Link parsing
├── logs/
│   └── vpn_bot.log            # Bot logs
└── docs/
    ├── QUICK_BOT_SETUP.md     # Quick setup guide
    └── VPN_BOT_SETUP_GUIDE.md # Complete setup guide
```

## 🎯 **How It Works**

### **Repository Separation:**
- **`bot_testing` (this repo):** Contains bot code and logic
- **`your-vpn-repo`:** Contains VPN configurations to be tested
- **Bot monitors:** Remote VPN repo via GitHub API

### **Process Flow:**
```
1. Bot runs every X minutes (configurable)
2. Fetch config from remote VPN repository 
3. Extract VPN accounts using same logic as VortexVPN Manager
4. Test all accounts in parallel
5. Send simple report via Telegram/WhatsApp:
   - ✅ Akun Hidup: X
   - ❌ Akun Mati: Y
   - 📦 Total: Z
```

## 🚀 **Quick Start**

### **1. Clone/Setup Repository**
```bash
git clone <this-repo> bot_testing
cd bot_testing
```

### **2. Install Dependencies**
```bash
pip install -r bot_requirements.txt
```

### **3. Configure Bot**
```bash
cp bot_config.json.example bot_config.json
nano bot_config.json
```

### **4. Set Target VPN Repository**
Edit `bot_config.json`:
```json
{
  "github_token": "ghp_your_token",
  "github_owner": "your-username",
  "github_repo": "your-vpn-config-repo",  // Target repo to monitor
  "config_file": "template.json",
  
  "check_interval_minutes": 5,
  "telegram_token": "your_bot_token",
  "telegram_chat_id": "your_chat_id"
}
```

### **5. Test & Run**
```bash
# Test first
python3 test_bot.py

# Run bot
python3 bot_vpn_checker.py
```

## 📊 **Sample Notification**

Bot will send messages like this every 5 minutes:

```
🔍 VPN Status Report - 14:30:25

✅ Akun Hidup: 12
❌ Akun Mati: 3  
📦 Total: 15

📊 80% akun masih berfungsi

🔄 Cek otomatis setiap 5 menit
```

## ⚙️ **Configuration Options**

- **`check_interval_minutes`:** How often to check (1, 5, 15, 60, etc.)
- **`github_repo`:** Which repository to monitor for VPN configs
- **`config_file`:** Which file in target repo to use
- **`send_only_failures`:** Only notify when accounts fail
- **`max_concurrent_tests`:** Parallel testing limit

## 🔧 **Monitoring Multiple Repositories**

You can run multiple bot instances to monitor different VPN repositories:

```bash
# Bot 1: Monitor production VPNs
cp bot_config.json bot_config_prod.json
# Edit to point to production repo

# Bot 2: Monitor testing VPNs  
cp bot_config.json bot_config_test.json
# Edit to point to testing repo

# Run separately
python3 bot_vpn_checker.py --config bot_config_prod.json &
python3 bot_vpn_checker.py --config bot_config_test.json &
```

## 📱 **Telegram Setup**

1. **Create Bot:** Chat @BotFather → `/newbot`
2. **Get Token:** Copy the bot token  
3. **Get Chat ID:** Message your bot, then visit:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. **Configure:** Add token and chat_id to config

## 🎯 **Use Cases**

- **Personal Monitoring:** Check your VPN accounts every hour
- **Team Monitoring:** Monitor shared VPN configs 
- **Multi-Repository:** Different bots for different VPN setups
- **Development:** Test with 1-minute intervals for quick feedback

## 📝 **Files Included**

- `bot_vpn_checker.py` - Main bot script
- `core/` - VPN testing logic (reused from VortexVPN Manager)
- `test_bot.py` - Test script for debugging
- `docs/` - Setup guides and documentation

## 🔒 **Security**

- `bot_config.json` is gitignored (contains tokens)
- Bot only reads from target VPN repository  
- No sensitive data stored in this repository
- GitHub token needs read access to target repo

---

**Ready to monitor your VPN accounts 24/7!** 🚀