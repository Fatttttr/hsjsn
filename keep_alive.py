#!/usr/bin/env python3
"""
Keep-Alive Module untuk Render.com
Prevents bot from sleeping by sending periodic HTTP requests
"""

import threading
import time
import requests
import os
import logging

logger = logging.getLogger(__name__)

class KeepAlive:
    def __init__(self, service_url=None, ping_interval=600):  # 10 minutes
        """
        Initialize keep-alive service
        
        Args:
            service_url: Your Render service URL (optional)
            ping_interval: Interval between pings in seconds (default: 10 min)
        """
        self.service_url = service_url or os.getenv('RENDER_EXTERNAL_URL')
        self.ping_interval = ping_interval
        self.running = False
        self.thread = None
        
    def start(self):
        """Start keep-alive thread"""
        if not self.service_url:
            logger.warning("No service URL provided, keep-alive disabled")
            return
            
        if self.running:
            logger.warning("Keep-alive already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.thread.start()
        logger.info(f"Keep-alive started, pinging {self.service_url} every {self.ping_interval/60:.1f} minutes")
        
    def stop(self):
        """Stop keep-alive thread"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Keep-alive stopped")
        
    def _keep_alive_loop(self):
        """Main keep-alive loop"""
        while self.running:
            try:
                # Wait for interval
                time.sleep(self.ping_interval)
                
                if not self.running:
                    break
                    
                # Send ping request
                self._send_ping()
                
            except Exception as e:
                logger.error(f"Keep-alive error: {e}")
                
    def _send_ping(self):
        """Send ping request to keep service awake"""
        try:
            # Create health check endpoint URL
            ping_url = f"{self.service_url}/health" if self.service_url.endswith('/') else f"{self.service_url}/health"
            
            # Send quick GET request
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code == 200:
                logger.debug("Keep-alive ping successful")
            else:
                logger.warning(f"Keep-alive ping returned {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Keep-alive ping failed: {e}")
        except Exception as e:
            logger.error(f"Keep-alive ping error: {e}")

# Global keep-alive instance
keep_alive = KeepAlive()

def start_keep_alive(service_url=None, ping_interval=600):
    """
    Start keep-alive service
    
    Args:
        service_url: Your Render service URL
        ping_interval: Ping interval in seconds (default: 10 minutes)
    """
    global keep_alive
    keep_alive = KeepAlive(service_url, ping_interval)
    keep_alive.start()

def stop_keep_alive():
    """Stop keep-alive service"""
    global keep_alive
    if keep_alive:
        keep_alive.stop()