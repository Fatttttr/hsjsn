#!/usr/bin/env python3
"""
🤖 VPN Bot Checker
Automated VPN account monitoring bot for Telegram/WhatsApp notifications.

This bot monitors VPN accounts from a GitHub repository and sends simple
live/dead status reports at scheduled intervals.
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
from twilio.rest import Client as TwilioClient

# Import VPN testing modules
from core import GitHubClient, VPNTester, extract_vpn_accounts, ensure_ws_path_field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """Bot configuration settings"""
    # GitHub settings
    github_token: str
    github_owner: str
    github_repo: str
    
    # Testing settings
    check_interval_minutes: int = 5
    max_concurrent_tests: int = 5
    timeout_seconds: int = 10
    
    # Notification settings
    send_only_failures: bool = False
    send_summary: bool = True
    
    # Telegram settings (optional)
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    # WhatsApp settings (optional)
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_from: Optional[str] = None
    whatsapp_to: Optional[str] = None

class VPNBotChecker:
    """Main bot class for automated VPN monitoring"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.github_client = GitHubClient(
            token=config.github_token,
            owner=config.github_owner,
            repo=config.github_repo
        )
        
        # Initialize notification clients
        self.telegram_bot = None
        self.twilio_client = None
        
        if config.telegram_token:
            self.telegram_bot = TeleBot(config.telegram_token)
            
        if config.twilio_account_sid and config.twilio_auth_token:
            self.twilio_client = TwilioClient(
                config.twilio_account_sid,
                config.twilio_auth_token
            )
    
    async def load_all_configs_from_github(self) -> Dict[str, List[str]]:
        """Load VPN accounts from all JSON files in GitHub repository"""
        try:
            logger.info("Loading all JSON config files from GitHub repository...")
            
            # Get list of JSON files from repository
            files = self.github_client.list_files_in_repo()
            json_files = [f['name'] for f in files if f.get('name', '').endswith('.json')]
            
            if not json_files:
                logger.warning("No JSON files found in repository")
                return {}
            
            all_configs = {}
            
            for filename in json_files:
                try:
                    logger.info(f"Loading config from: {filename}")
                    
                    # Get file content from GitHub
                    file_content, file_sha = self.github_client.get_file(filename)
                    if not file_content:
                        logger.error(f"Failed to load {filename} from GitHub")
                        continue
                    
                    # Parse JSON content
                    config_data = json.loads(file_content)
                    
                    # Extract VPN accounts using the same logic as VortexVPN Manager
                    accounts = extract_vpn_accounts(config_data)
                    
                    if accounts:
                        # Apply same preprocessing as main branch
                        accounts = ensure_ws_path_field(accounts)
                        all_configs[filename] = accounts
                        logger.info(f"Loaded {len(accounts)} VPN accounts from {filename}")
                    else:
                        logger.warning(f"No VPN accounts found in {filename}")
                        
                except Exception as e:
                    logger.error(f"Error loading {filename}: {str(e)}")
                    continue
            
            total_accounts = sum(len(accounts) for accounts in all_configs.values())
            logger.info(f"Total loaded: {total_accounts} accounts from {len(all_configs)} config files")
            
            return all_configs
            
        except Exception as e:
            logger.error(f"Error loading configs from GitHub: {str(e)}")
            return {}
    
    async def test_accounts_by_file(self, all_configs: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """Test VPN accounts grouped by config file"""
        if not all_configs:
            return {}
        
        file_results = {}
        tester = VPNTester(
            max_concurrent=self.config.max_concurrent_tests,
            timeout=self.config.timeout_seconds
        )
        
        for filename, accounts in all_configs.items():
            if not accounts:
                file_results[filename] = {
                    'successful': 0,
                    'failed': 0,
                    'total': 0,
                    'success_rate': 0.0,
                    'test_time': datetime.now().strftime('%H:%M:%S')
                }
                continue
            
            logger.info(f"Testing {len(accounts)} accounts from {filename}...")
            
            # Test accounts concurrently
            results = await tester.test_multiple_accounts(accounts)
            
            # Count successful and failed tests
            successful = sum(1 for result in results if result.is_working)
            failed = len(results) - successful
            total = len(results)
            success_rate = (successful / total * 100) if total > 0 else 0.0
            
            file_results[filename] = {
                'successful': successful,
                'failed': failed,
                'total': total,
                'success_rate': success_rate,
                'test_time': datetime.now().strftime('%H:%M:%S'),
                'results': results
            }
            
            logger.info(f"{filename}: {successful}/{total} accounts working ({success_rate:.1f}%)")
        
        return file_results
    
    def format_summary_message(self, file_results: Dict[str, Dict[str, Any]]) -> str:
        """Format summary message with per-file results"""
        if not file_results:
            return "❌ No config files found or all failed to load"
        
        check_time = datetime.now().strftime('%H:%M:%S')
        summary = f"🔍 VPN Status Report - {check_time}\n\n"
        
        total_successful = 0
        total_failed = 0
        total_accounts = 0
        
        # Per-file breakdown
        for filename, results in file_results.items():
            successful = results['successful']
            failed = results['failed']
            total = results['total']
            success_rate = results['success_rate']
            
            # Accumulate totals
            total_successful += successful
            total_failed += failed
            total_accounts += total
            
            # File status with emoji indicator and details like main branch
            if total > 0:
                status_emoji = "✅" if success_rate >= 70 else "⚠️" if success_rate >= 30 else "❌"
                summary += f"{status_emoji} **{filename}**\n"
                summary += f"   Hidup: {successful} | Mati: {failed} | Total: {total}\n"
                summary += f"   Status: {success_rate:.0f}% berfungsi\n"
                
                # Add country info like main branch (if available)
                countries = set()
                for result in results.get('results', []):
                    if hasattr(result, 'country') and result.country != '❓':
                        countries.add(result.country)
                if countries:
                    country_list = ' '.join(sorted(countries)[:5])  # Show up to 5 countries
                    summary += f"   Countries: {country_list}\n"
                summary += "\n"
            else:
                summary += f"❌ **{filename}**\n"
                summary += f"   No accounts found\n\n"
        
        # Overall summary
        if total_accounts > 0:
            overall_rate = (total_successful / total_accounts * 100)
            summary += f"📊 **RINGKASAN TOTAL**\n"
            summary += f"✅ Total Hidup: {total_successful}\n"
            summary += f"❌ Total Mati: {total_failed}\n"
            summary += f"📦 Total Akun: {total_accounts}\n"
            summary += f"📈 Success Rate: {overall_rate:.0f}%\n\n"
        
        summary += f"🔄 Cek otomatis setiap {self.config.check_interval_minutes} menit"
        
        return summary
    
    async def send_telegram_notification(self, message: str):
        """Send notification via Telegram"""
        if not self.telegram_bot or not self.config.telegram_chat_id:
            return
            
        try:
            self.telegram_bot.send_message(
                chat_id=self.config.telegram_chat_id,
                text=message,
                parse_mode='HTML'
            )
            logger.info("Telegram notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {str(e)}")
    
    async def send_whatsapp_notification(self, message: str):
        """Send notification via WhatsApp"""
        if not self.twilio_client or not self.config.whatsapp_to:
            return
            
        try:
            self.twilio_client.messages.create(
                from_=self.config.twilio_whatsapp_from,
                to=self.config.whatsapp_to,
                body=message
            )
            logger.info("WhatsApp notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp notification: {str(e)}")
    
    async def send_notifications(self, message: str):
        """Send notifications to all configured platforms"""
        await asyncio.gather(
            self.send_telegram_notification(message),
            self.send_whatsapp_notification(message),
            return_exceptions=True
        )
    
    async def run_check(self):
        """Run a single VPN check cycle"""
        try:
            logger.info("Starting VPN check cycle...")
            
            # Load all config files from GitHub
            all_configs = await self.load_all_configs_from_github()
            
            if not all_configs:
                logger.warning("No config files found or all failed to load")
                return
            
            # Test accounts by file
            file_results = await self.test_accounts_by_file(all_configs)
            
            # Format and send summary message
            if self.config.send_summary:
                summary_message = self.format_summary_message(file_results)
                await self.send_notifications(summary_message)
            
            # Log summary
            total_successful = sum(r['successful'] for r in file_results.values())
            total_accounts = sum(r['total'] for r in file_results.values())
            logger.info(f"Check completed: {total_successful}/{total_accounts} total accounts working across {len(file_results)} files")
            
        except Exception as e:
            logger.error(f"Error during check cycle: {str(e)}")
    
    def start_scheduler(self):
        """Start the scheduled checking"""
        logger.info(f"Starting VPN Bot Checker with {self.config.check_interval_minutes} minute intervals")
        
        # Schedule the check
        schedule.every(self.config.check_interval_minutes).minutes.do(
            lambda: asyncio.run(self.run_check())
        )
        
        logger.info("Bot scheduler started. Press Ctrl+C to stop.")
        
        # Run initial check
        asyncio.run(self.run_check())
        
        # Keep running scheduled checks
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds for scheduled tasks

def load_bot_config() -> BotConfig:
    """Load bot configuration from file or environment variables"""
    config_file = Path("bot_config.json")
    
    if config_file.exists():
        # Load from config file
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return BotConfig(
            github_token=config_data.get('github_token'),
            github_owner=config_data.get('github_owner'),
            github_repo=config_data.get('github_repo'),
            check_interval_minutes=config_data.get('check_interval_minutes', 5),
            max_concurrent_tests=config_data.get('max_concurrent_tests', 5),
            timeout_seconds=config_data.get('timeout_seconds', 10),
            send_only_failures=config_data.get('send_only_failures', False),
            send_summary=config_data.get('send_summary', True),
            telegram_token=config_data.get('telegram_token'),
            telegram_chat_id=config_data.get('telegram_chat_id'),
            twilio_account_sid=config_data.get('twilio_account_sid'),
            twilio_auth_token=config_data.get('twilio_auth_token'),
            twilio_whatsapp_from=config_data.get('twilio_whatsapp_from'),
            whatsapp_to=config_data.get('whatsapp_to')
        )
    else:
        # Load from environment variables
        return BotConfig(
            github_token=os.getenv('GITHUB_TOKEN'),
            github_owner=os.getenv('GITHUB_OWNER'),
            github_repo=os.getenv('GITHUB_REPO'),
            check_interval_minutes=int(os.getenv('CHECK_INTERVAL_MINUTES', '5')),
            max_concurrent_tests=int(os.getenv('MAX_CONCURRENT_TESTS', '5')),
            timeout_seconds=int(os.getenv('TIMEOUT_SECONDS', '10')),
            send_only_failures=os.getenv('SEND_ONLY_FAILURES', 'false').lower() == 'true',
            send_summary=os.getenv('SEND_SUMMARY', 'true').lower() == 'true',
            telegram_token=os.getenv('TELEGRAM_TOKEN'),
            telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID'),
            twilio_account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
            twilio_auth_token=os.getenv('TWILIO_AUTH_TOKEN'),
            twilio_whatsapp_from=os.getenv('TWILIO_WHATSAPP_FROM'),
            whatsapp_to=os.getenv('WHATSAPP_TO')
        )

def main():
    """Main function to start the bot"""
    try:
        # Load configuration
        config = load_bot_config()
        
        # Validate required config
        if not all([config.github_token, config.github_owner, config.github_repo]):
            logger.error("Missing required GitHub configuration!")
            return
        
        # Create and start bot
        bot = VPNBotChecker(config)
        bot.start_scheduler()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")

if __name__ == "__main__":
    main()