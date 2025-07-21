#!/usr/bin/env python3
"""
🧪 Bot VPN Checker Test Script
Manual testing script for bot functionality without scheduling.
"""

import asyncio
import json
import logging
from pathlib import Path

from bot_vpn_checker import VPNBotChecker, BotConfig, load_bot_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_single_check():
    """Test a single VPN check cycle"""
    try:
        # Load configuration
        config = load_bot_config()
        
        # Override for quick testing
        config.check_interval_minutes = 1  # Quick testing
        
        # Validate required config
        if not all([config.github_token, config.github_owner, config.github_repo]):
            logger.error("Missing required GitHub configuration!")
            logger.info("Please create bot_config.json from bot_config.json.example")
            return
        
        # Create bot instance
        bot = VPNBotChecker(config)
        
        # Test loading accounts from GitHub
        print("🔍 Testing GitHub connection and account loading...")
        accounts = await bot.load_accounts_from_github()
        
        if not accounts:
            print("❌ No accounts found or GitHub connection failed")
            return
        
        print(f"✅ Loaded {len(accounts)} accounts from GitHub")
        
        # Test VPN accounts
        print("🧪 Testing VPN accounts...")
        results = await bot.test_accounts(accounts)
        
        # Display results
        print("\n📊 Test Results:")
        print(f"✅ Working: {results['successful']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"📦 Total: {results['total']}")
        print(f"📈 Success Rate: {results['success_rate']:.1f}%")
        
        # Test message formatting
        print("\n📱 Sample Notification Message:")
        message = bot.format_summary_message(results)
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # Test notification (if configured)
        if config.telegram_token or config.twilio_account_sid:
            response = input("\n📤 Send test notification? (y/n): ")
            if response.lower() == 'y':
                await bot.send_notifications(message)
                print("✅ Test notification sent!")
        
        print("\n🎉 Manual test completed!")
        
    except Exception as e:
        logger.error(f"Test error: {str(e)}")

def test_config_loading():
    """Test configuration loading"""
    print("⚙️ Testing configuration loading...")
    
    config_file = Path("bot_config.json")
    if not config_file.exists():
        print("❌ bot_config.json not found")
        print("📝 Please copy bot_config.json.example to bot_config.json and configure it")
        return False
    
    try:
        config = load_bot_config()
        print("✅ Configuration loaded successfully")
        print(f"📁 GitHub Repo: {config.github_owner}/{config.github_repo}")
        print(f"📄 Config File: {config.config_file}")
        print(f"⏰ Check Interval: {config.check_interval_minutes} minutes")
        print(f"📱 Telegram: {'✅' if config.telegram_token else '❌'}")
        print(f"📱 WhatsApp: {'✅' if config.twilio_account_sid else '❌'}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🤖 VPN Bot Checker - Manual Test")
    print("=" * 40)
    
    # Test configuration
    if not test_config_loading():
        return
    
    print("\n" + "=" * 40)
    
    # Test single check
    await test_single_check()

if __name__ == "__main__":
    asyncio.run(main())