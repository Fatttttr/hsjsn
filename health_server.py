#!/usr/bin/env python3
"""
Simple Health Check Server untuk Keep-Alive
Provides HTTP endpoint for Render keep-alive pings
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    """Simple health check handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'vpn-bot-checker',
                'uptime': time.time() - getattr(self.server, 'start_time', time.time())
            }
            
            self.wfile.write(json.dumps(response).encode())
            logger.debug("Health check responded")
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP logs to avoid spam"""
        pass

class HealthServer:
    """Simple HTTP server untuk health checks"""
    
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.thread = None
        self.running = False
        
    def start(self):
        """Start health server in background thread"""
        if self.running:
            logger.warning("Health server already running")
            return
            
        try:
            self.server = HTTPServer(('0.0.0.0', self.port), HealthHandler)
            self.server.start_time = time.time()
            
            self.running = True
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
            
            logger.info(f"Health server started on port {self.port}")
            
        except Exception as e:
            logger.error(f"Failed to start health server: {e}")
            
    def stop(self):
        """Stop health server"""
        self.running = False
        if self.server:
            self.server.shutdown()
        if self.thread:
            self.thread.join()
        logger.info("Health server stopped")
        
    def _run_server(self):
        """Run server loop"""
        try:
            self.server.serve_forever()
        except Exception as e:
            if self.running:
                logger.error(f"Health server error: {e}")

# Global health server instance
health_server = HealthServer()

def start_health_server(port=8080):
    """Start health server"""
    global health_server
    health_server = HealthServer(port)
    health_server.start()

def stop_health_server():
    """Stop health server"""
    global health_server
    if health_server:
        health_server.stop()