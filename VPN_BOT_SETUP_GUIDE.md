# 🤖 VPN Bot Checker - Setup Guide

Automated VPN account monitoring bot dengan notifikasi WhatsApp & Telegram.

## 🎯 **Features**

### **Core Functions:**
- ✅ **Auto-extract** VPN accounts dari GitHub repository
- 🔍 **Scheduled testing** setiap X jam (configurable)
- 📱 **Dual notifications** WhatsApp + Telegram
- 📊 **Smart reporting** summary & failed accounts only
- 🔄 **Auto-retry** dan error handling
- 📝 **Detailed logging** untuk debugging

### **Notification Types:**
- 📈 **Summary reports** (successful/failed counts)
- 🚨 **Failure alerts** (specific failed accounts)
- ⚠️ **Error notifications** (bot errors)
- 📊 **Top performers** (best latency accounts)

## 📋 **Prerequisites**

### **Required:**
- ✅ GitHub repository dengan VPN config
- ✅ GitHub token (sama dengan VortexVPN Manager)
- ✅ Python 3.7+ environment

### **Optional (pilih salah satu atau keduanya):**
- 📱 **Telegram:** Bot token + Chat ID
- 📱 **WhatsApp:** Twilio account + Phone numbers

## 🚀 **Quick Setup**

### **1. Install Dependencies**
```bash
pip install -r bot_requirements.txt
```

### **2. Copy Configuration**
```bash
cp bot_config.json.example bot_config.json
```

### **3. Configure Settings**
Edit `bot_config.json` dengan details Anda:

```json
{
  "github_token": "ghp_your_actual_token",
  "github_owner": "your-username", 
  "github_repo": "your-vpn-repo",
  "config_file": "template.json",
  
  "check_interval_hours": 6,
  "telegram_token": "your_bot_token",
  "telegram_chat_id": "your_chat_id"
}
```

### **4. Run Bot**
```bash
python3 bot_vpn_checker.py
```

## 📱 **Telegram Setup (Recommended)**

### **Step 1: Create Bot**
1. Open Telegram, search **@BotFather**
2. Send `/newbot` command
3. Choose bot name: `Your VPN Monitor Bot`
4. Choose username: `your_vpn_bot`
5. **Copy the token** (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### **Step 2: Get Chat ID**
1. Start chat dengan bot Anda (click link dari BotFather)
2. Send any message to your bot
3. Open: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat":{"id":123456789` - ini Chat ID Anda

### **Step 3: Test**
```bash
curl -X POST \
  "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage" \
  -d "chat_id=<YOUR_CHAT_ID>&text=VPN Bot Test"
```

## 📱 **WhatsApp Setup (Via Twilio)**

### **Step 1: Twilio Account**
1. Sign up: https://www.twilio.com/
2. Get **Account SID** dan **Auth Token**
3. Go to Console → Programmable Messaging → WhatsApp sandbox

### **Step 2: WhatsApp Sandbox**
1. **Sandbox number:** `+1 415 523 8886` (Twilio default)
2. **Join sandbox:** Send WhatsApp message "join <your-sandbox-code>" ke +1 415 523 8886
3. **Your number:** Format +62812345678 (with country code)

### **Step 3: Test**
```python
from twilio.rest import Client

client = Client("your_sid", "your_token")
message = client.messages.create(
    body="VPN Bot Test",
    from_="+14155238886",
    to="+62812345678"  # Your number
)
```

## ⚙️ **Configuration Options**

### **Core Settings:**
```json
{
  "check_interval_hours": 6,     // How often to check
  "max_concurrent_tests": 5,     // Parallel testing limit
  "send_only_failures": false,   // Only notify on failures
  "send_summary": true           // Send full summary reports
}
```

### **Notification Modes:**

#### **Mode 1: Full Reports (Recommended)**
```json
{
  "send_only_failures": false,
  "send_summary": true
}
```
- 📊 **Every check:** Summary report
- 🚨 **On failures:** Additional failure alert

#### **Mode 2: Failures Only**
```json
{
  "send_only_failures": true,
  "send_summary": false  
}
```
- 🔕 **Quiet mode:** Only when accounts fail
- 🚨 **Alert mode:** Immediate failure notifications

#### **Mode 3: Summary Only**
```json
{
  "send_only_failures": false,
  "send_summary": true
}
```
- 📈 **Regular reports:** Every check cycle
- 📊 **Includes:** Success + failure counts

## 📊 **Sample Notifications**

### **Summary Report:**
```
🔍 VPN Account Check Report
📅 Time: 2024-07-21 14:30:00
📊 Results: 15✅ / 2❌ / 17📦

⚠️ 2 accounts need attention

❌ Failed Accounts:
• VLESS: Singapore-Server-1
• TROJAN: Japan-Backup

✅ Top Working Accounts:
• VLESS 🇸🇬 (25ms)
• TROJAN 🇯🇵 (45ms)
• SS 🇺🇸 (78ms)

🤖 Auto-check every 6h
```

### **Failure Alert:**
```
🚨 VPN Accounts Down Alert

❌ 3 accounts failed:

• VLESS: Singapore-Primary (Timeout)
• TROJAN: Japan-Server-2 (Dead)
• SS: US-West-Coast (Failed)
```

## 🔧 **Advanced Usage**

### **Multiple Config Files:**
```json
{
  "config_file": "production-config.json"
  // Monitor specific config instead of template.json
}
```

### **Environment Variables:**
```bash
export GITHUB_TOKEN="ghp_token"
export GITHUB_OWNER="username"
export GITHUB_REPO="repo-name"
export TELEGRAM_TOKEN="bot_token"
export TELEGRAM_CHAT_ID="chat_id"
export CHECK_INTERVAL_HOURS="4"

python3 bot_vpn_checker.py
```

### **Different Check Intervals:**
- `1` = Every hour (intensive monitoring)
- `6` = Every 6 hours (recommended)
- `12` = Twice daily
- `24` = Daily checks

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **Bot Not Starting:**
```bash
❌ Missing required GitHub configuration
```
**Solution:** Check `github_token`, `github_owner`, `github_repo` in config

#### **No Notifications:**
```bash
❌ No notification method configured
```
**Solution:** Configure at least Telegram OR WhatsApp settings

#### **GitHub Access Failed:**
```bash
❌ Failed to load config: 401 Unauthorized
```
**Solution:** Update GitHub token (same as VortexVPN Manager)

#### **Telegram Failed:**
```bash
❌ Failed to send Telegram message
```
**Solution:** 
1. Check bot token format
2. Verify chat ID is number, not string
3. Ensure bot has been started (send any message first)

#### **WhatsApp Failed:**
```bash
❌ Failed to send WhatsApp message
```
**Solution:**
1. Join Twilio sandbox first
2. Check phone number format (+62812345678)
3. Verify Twilio credentials

### **Debug Mode:**
```bash
# See detailed logs
tail -f vpn_bot.log

# Manual single check
python3 -c "
import asyncio
from bot_vpn_checker import VPNBotChecker, load_bot_config
config = load_bot_config()
bot = VPNBotChecker(config)
asyncio.run(bot.run_check())
"
```

## 🚀 **Deployment Options**

### **Option 1: Local Machine**
```bash
# Run in background
nohup python3 bot_vpn_checker.py &
```

### **Option 2: VPS Server**
```bash
# Create systemd service
sudo nano /etc/systemd/system/vpn-bot.service

# Add systemd configuration
[Unit]
Description=VPN Bot Checker
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/vpn-bot
ExecStart=/usr/bin/python3 bot_vpn_checker.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable vpn-bot
sudo systemctl start vpn-bot
```

### **Option 3: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r bot_requirements.txt
CMD ["python3", "bot_vpn_checker.py"]
```

## 📈 **Usage Examples**

### **Personal Monitoring:**
- ⏰ **Check:** Every 6 hours
- 📱 **Notify:** Telegram personal chat
- 📊 **Mode:** Summary + failures

### **Team Monitoring:**
- ⏰ **Check:** Every 2 hours  
- 📱 **Notify:** Telegram group chat
- 🚨 **Mode:** Failures only (quiet)

### **Critical Infrastructure:**
- ⏰ **Check:** Every hour
- 📱 **Notify:** Both Telegram + WhatsApp
- 📊 **Mode:** Full reports + immediate alerts

## 🎯 **Next Steps**

1. **Setup bot** dengan configuration Anda
2. **Test notifications** manual
3. **Run first check** dan verify hasilnya
4. **Deploy** ke server untuk 24/7 monitoring
5. **Monitor logs** untuk performance optimization

Bot siap monitor VPN accounts Anda 24/7! 🎉