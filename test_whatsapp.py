#!/usr/bin/env python3
"""
Test Twilio WhatsApp Integration
Usage: python test_whatsapp.py
"""

from twilio.rest import Client
import json

def test_twilio_whatsapp():
    """Test Twilio WhatsApp functionality"""
    
    print("🔧 Twilio WhatsApp Test")
    print("=" * 40)
    
    # Load config
    try:
        with open('bot_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ bot_config.json not found!")
        return
    
    # Get Twilio credentials
    account_sid = config.get('twilio_account_sid')
    auth_token = config.get('twilio_auth_token')
    whatsapp_from = config.get('twilio_whatsapp_from')
    whatsapp_to = config.get('whatsapp_to')
    
    if not all([account_sid, auth_token, whatsapp_from, whatsapp_to]):
        print("❌ Missing Twilio credentials in config!")
        print("Please set:")
        print("- twilio_account_sid")
        print("- twilio_auth_token") 
        print("- twilio_whatsapp_from")
        print("- whatsapp_to")
        return
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        print(f"✅ Twilio client initialized")
        print(f"📞 From: {whatsapp_from}")
        print(f"📱 To: {whatsapp_to}")
        
        # Test message
        test_message = """🤖 VPN Bot Test Message

🔍 This is a test from your VPN monitoring bot!

✅ Twilio WhatsApp integration is working correctly.

🚀 Your bot is ready for automated VPN status notifications!

📊 Next: Run bot_vpn_checker.py for real monitoring."""
        
        # Send WhatsApp message
        print(f"\n📤 Sending test message...")
        message = client.messages.create(
            body=test_message,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        
        print(f"✅ Message sent successfully!")
        print(f"📧 Message SID: {message.sid}")
        print(f"📊 Status: {message.status}")
        print(f"\n🎉 WhatsApp integration working! Check your WhatsApp.")
        
    except Exception as e:
        print(f"❌ Twilio error: {str(e)}")
        print("\n🔧 Common issues:")
        print("- Wrong Account SID or Auth Token")
        print("- WhatsApp number not joined to sandbox")
        print("- Invalid phone number format")
        print("- Insufficient Twilio balance")
        print("\n📋 Solutions:")
        print("1. Check credentials di Twilio Console")
        print("2. Send 'join <code>' ke +1 415 523 8886")
        print("3. Use format: whatsapp:+6281234567890")

if __name__ == "__main__":
    test_twilio_whatsapp()