"""
Replit Keep-Alive Service
Keeps the bot running 24/7 on free tier
"""

from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return {
        'status': 'VPN Bot Running',
        'platform': 'Replit.com',
        'uptime': 'Always-On'
    }

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'vpn-bot-checker'}

def keep_alive():
    """Start Flask server in background thread"""
    app.run(host='0.0.0.0', port=8080, debug=False)

def start_keep_alive():
    """Start keep-alive server"""
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    print("🌐 Keep-alive server started on port 8080")

if __name__ == "__main__":
    keep_alive()
