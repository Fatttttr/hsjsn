#!/usr/bin/env python3
"""
Test script untuk VPN Bot Checker
"""

import asyncio
import json
from bot_vpn_checker import VPNBotChecker, BotConfig

def create_test_config():
    """Create test configuration"""
    # Load from file if exists, otherwise create minimal config
    try:
        with open('bot_config.json', 'r') as f:
            config_data = json.load(f)
        
        config = BotConfig(
            github_token=config_data.get('github_token', ''),
            github_owner=config_data.get('github_owner', ''),
            github_repo=config_data.get('github_repo', ''),
            config_file=config_data.get('config_file', 'template.json'),
            check_interval_minutes=1,  # Test every 1 minute
            max_concurrent_tests=config_data.get('max_concurrent_tests', 3),
            send_only_failures=False,
            send_summary=True,
            telegram_token=config_data.get('telegram_token', ''),
            telegram_chat_id=config_data.get('telegram_chat_id', ''),
            twilio_sid=config_data.get('twilio_sid', ''),
            twilio_token=config_data.get('twilio_token', ''),
            whatsapp_from=config_data.get('whatsapp_from', ''),
            whatsapp_to=config_data.get('whatsapp_to', '')
        )
        
        return config
        
    except FileNotFoundError:
        print("❌ bot_config.json not found")
        print("Please copy bot_config.json.example to bot_config.json and configure it")
        return None

async def test_single_check():
    """Test single VPN check"""
    print("🧪 Testing Single VPN Check")
    print("=" * 40)
    
    config = create_test_config()
    if not config:
        return
    
    if not all([config.github_token, config.github_owner, config.github_repo]):
        print("❌ Missing GitHub configuration")
        print("Please configure github_token, github_owner, github_repo in bot_config.json")
        return
    
    bot = VPNBotChecker(config)
    
    try:
        print("🚀 Starting single check...")
        await bot.run_check()
        print("✅ Single check completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_message_formatting():
    """Test message formatting"""
    print("\n🧪 Testing Message Formatting")
    print("=" * 40)
    
    config = create_test_config()
    if not config:
        return
    
    bot = VPNBotChecker(config)
    
    # Test data
    test_results = {
        'success': True,
        'total_accounts': 10,
        'successful_count': 7,
        'failed_count': 3,
        'successful_accounts': [],
        'failed_accounts': []
    }
    
    message = bot.format_summary_message(test_results)
    print("📱 Test Message Output:")
    print("-" * 30)
    print(message)
    print("-" * 30)

async def main():
    """Main test function"""
    print("🤖 VPN Bot Checker - Test Mode")
    print("=" * 50)
    
    # Test message formatting first
    test_message_formatting()
    
    # Test single check
    await test_single_check()
    
    print("\n✅ All tests completed!")
    print("\nTo run the actual bot:")
    print("python3 bot_vpn_checker.py")

if __name__ == "__main__":
    asyncio.run(main())