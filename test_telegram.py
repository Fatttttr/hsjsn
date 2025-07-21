#!/usr/bin/env python3
"""
📱 Quick Telegram Bot Test Script
Test your Telegram bot token and chat ID before running the main bot.
"""

import requests
import json

def test_telegram_bot():
    """Test Telegram bot connection"""
    print("📱 Telegram Bot Test")
    print("=" * 30)
    
    # Get credentials from user
    bot_token = input("🤖 Masukkan Bot Token: ").strip()
    chat_id = input("💬 Masukkan Chat ID: ").strip()
    
    if not bot_token or not chat_id:
        print("❌ Token atau Chat ID tidak boleh kosong!")
        return
    
    # Test bot info
    print("\n🔍 Testing bot info...")
    try:
        bot_info_url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(bot_info_url)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot found: @{bot_info['username']}")
            print(f"📛 Bot name: {bot_info['first_name']}")
        else:
            print(f"❌ Bot error: {data.get('description', 'Unknown error')}")
            return
            
    except Exception as e:
        print(f"❌ Error checking bot: {str(e)}")
        return
    
    # Test send message
    print("\n📤 Testing send message...")
    try:
        message = "🧪 Test message from VPN Bot Checker!\n\nJika Anda menerima pesan ini, berarti konfigurasi Telegram bot sudah benar! ✅"
        
        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(send_url, data=data)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Test message sent successfully!")
            print("📱 Check your Telegram for the test message")
            
            # Show config format
            print("\n⚙️ Your bot_config.json format:")
            print("=" * 40)
            config_example = {
                "telegram_token": bot_token,
                "telegram_chat_id": chat_id
            }
            print(json.dumps(config_example, indent=2))
            print("=" * 40)
            
        else:
            print(f"❌ Failed to send message: {result.get('description', 'Unknown error')}")
            
            # Common error explanations
            error_desc = result.get('description', '').lower()
            if 'chat not found' in error_desc:
                print("\n💡 Solusi:")
                print("1. Pastikan sudah start bot di Telegram")
                print("2. Kirim pesan '/start' ke bot")
                print("3. Coba ambil Chat ID lagi")
            elif 'forbidden' in error_desc:
                print("\n💡 Solusi:")
                print("1. Unblock bot di Telegram")
                print("2. Start ulang bot")
                print("3. Pastikan bot masih aktif")
                
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")

def get_chat_id_helper():
    """Helper to get Chat ID"""
    print("\n💡 Cara mendapatkan Chat ID:")
    print("1. Start bot Anda di Telegram")
    print("2. Kirim pesan apa saja ke bot")
    print("3. Buka URL berikut di browser (ganti TOKEN):")
    
    token = input("\n🤖 Masukkan Bot Token untuk generate URL: ").strip()
    if token:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        print(f"\n📋 Copy URL ini ke browser:")
        print(f"🔗 {url}")
        print("\n4. Cari 'chat': {'id': XXXXXXXX} di response JSON")
        print("5. Copy angka XXXXXXXX sebagai Chat ID")

def main():
    """Main function"""
    while True:
        print("\n📱 Telegram Bot Setup Helper")
        print("1. Test Bot Token & Chat ID")
        print("2. Help: Cara dapat Chat ID") 
        print("3. Exit")
        
        choice = input("\nPilih (1/2/3): ").strip()
        
        if choice == '1':
            test_telegram_bot()
        elif choice == '2':
            get_chat_id_helper()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()