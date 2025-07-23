#!/usr/bin/env python3
"""
🤖 VPN Bot Checker - Telegram Only Version
Simplified bot tanpa Twilio/WhatsApp - hanya Telegram notifications.
Optimized untuk Android/mobile data usage.
"""

import asyncio
import json
import logging
import os
import schedule
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

import requests
from telebot import TeleBot

from core import GitHubClient, VPNTester, extract_vpn_accounts, ensure_ws_path_field

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """Simple bot configuration for Telegram-only version"""
    github_token: str
    github_owner: str
    github_repo: str
    check_interval_minutes: int = 60
    max_concurrent_tests: int = 3
    timeout_seconds: int = 8
    send_only_failures: bool = False
    send_summary: bool = True
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

class TelegramVPNBot:
    """Simplified VPN Bot with Telegram-only notifications"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        
        # Initialize GitHub client
        self.github_client = GitHubClient(
            token=config.github_token,
            owner=config.github_owner,
            repo=config.github_repo
        )
        
        # Initialize Telegram bot
        self.telegram_bot = None
        if config.telegram_token:
            self.telegram_bot = TeleBot(config.telegram_token)
            logger.info("✅ Telegram bot initialized")
        else:
            logger.warning("⚠️ No Telegram token provided")
    
    async def load_all_configs_from_github(self) -> Dict[str, List[str]]:
        """Load VPN accounts from all JSON files in GitHub repository"""
        try:
            logger.info("🔍 Loading JSON config files from GitHub...")
            
            # Get list of JSON files from repository
            files = self.github_client.list_files_in_repo()
            json_files = [f['name'] for f in files if f.get('name', '').endswith('.json')]
            
            if not json_files:
                logger.warning("⚠️ No JSON files found in repository")
                return {}
            
            logger.info(f"📁 Found {len(json_files)} JSON files: {json_files}")
            all_configs = {}
            
            for filename in json_files:
                try:
                    logger.info(f"📄 Loading config from: {filename}")
                    
                    # Get file content from GitHub
                    file_content, file_sha = self.github_client.get_file(filename)
                    if not file_content:
                        logger.error(f"❌ Failed to load {filename} from GitHub")
                        continue
                    
                    # Parse JSON content
                    config_data = json.loads(file_content)
                    
                    # Extract VPN accounts
                    accounts = extract_vpn_accounts(config_data)
                    
                    if accounts:
                        # Apply preprocessing
                        accounts = ensure_ws_path_field(accounts)
                        all_configs[filename] = accounts
                        logger.info(f"✅ Loaded {len(accounts)} accounts from {filename}")
                    else:
                        logger.warning(f"⚠️ No VPN accounts found in {filename}")
                        
                except Exception as e:
                    logger.error(f"❌ Error loading {filename}: {str(e)}")
                    continue
            
            total_accounts = sum(len(accounts) for accounts in all_configs.values())
            logger.info(f"📊 Total loaded: {total_accounts} accounts from {len(all_configs)} files")
            return all_configs
            
        except Exception as e:
            logger.error(f"❌ Error loading configs from GitHub: {str(e)}")
            return {}
    
    async def test_accounts_by_file(self, configs_by_file: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """Test VPN accounts grouped by file"""
        if not configs_by_file:
            logger.warning("⚠️ No configs to test")
            return {}
        
        file_results = {}
        tester = VPNTester(
            max_concurrent=self.config.max_concurrent_tests,
            timeout=self.config.timeout_seconds
        )
        
        for filename, accounts in configs_by_file.items():
            logger.info(f"🧪 Testing {len(accounts)} accounts from {filename}...")
            
            # Test accounts for this file
            results = await tester.test_accounts(accounts)
            
            # Count results
            successful = len([r for r in results if r.is_working])
            failed = len([r for r in results if not r.is_working])
            total = len(results)
            success_rate = (successful / total * 100) if total > 0 else 0
            
            # Extract countries
            countries = set()
            for result in results:
                if result.is_working and result.country:
                    countries.add(result.country)
            
            file_results[filename] = {
                'successful': successful,
                'failed': failed,
                'total': total,
                'success_rate': success_rate,
                'countries': sorted(list(countries)),
                'test_time': datetime.now().strftime('%H:%M:%S'),
                'results': results
            }
            
            logger.info(f"📊 {filename}: {successful}/{total} working ({success_rate:.1f}%)")
        
        return file_results
    
    def format_telegram_message(self, file_results: Dict[str, Dict[str, Any]]) -> str:
        """Format summary message for Telegram"""
        if not file_results:
            return "❌ Tidak ada file config yang berhasil dimuat"
        
        check_time = datetime.now().strftime('%H:%M:%S')
        message = f"🔍 *VPN Status Report* - {check_time}\n\n"
        
        total_successful = 0
        total_failed = 0
        total_accounts = 0
        
        # Per-file breakdown
        for filename, results in file_results.items():
            successful = results['successful']
            failed = results['failed']
            total = results['total']
            success_rate = results['success_rate']
            countries = results['countries']
            
            # Status emoji based on success rate
            if success_rate >= 80:
                status_emoji = "✅"
            elif success_rate >= 50:
                status_emoji = "⚠️"
            else:
                status_emoji = "❌"
            
            message += f"{status_emoji} *{filename}*\n"
            message += f"   Hidup: {successful} | Mati: {failed} | Total: {total}\n"
            message += f"   Status: {success_rate:.0f}% berfungsi\n"
            
            # Add countries if available
            if countries:
                country_flags = []
                for country in countries[:5]:  # Show max 5 countries
                    flag = self.get_country_flag(country)
                    if flag:
                        country_flags.append(flag)
                
                if country_flags:
                    message += f"   Countries: {' '.join(country_flags)}\n"
            
            message += "\n"
            
            total_successful += successful
            total_failed += failed
            total_accounts += total
        
        # Overall summary
        overall_rate = (total_successful / total_accounts * 100) if total_accounts > 0 else 0
        
        message += f"📊 *RINGKASAN TOTAL*\n"
        message += f"✅ Total Hidup: {total_successful}\n"
        message += f"❌ Total Mati: {total_failed}\n"
        message += f"📦 Total Akun: {total_accounts}\n"
        message += f"📈 Success Rate: {overall_rate:.0f}%\n\n"
        
        message += f"🔄 Cek otomatis setiap {self.config.check_interval_minutes} menit"
        
        return message
    
    def get_country_flag(self, country: str) -> str:
        """Get country flag emoji"""
        flags = {
            'Indonesia': '🇮🇩', 'Singapore': '🇸🇬', 'Malaysia': '🇲🇾',
            'Thailand': '🇹🇭', 'Philippines': '🇵🇭', 'Vietnam': '🇻🇳',
            'United States': '🇺🇸', 'Canada': '🇨🇦', 'United Kingdom': '🇬🇧',
            'Germany': '🇩🇪', 'France': '🇫🇷', 'Netherlands': '🇳🇱',
            'Japan': '🇯🇵', 'South Korea': '🇰🇷', 'Australia': '🇦🇺',
            'India': '🇮🇳', 'China': '🇨🇳', 'Hong Kong': '🇭🇰',
            'Taiwan': '🇹🇼', 'Brazil': '🇧🇷', 'Argentina': '🇦🇷',
            'Mexico': '🇲🇽', 'Russia': '🇷🇺', 'Turkey': '🇹🇷',
            'Sweden': '🇸🇪', 'Norway': '🇳🇴', 'Finland': '🇫🇮',
            'Denmark': '🇩🇰', 'Switzerland': '🇨🇭', 'Austria': '🇦🇹',
            'Belgium': '🇧🇪', 'Italy': '🇮🇹', 'Spain': '🇪🇸',
            'Poland': '🇵🇱', 'Czech Republic': '🇨🇿', 'Hungary': '🇭🇺',
            'Romania': '🇷🇴', 'Bulgaria': '🇧🇬', 'Croatia': '🇭🇷',
            'Ukraine': '🇺🇦', 'Estonia': '🇪🇪', 'Latvia': '🇱🇻',
            'Lithuania': '🇱🇹', 'Slovakia': '🇸🇰', 'Slovenia': '🇸🇮',
            'South Africa': '🇿🇦', 'Egypt': '🇪🇬', 'Israel': '🇮🇱',
            'UAE': '🇦🇪', 'Saudi Arabia': '🇸🇦', 'New Zealand': '🇳🇿'
        }
        return flags.get(country, '🌍')
    
    def send_telegram_message(self, message: str):
        """Send message to Telegram"""
        if not self.telegram_bot or not self.config.telegram_chat_id:
            logger.warning("⚠️ Telegram not configured, skipping notification")
            return
        
        try:
            # Split long messages if needed
            max_length = 4000
            if len(message) <= max_length:
                self.telegram_bot.send_message(
                    chat_id=self.config.telegram_chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                logger.info("✅ Telegram message sent successfully")
            else:
                # Split into chunks
                chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
                for i, chunk in enumerate(chunks):
                    if i > 0:
                        time.sleep(1)  # Avoid rate limiting
                    self.telegram_bot.send_message(
                        chat_id=self.config.telegram_chat_id,
                        text=chunk,
                        parse_mode='Markdown'
                    )
                logger.info(f"✅ Telegram message sent in {len(chunks)} parts")
                
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram message: {str(e)}")
    
    async def run_check(self):
        """Run a complete VPN check cycle"""
        try:
            logger.info("🚀 Starting VPN check cycle...")
            
            # Load configs from GitHub
            configs = await self.load_all_configs_from_github()
            if not configs:
                logger.warning("⚠️ No configs loaded, skipping check")
                return
            
            # Test accounts by file
            results = await self.test_accounts_by_file(configs)
            if not results:
                logger.warning("⚠️ No test results, skipping notification")
                return
            
            # Send summary
            if self.config.send_summary:
                message = self.format_telegram_message(results)
                self.send_telegram_message(message)
            
            # Count totals
            total_successful = sum(r['successful'] for r in results.values())
            total_accounts = sum(r['total'] for r in results.values())
            
            logger.info(f"✅ Check completed: {total_successful}/{total_accounts} accounts working across {len(results)} files")
            
        except Exception as e:
            logger.error(f"❌ Error during check cycle: {str(e)}")
            
            # Send error notification
            error_message = f"❌ *VPN Bot Error*\n\n`{str(e)}`\n\nBot will retry pada check berikutnya."
            self.send_telegram_message(error_message)
    
    def start_scheduler(self):
        """Start the scheduled checking"""
        logger.info(f"🤖 Starting Telegram-only VPN Bot with {self.config.check_interval_minutes} minute intervals")
        
        # Schedule the check
        schedule.every(self.config.check_interval_minutes).minutes.do(
            lambda: asyncio.run(self.run_check())
        )
        
        logger.info("📅 Bot scheduler started. Press Ctrl+C to stop.")
        
        # Run initial check
        asyncio.run(self.run_check())
        
        # Keep running scheduled checks
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds for scheduled tasks
        except KeyboardInterrupt:
            logger.info("👋 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Scheduler error: {str(e)}")
            raise

def load_bot_config() -> BotConfig:
    """Load bot configuration from file or environment variables"""
    
    # Try environment variables first (for cloud deployment)
    if os.getenv('GITHUB_TOKEN'):
        logger.info("🔧 Loading configuration from environment variables")
        return BotConfig(
            github_token=os.getenv('GITHUB_TOKEN'),
            github_owner=os.getenv('GITHUB_OWNER'),
            github_repo=os.getenv('GITHUB_REPO'),
            check_interval_minutes=int(os.getenv('CHECK_INTERVAL_MINUTES', '60')),
            max_concurrent_tests=int(os.getenv('MAX_CONCURRENT_TESTS', '3')),
            timeout_seconds=int(os.getenv('TIMEOUT_SECONDS', '8')),
            send_only_failures=os.getenv('SEND_ONLY_FAILURES', 'false').lower() == 'true',
            send_summary=os.getenv('SEND_SUMMARY', 'true').lower() == 'true',
            telegram_token=os.getenv('TELEGRAM_TOKEN'),
            telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID')
        )
    
    # Fallback to config file (for local development)
    config_file = Path("config.json")
    if config_file.exists():
        logger.info("🔧 Loading configuration from config.json")
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return BotConfig(
            github_token=config_data.get('github_token'),
            github_owner=config_data.get('github_owner'),
            github_repo=config_data.get('github_repo'),
            check_interval_minutes=config_data.get('check_interval_minutes', 60),
            max_concurrent_tests=config_data.get('max_concurrent_tests', 3),
            timeout_seconds=config_data.get('timeout_seconds', 8),
            send_only_failures=config_data.get('send_only_failures', False),
            send_summary=config_data.get('send_summary', True),
            telegram_token=config_data.get('telegram_token'),
            telegram_chat_id=config_data.get('telegram_chat_id')
        )
    else:
        raise FileNotFoundError("❌ No configuration found. Please set environment variables or create config.json")

def main():
    """Main function to start the bot"""
    try:
        # Load configuration
        config = load_bot_config()
        
        # Validate required config
        if not all([config.github_token, config.github_owner, config.github_repo]):
            logger.error("❌ Missing required GitHub configuration!")
            return
        
        if not config.telegram_token or not config.telegram_chat_id:
            logger.error("❌ Missing required Telegram configuration!")
            return
        
        # Create and start bot
        bot = TelegramVPNBot(config)
        bot.start_scheduler()
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {str(e)}")

if __name__ == "__main__":
    main()