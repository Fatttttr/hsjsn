#!/bin/bash
# Persistent Bot Runner dengan Auto-Restart
# Usage: ./run_persistent.sh

echo "🤖 Starting VPN Bot with Auto-Restart"
echo "📍 Press Ctrl+C to stop completely"
echo "🔄 Bot will auto-restart if crash"
echo "===================="

while true; do
    echo "$(date): Starting VPN Bot..."
    
    # Run bot
    python3 bot_vpn_checker.py
    
    # If bot exits, wait 30 seconds then restart
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "$(date): Bot stopped normally (exit code 0)"
        break
    else
        echo "$(date): Bot crashed (exit code $exit_code)"
        echo "🔄 Restarting in 30 seconds..."
        sleep 30
    fi
done

echo "$(date): Bot runner stopped"
