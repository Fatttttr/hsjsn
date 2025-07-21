# 📱 WhatsApp Setup Guide (Twilio)

Complete guide untuk setup WhatsApp notifications melalui Twilio.

## 🚀 Step-by-Step Setup

### **1. Daftar Twilio Account**

1. **Visit:** https://www.twilio.com/
2. **Click:** "Start building for free"
3. **Sign up** dengan email dan password
4. **Verify** phone number Anda
5. **Get $15 free credit** untuk testing

### **2. Get Twilio Credentials**

1. **Login ke Twilio Console:** https://console.twilio.com/
2. **Di dashboard, copy:**
   - **Account SID**: `ACxxxxxxxxxxxxxxxx...` (starts with AC)
   - **Auth Token**: Click "show" untuk reveal token

### **3. Setup WhatsApp Sandbox**

1. **Go to:** Console → Develop → Messaging → Try it out → Send a WhatsApp message
2. **Atau direct:** https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

3. **Your Twilio WhatsApp number:** `+1 415 523 8886`
4. **Your sandbox code:** Example: `join early-frog`

5. **Send WhatsApp message:**
   ```
   To: +1 415 523 8886
   Message: join early-frog
   ```

6. **✅ You should receive:** "Connected to sandbox"

### **4. Update bot_config.json**

```json
{
  "twilio_account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "twilio_auth_token": "your_twilio_auth_token_here",
  "twilio_whatsapp_from": "whatsapp:+14155238886",
  "whatsapp_to": "whatsapp:+6281234567890"
}
```

**Important Notes:**
- `twilio_whatsapp_from`: Always `whatsapp:+14155238886` (Twilio's number)
- `whatsapp_to`: Your WhatsApp number dengan format `whatsapp:+country_code_number`
- No spaces in phone number!

### **5. Test WhatsApp Integration**

```bash
python test_whatsapp.py
```

**Expected output:**
```
🔧 Twilio WhatsApp Test
✅ Twilio client initialized
📞 From: whatsapp:+14155238886
📱 To: whatsapp:+6281234567890
📤 Sending test message...
✅ Message sent successfully!
```

### **6. Run Bot with WhatsApp**

```bash
python bot_vpn_checker.py
```

Bot akan send notifications ke **both** Telegram and WhatsApp!

## 📱 WhatsApp Number Format Examples

| Country | Phone Number | WhatsApp Format |
|---------|--------------|-----------------|
| Indonesia | 081234567890 | `whatsapp:+6281234567890` |
| Malaysia | 0123456789 | `whatsapp:+60123456789` |
| Singapore | 91234567 | `whatsapp:+6591234567` |
| USA | (555) 123-4567 | `whatsapp:+15551234567` |

## 🔧 Troubleshooting

### **Common Errors:**

**❌ "The number +6281234567890 is unverified"**
- Solution: Send `join <code>` message to Twilio sandbox

**❌ "Authentication Error"**
- Solution: Check Account SID and Auth Token

**❌ "Invalid 'To' number"**
- Solution: Use correct format `whatsapp:+country_code_number`

**❌ "Insufficient balance"**
- Solution: Add credit to Twilio account ($10 minimum)

### **Sandbox Limitations:**

- ✅ **Free testing** untuk joined numbers
- ❌ **Limited to verified numbers** only
- ⚠️ **For production:** Need Twilio phone number ($1/month)

### **Production Setup:**

For production WhatsApp (unlimited numbers):
1. **Buy Twilio phone number** ($1/month)
2. **Request WhatsApp approval** from Twilio
3. **Update configuration** dengan your Twilio number

## 💰 Pricing

- **Sandbox:** Free (untuk testing)
- **WhatsApp messages:** $0.005 per message
- **Phone number:** $1/month
- **Free credit:** $15 untuk new accounts

## ✅ Verification

After setup, your bot will send status reports like:

**WhatsApp Message:**
```
🔍 VPN Status Report - 16:30:15

✅ **testing.json**
   Hidup: 50 | Mati: 0 | Total: 50
   Status: 100% berfungsi
   Countries: 🇦🇹 🇦🇺 🇩🇪 🇪🇪 🇫🇮

📊 **RINGKASAN TOTAL**
✅ Total Hidup: 55
❌ Total Mati: 0  
📦 Total Akun: 55
📈 Success Rate: 100%

🔄 Cek otomatis setiap 30 menit
```

**Perfect dual notification system!** 🚀