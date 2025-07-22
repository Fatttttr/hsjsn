#!/usr/bin/env python3
"""
Replit Entry Point for VPN Bot Checker
This file is required by Replit to run the bot
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Replit"""
    try:
        logger.info("🚀 Starting VPN Bot on Replit.com")
        logger.info("🔧 Loading bot configuration...")
        
        # Import and run the bot
        from bot_vpn_checker import main as bot_main
        bot_main()
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
