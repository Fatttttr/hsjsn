# 🤖 VPN Bot Checker - Setup for Separate Repository

Bot VPN checker yang akan monitor akun VPN dari repository ini secara otomatis.

## 📍 **Repository Structure**

### **This Repository (VortexVPN Manager):**
- ✅ Web interface untuk manual testing & config management
- ✅ GitHub integration dengan dropdown & create config
- ✅ VPN testing logic & algorithms
- ✅ Template system & account extraction

### **Bot Repository (`bot_testing`):**
- 🤖 Automated VPN monitoring bot
- 📱 Telegram/WhatsApp notifications  
- ⏰ Scheduled checking (every X minutes)
- 📊 Simple hidup/mati reports
- 🔗 Monitors this repository via GitHub API

## 🚀 **How to Setup Bot (Separate Repository)**

### **1. Create `bot_testing` Repository**
```bash
# Create new repository
mkdir bot_testing
cd bot_testing
git init
```

### **2. Create Bot Files Structure**
```
bot_testing/
├── bot_vpn_checker.py          # Main bot script
├── bot_config.json.example     # Config template
├── bot_requirements.txt        # Dependencies
├── test_bot.py                 # Test script
├── README.md                   # Bot documentation
└── core/                       # VPN logic (copied)
    ├── __init__.py
    ├── github_client.py
    ├── core.py
    ├── extractor.py
    └── converter.py
```

### **3. Copy Required Files**

Copy these files from VortexVPN Manager to `bot_testing/core/`:
- `github_client.py`
- `core.py` 
- `extractor.py`
- `converter.py`

### **4. Bot Configuration**

Create `bot_config.json`:
```json
{
  "github_token": "ghp_your_github_token",
  "github_owner": "your-username",
  "github_repo": "vortex-vpn-manager",  // This repository
  "config_file": "template.json",       // File to monitor
  
  "check_interval_minutes": 5,
  "max_concurrent_tests": 5,
  "send_only_failures": false,
  "send_summary": true,
  
  "telegram_token": "your_telegram_bot_token",
  "telegram_chat_id": "your_chat_id"
}
```

## 📱 **Sample Bot Messages**

Bot will send simple reports like this:

```
🔍 VPN Status Report - 14:30:25

✅ Akun Hidup: 12
❌ Akun Mati: 3  
📦 Total: 15

📊 80% akun masih berfungsi

🔄 Cek otomatis setiap 5 menit
```

## 🎯 **Workflow**

### **Manual Testing (This Repository):**
1. Use VortexVPN Manager web interface
2. Add VPN links via smart detection
3. Test accounts manually
4. Download/upload configs to GitHub

### **Automated Monitoring (Bot Repository):**
1. Bot monitors this repository's config files
2. Extracts accounts using same logic
3. Tests accounts every X minutes
4. Sends hidup/mati reports via Telegram

## 🔧 **Key Features**

### **Bot Advantages:**
- ⏰ **24/7 monitoring** of VPN accounts
- 📱 **Instant notifications** when accounts fail
- 📊 **Simple reports** (hidup/mati counts only)
- 🔄 **Automated testing** without manual intervention
- 🎯 **Focuses on uptime** monitoring

### **VortexVPN Manager Advantages:**
- 🌐 **Web interface** for interactive testing
- 🔧 **Configuration management** with GitHub integration
- 📊 **Detailed results** with latency, country, provider
- 🎨 **Visual feedback** with real-time progress
- 🛠️ **Advanced features** like custom servers

## 🎪 **Use Cases**

### **Personal Setup:**
- **VortexVPN Manager:** Weekend config updates & testing
- **Bot:** Daily monitoring notifications

### **Team Setup:**
- **VortexVPN Manager:** Team lead manages configs
- **Bot:** Team gets automated status updates

### **Production Setup:**
- **VortexVPN Manager:** Staging environment testing
- **Bot:** Production monitoring alerts

## 📝 **Next Steps**

1. **Keep using VortexVPN Manager** untuk config management
2. **Create bot_testing repository** untuk automated monitoring
3. **Copy required core files** ke bot repository
4. **Setup Telegram bot** untuk notifications
5. **Configure monitoring** dengan interval yang sesuai

## 🔗 **Repository Links**

- **VortexVPN Manager:** This repository (manual testing & config management)
- **Bot Testing:** Separate repository for automated monitoring
- **Target Config:** Repository yang dimonitor oleh bot (bisa sama atau berbeda)

---

**Bot akan monitor repository ini dan kirim laporan hidup/mati otomatis!** 🚀