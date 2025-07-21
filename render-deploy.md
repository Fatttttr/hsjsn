# 🆓 Deploy VPN Bot ke Render.com (100% Free Forever)

Complete guide untuk deploy bot ke Render.com dengan **permanent free hosting**.

## 💰 Why Render.com?

- ✅ **100% FREE forever** (no credit cards)
- ✅ **750 hours/month** (enough untuk 24/7)
- ✅ **Auto-restart** when webhook triggered
- ⚠️ **Sleeps after 15min inactive** (acceptable untuk scheduled bots)
- ✅ **GitHub integration**

## 🚀 Step-by-Step Deployment

### **1. Prepare Bot untuk Render**

Bot sudah ready dengan:
- ✅ `Procfile` configured
- ✅ `bot_requirements.txt` dependencies
- ✅ Environment variables support

### **2. Setup Render Account**

1. **Go to:** https://render.com/
2. **Sign up** dengan GitHub account (FREE)
3. **No credit card required**
4. **Verify email**

### **3. Create Web Service**

1. **Click "New +"**
2. **Select "Web Service"**
3. **Connect GitHub repository**
4. **Choose:** `bot-vpn-checker` branch

### **4. Configure Service**

#### **Basic Settings:**
```
Name: vpn-bot-checker
Environment: Python 3
Region: Singapore (closest to Indonesia)
Branch: bot-vpn-checker
Build Command: pip install -r bot_requirements.txt
Start Command: python bot_vpn_checker.py
```

#### **Plan:**
```
Instance Type: Free ($0/month)
```

### **5. Environment Variables**

Add di Render dashboard:

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

### **6. Deploy & Monitor**

1. **Click "Create Web Service"**
2. **Wait for build completion** (~2-3 minutes)
3. **Check logs** untuk verify deployment
4. **Bot starts running!**

## 😴 Handling Sleep Mode (3 Solutions)

### **Solution 1: Accept Sleep (Simplest)**
- 🤖 **Bot runs normally** saat active
- 😴 **Sleeps after 15min** no HTTP requests
- ⏰ **Auto-wakes** when scheduled task triggers
- 🔄 **Continues monitoring** seamlessly
- ✅ **Works fine untuk 30min+ intervals**

### **Solution 2: Self-Ping Keep-Alive (Built-in)**
Bot automatically enabled jika deploy ke Render:
- 🔄 **Bot pings itself every 10 minutes**
- 🌐 **Health endpoint** available at `/health`
- ⚡ **Prevents sleep completely**
- 📊 **Zero additional setup required**

### **Solution 3: External Ping Services (Recommended)**
Use free monitoring services:
- 📡 **UptimeRobot** (free, 5min intervals) 
- 🕐 **Cron-job.org** (free, 1min intervals)
- 📈 **Pingdom** (free, 1min intervals)
- ✅ **Professional monitoring + keep awake**
- 🎁 **Bonus: uptime alerts & statistics**

#### **Quick UptimeRobot Setup:**
1. Sign up at https://uptimerobot.com/ (free)
2. Add monitor: `https://your-app.onrender.com/health`
3. Interval: 5 minutes
4. ✅ App stays awake + professional monitoring!

## 📊 Performance Comparison

| Feature | Railway ($3/month) | Render (FREE) |
|---------|-------------------|---------------|
| **Cost** | $2-3/month | $0/month |
| **Uptime** | 100% active | 99.9% (sleeps) |
| **Restart** | Auto | Auto |
| **Reliability** | Excellent | Very Good |
| **Setup** | Easy | Easy |

## ✅ Success Indicators

- ✅ **Service shows "Live"** di Render dashboard
- ✅ **Logs show** scheduled runs
- ✅ **Telegram/WhatsApp** receive notifications
- ✅ **No monthly bills!**

## 🔧 Monitoring

### **Render Dashboard:**
- **Service status:** Live/Building/Failed
- **Logs:** Real-time bot output
- **Metrics:** CPU/Memory usage
- **Events:** Deployment history

### **Bot Notifications:**
Bot akan continue send notifications as normal:
```
🔍 VPN Status Report - 16:30:15
✅ 55/55 accounts working (100%)
```

## 🎯 Recommendation

**Perfect untuk:**
- ✅ **Budget-conscious users**
- ✅ **Testing deployments**
- ✅ **Non-critical monitoring** (30min intervals acceptable)
- ✅ **Learning cloud deployment**

**Consider Railway jika:**
- 💼 **Production-critical monitoring**
- 💰 **Budget allows $3/month**
- 🚀 **Need guaranteed 100% uptime**

## 🆓 ULTIMATE FREE HOSTING SOLUTION

**Total monthly cost: $0.00**
**24/7 VPN monitoring: ✅**
**Professional cloud hosting: ✅**
**No credit card required: ✅**

Perfect untuk automated VPN monitoring tanpa monthly fees! 🚀