#!/usr/bin/env python3
"""
VPN Bot Checker - Auto check VPN accounts from GitHub repository
Supports WhatsApp & Telegram with scheduled monitoring
"""

import os
import json
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from dataclasses import dataclass

# Import existing VortexVPN logic
from github_client import GitHubClient
from core import test_all_accounts, ensure_ws_path_field, sort_priority
from extractor import extract_accounts_from_config

# Bot libraries (install as needed)
try:
    import telebot  # For Telegram: pip install pyTelegramBotAPI
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram support not available. Install: pip install pyTelegramBotAPI")

try:
    from twilio.rest import Client  # For WhatsApp: pip install twilio
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False
    print("⚠️ WhatsApp support not available. Install: pip install twilio")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vpn_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """Bot configuration"""
    # GitHub settings
    github_token: str
    github_owner: str
    github_repo: str
    config_file: str = "template.json"
    
    # Schedule settings
    check_interval_minutes: int = 5  # Check every 5 minutes (for testing)
    max_concurrent_tests: int = 5
    
    # Notification settings
    send_only_failures: bool = False  # True = only send failed accounts
    send_summary: bool = True         # Send summary after each check
    
    # Telegram settings (optional)
    telegram_token: str = ""
    telegram_chat_id: str = ""
    
    # WhatsApp settings (optional)
    twilio_sid: str = ""
    twilio_token: str = ""
    whatsapp_from: str = ""  # +14155238886 (Twilio sandbox)
    whatsapp_to: str = ""    # +62812345678

class VPNBotChecker:
    def __init__(self, config: BotConfig):
        self.config = config
        self.github_client = GitHubClient(
            config.github_token,
            config.github_owner, 
            config.github_repo
        )
        
        # Initialize bots
        self.telegram_bot = None
        self.whatsapp_client = None
        
        if TELEGRAM_AVAILABLE and config.telegram_token:
            self.telegram_bot = telebot.TeleBot(config.telegram_token)
            logger.info("📱 Telegram bot initialized")
        
        if WHATSAPP_AVAILABLE and config.twilio_sid:
            self.whatsapp_client = Client(config.twilio_sid, config.twilio_token)
            logger.info("📱 WhatsApp client initialized")
        
        self.last_check = None
        self.check_count = 0

    async def load_config_from_github(self) -> Dict[str, Any]:
        """Load VPN configuration from GitHub repository"""
        try:
            logger.info(f"📁 Loading config from GitHub: {self.config.config_file}")
            
            content, sha = self.github_client.get_file(self.config.config_file)
            if not content:
                raise Exception(f"Failed to load {self.config.config_file} from repository")
            
            config_data = json.loads(content)
            logger.info(f"✅ Config loaded successfully")
            return config_data
            
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            raise

    async def extract_and_test_accounts(self) -> Dict[str, Any]:
        """Extract accounts from config and test them"""
        try:
            # Load config from GitHub
            config_data = await self.load_config_from_github()
            
            # Extract accounts using existing logic
            accounts = extract_accounts_from_config(config_data)
            accounts = ensure_ws_path_field(accounts)
            
            if not accounts:
                return {
                    'success': False,
                    'message': 'No VPN accounts found in configuration',
                    'accounts': [],
                    'results': []
                }
            
            logger.info(f"🔍 Found {len(accounts)} VPN accounts to test")
            
            # Initialize test results
            live_results = []
            for i, acc in enumerate(accounts):
                result = {
                    "index": i,
                    "OriginalTag": acc.get("tag", f"Account-{i+1}"),
                    "OriginalAccount": acc,
                    "VpnType": acc.get("type", "unknown"),
                    "Country": "❓",
                    "Provider": "-",
                    "Tested IP": "-",
                    "Latency": -1,
                    "Jitter": -1,
                    "ICMP": "N/A",
                    "Status": "WAIT",
                    "Retry": 0
                }
                live_results.append(result)
            
            # Test accounts using existing logic
            semaphore = asyncio.Semaphore(self.config.max_concurrent_tests)
            await test_all_accounts(accounts, semaphore, live_results)
            
            # Count results
            successful = [r for r in live_results if r["Status"] == "✅"]
            failed = [r for r in live_results if r["Status"] not in ["✅", "WAIT"]]
            
            # Sort successful accounts by priority
            successful.sort(key=sort_priority)
            
            result = {
                'success': True,
                'total_accounts': len(accounts),
                'successful_count': len(successful),
                'failed_count': len(failed),
                'successful_accounts': successful,
                'failed_accounts': failed,
                'all_results': live_results,
                'check_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Testing complete: {len(successful)}/{len(accounts)} successful")
            return result
            
        except Exception as e:
            logger.error(f"❌ Testing failed: {e}")
            return {
                'success': False,
                'message': str(e),
                'accounts': [],
                'results': []
            }

    def format_summary_message(self, results: Dict[str, Any]) -> str:
        """Format test results as simple hidup/mati report"""
        if not results['success']:
            return f"❌ VPN Check Failed\n\nError: {results.get('message', 'Unknown error')}"
        
        check_time = datetime.now().strftime("%H:%M:%S")
        total = results['total_accounts']
        successful = results['successful_count']
        failed = results['failed_count']
        
        # Simple summary message
        summary = f"🔍 VPN Status Report - {check_time}\n\n"
        summary += f"✅ Akun Hidup: {successful}\n"
        summary += f"❌ Akun Mati: {failed}\n"
        summary += f"📦 Total: {total}\n\n"
        
        # Status overview
        if successful == total:
            summary += "🎉 Semua akun normal!"
        elif successful > 0:
            percentage = round((successful / total) * 100)
            summary += f"📊 {percentage}% akun masih berfungsi"
        else:
            summary += "🚨 Semua akun DOWN!"
        
        summary += f"\n\n🔄 Cek otomatis setiap {self.config.check_interval_minutes} menit"
        return summary

    def format_failed_accounts_message(self, failed_accounts: List[Dict]) -> str:
        """Format failed accounts message"""
        if not failed_accounts:
            return ""
        
        message = "🚨 VPN Accounts Down Alert\n\n"
        message += f"❌ {len(failed_accounts)} accounts failed:\n\n"
        
        for acc in failed_accounts[:10]:  # Max 10 failed accounts
            acc_type = acc.get('VpnType', 'unknown').upper()
            acc_tag = acc.get('OriginalTag', 'Unknown')
            status = acc.get('Status', 'Unknown')
            message += f"• {acc_type}: {acc_tag} ({status})\n"
        
        if len(failed_accounts) > 10:
            message += f"\n... and {len(failed_accounts) - 10} more accounts failed"
        
        return message

    async def send_telegram_message(self, message: str):
        """Send message via Telegram"""
        if not self.telegram_bot or not self.config.telegram_chat_id:
            return False
        
        try:
            # Split long messages
            max_length = 4000
            if len(message) > max_length:
                parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
                for part in parts:
                    self.telegram_bot.send_message(self.config.telegram_chat_id, part)
            else:
                self.telegram_bot.send_message(self.config.telegram_chat_id, message)
            
            logger.info("📱 Telegram message sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram message: {e}")
            return False

    async def send_whatsapp_message(self, message: str):
        """Send message via WhatsApp"""
        if not self.whatsapp_client or not self.config.whatsapp_to:
            return False
        
        try:
            # WhatsApp has message length limits
            max_length = 1500
            if len(message) > max_length:
                message = message[:max_length] + "\n\n... (message truncated)"
            
            self.whatsapp_client.messages.create(
                body=message,
                from_=self.config.whatsapp_from,
                to=self.config.whatsapp_to
            )
            
            logger.info("📱 WhatsApp message sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send WhatsApp message: {e}")
            return False

    async def send_notifications(self, results: Dict[str, Any]):
        """Send notifications via enabled platforms"""
        if not results['success']:
            error_msg = f"🚨 VPN Bot Error\n\n{results.get('message', 'Unknown error occurred')}"
            await self.send_telegram_message(error_msg)
            await self.send_whatsapp_message(error_msg)
            return
        
        # Send summary if enabled
        if self.config.send_summary:
            summary_msg = self.format_summary_message(results)
            await self.send_telegram_message(summary_msg)
            await self.send_whatsapp_message(summary_msg)
        
        # Send failed accounts alert if any
        if results['failed_count'] > 0 and not self.config.send_only_failures:
            failed_msg = self.format_failed_accounts_message(results['failed_accounts'])
            if failed_msg:
                await self.send_telegram_message(failed_msg)
                await self.send_whatsapp_message(failed_msg)
        
        # If send_only_failures is True, only send when there are failures
        if self.config.send_only_failures and results['failed_count'] > 0:
            failed_msg = self.format_failed_accounts_message(results['failed_accounts'])
            if failed_msg:
                await self.send_telegram_message(failed_msg)
                await self.send_whatsapp_message(failed_msg)

    async def run_check(self):
        """Run a single VPN check cycle"""
        try:
            self.check_count += 1
            logger.info(f"🚀 Starting VPN check #{self.check_count}")
            
            # Test all accounts
            results = await self.extract_and_test_accounts()
            
            # Send notifications
            await self.send_notifications(results)
            
            # Update last check time
            self.last_check = datetime.now()
            
            logger.info(f"✅ VPN check #{self.check_count} completed")
            
        except Exception as e:
            logger.error(f"❌ VPN check failed: {e}")
            error_msg = f"🚨 VPN Bot Error\n\nCheck #{self.check_count} failed: {str(e)}"
            await self.send_telegram_message(error_msg)
            await self.send_whatsapp_message(error_msg)

    def start_scheduler(self):
        """Start the automated scheduler"""
        logger.info(f"🤖 Starting VPN Bot Scheduler")
        logger.info(f"⏰ Check interval: {self.config.check_interval_minutes} minutes")
        logger.info(f"📁 Repository: {self.config.github_owner}/{self.config.github_repo}")
        logger.info(f"📄 Config file: {self.config.config_file}")
        
        # Schedule periodic checks (in minutes for testing)
        schedule.every(self.config.check_interval_minutes).minutes.do(
            lambda: asyncio.run(self.run_check())
        )
        
        # Run first check immediately
        asyncio.run(self.run_check())
        
        # Keep running (check every 30 seconds for scheduled tasks)
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds for scheduled tasks

def load_bot_config() -> BotConfig:
    """Load bot configuration from environment or config file"""
    config_file = "bot_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return BotConfig(
            github_token=config_data.get('github_token', ''),
            github_owner=config_data.get('github_owner', ''),
            github_repo=config_data.get('github_repo', ''),
            config_file=config_data.get('config_file', 'template.json'),
            check_interval_minutes=config_data.get('check_interval_minutes', 5),
            max_concurrent_tests=config_data.get('max_concurrent_tests', 5),
            send_only_failures=config_data.get('send_only_failures', False),
            send_summary=config_data.get('send_summary', True),
            telegram_token=config_data.get('telegram_token', ''),
            telegram_chat_id=config_data.get('telegram_chat_id', ''),
            twilio_sid=config_data.get('twilio_sid', ''),
            twilio_token=config_data.get('twilio_token', ''),
            whatsapp_from=config_data.get('whatsapp_from', ''),
            whatsapp_to=config_data.get('whatsapp_to', '')
        )
    
    # Fallback to environment variables
    return BotConfig(
        github_token=os.getenv('GITHUB_TOKEN', ''),
        github_owner=os.getenv('GITHUB_OWNER', ''),
        github_repo=os.getenv('GITHUB_REPO', ''),
        config_file=os.getenv('CONFIG_FILE', 'template.json'),
        check_interval_minutes=int(os.getenv('CHECK_INTERVAL_MINUTES', '5')),
        max_concurrent_tests=int(os.getenv('MAX_CONCURRENT_TESTS', '5')),
        send_only_failures=os.getenv('SEND_ONLY_FAILURES', 'false').lower() == 'true',
        send_summary=os.getenv('SEND_SUMMARY', 'true').lower() == 'true',
        telegram_token=os.getenv('TELEGRAM_TOKEN', ''),
        telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID', ''),
        twilio_sid=os.getenv('TWILIO_SID', ''),
        twilio_token=os.getenv('TWILIO_TOKEN', ''),
        whatsapp_from=os.getenv('WHATSAPP_FROM', ''),
        whatsapp_to=os.getenv('WHATSAPP_TO', '')
    )

if __name__ == "__main__":
    print("🤖 VPN Bot Checker - Auto VPN Account Monitor")
    print("=" * 50)
    
    try:
        # Load configuration
        config = load_bot_config()
        
        # Validate required settings
        if not all([config.github_token, config.github_owner, config.github_repo]):
            print("❌ Missing required GitHub configuration")
            print("Please set: github_token, github_owner, github_repo")
            exit(1)
        
        if not config.telegram_token and not config.twilio_sid:
            print("❌ No notification method configured")
            print("Please configure Telegram or WhatsApp settings")
            exit(1)
        
        # Create and start bot
        bot = VPNBotChecker(config)
        bot.start_scheduler()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        logger.error(f"Bot startup failed: {e}")