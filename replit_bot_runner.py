#!/usr/bin/env python3
"""
Replit-optimized VPN Bot Runner
Integrates keep-alive service dengan bot
"""

import threading
import time
import logging
from replit_keepalive import start_keep_alive

logger = logging.getLogger(__name__)

def main():
    """Main function optimized untuk Replit"""
    try:
        # Start keep-alive service untuk prevent sleep
        logger.info("🌐 Starting Replit keep-alive service...")
        start_keep_alive()
        
        # Give keep-alive time to start
        time.sleep(2)
        
        # Start the actual VPN bot
        logger.info("🤖 Starting VPN Bot Checker...")
        from bot_vpn_checker import main as bot_main
        bot_main()
        
    except Exception as e:
        logger.error(f"❌ Replit bot error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
