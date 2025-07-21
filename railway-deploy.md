# 🚀 Deploy VPN Bot ke Railway.app (24/7 Free Hosting)

Complete guide untuk deploy bot ke Railway dengan free hosting.

## 📋 Prerequisites

- ✅ Bot working di local (sudah tested)
- ✅ GitHub repository dengan bot code
- ✅ Valid Twilio + Telegram credentials

## 🚀 Step-by-Step Deployment

### **1. Prepare Bot untuk Production**

#### **Create requirements.txt:**
```
requests>=2.28.0
schedule>=1.2.0
pyTelegramBotAPI>=4.0.0
twilio>=8.0.0
python-dotenv>=1.0.0
aiohttp>=3.8.0
```

#### **Create Procfile:**
```
worker: python bot_vpn_checker.py
```

#### **Create railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot_vpn_checker.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **2. Setup Railway Account**

1. **Go to:** https://railway.app/
2. **Sign up** dengan GitHub account
3. **Verify email** 
4. **Get $5 free credit** (auto-applied)

### **3. Deploy dari GitHub**

1. **Click "New Project"**
2. **Select "Deploy from GitHub repo"**
3. **Choose your VPN bot repository**
4. **Select branch:** `bot-vpn-checker`
5. **Click "Deploy"**

### **4. Configure Environment Variables**

Di Railway dashboard:

1. **Go to Variables tab**
2. **Add environment variables:**

```
GITHUB_TOKEN=ghp_your_github_token
GITHUB_OWNER=Fatttttr
GITHUB_REPO=fattt
CHECK_INTERVAL_MINUTES=30
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+6281234567890
```

### **5. Update Bot untuk Environment Variables**

Bot akan load environment variables instead of config file.

### **6. Deploy & Monitor**

1. **Railway auto-builds** dari GitHub
2. **Check logs** untuk verify deployment
3. **Monitor** di Railway dashboard

## 💰 Cost Analysis

### **Railway Pricing:**
- **Free:** $5 credit/month
- **Bot usage:** ~$2-3/month (24/7 running)
- **Duration:** 1-2 months free, then ~$3/month

### **Alternative Free Options:**
- **Render:** 750 hours/month (bot sleeps)
- **PythonAnywhere:** Limited CPU seconds
- **VPS:** DigitalOcean $4/month (not free)

## 🔧 Monitoring & Maintenance

### **Check Deployment:**
1. **Railway dashboard** shows deployment status
2. **Logs tab** untuk troubleshooting
3. **Metrics tab** untuk usage monitoring

### **Auto-restart:**
Railway automatically restarts bot kalau crash.

### **Updates:**
Push ke GitHub → Railway auto-deploys.

## 📱 Telegram/WhatsApp Notifications

Bot akan continue send notifications as configured, now running 24/7 dari cloud!

## ✅ Success Indicators

- ✅ **Deployment successful** di Railway
- ✅ **Bot logs** show scheduled runs
- ✅ **Telegram/WhatsApp** receive notifications
- ✅ **No local computer** needed anymore

**Perfect 24/7 VPN monitoring dengan professional cloud hosting!** 🚀