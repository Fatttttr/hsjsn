#!/usr/bin/env python3
"""
External Ping Service Setup Guide

Alternative to self-ping: use free external services to ping your Render app
"""

EXTERNAL_PING_SERVICES = {
    "UptimeRobot": {
        "url": "https://uptimerobot.com/",
        "free_tier": "50 monitors",
        "interval": "5 minutes minimum",
        "setup": [
            "1. Sign up at https://uptimerobot.com/",
            "2. Add new monitor",
            "3. Type: HTTP(s)",
            "4. URL: Your Render app URL (e.g., https://your-app.onrender.com/health)",
            "5. Monitoring interval: 5 minutes",
            "6. Save monitor"
        ],
        "benefits": [
            "✅ 100% external (no self-ping needed)",
            "✅ Professional monitoring service", 
            "✅ Email alerts if app goes down",
            "✅ Uptime statistics",
            "✅ Completely free"
        ]
    },
    
    "Cron-job.org": {
        "url": "https://cron-job.org/",
        "free_tier": "5 cron jobs",
        "interval": "1 minute minimum",
        "setup": [
            "1. Sign up at https://cron-job.org/",
            "2. Create new cron job",
            "3. URL: Your Render app URL/health",
            "4. Schedule: */10 * * * * (every 10 minutes)",
            "5. Enable job"
        ],
        "benefits": [
            "✅ More frequent pings (1min minimum)",
            "✅ Flexible scheduling",
            "✅ HTTP request logs",
            "✅ Free tier available"
        ]
    },
    
    "Pingdom": {
        "url": "https://www.pingdom.com/",
        "free_tier": "1 check, 1 minute interval",
        "setup": [
            "1. Sign up for free account",
            "2. Add uptime check",
            "3. URL: Your Render app URL",
            "4. Check interval: 1 minute",
            "5. Start monitoring"
        ],
        "benefits": [
            "✅ Professional grade monitoring",
            "✅ 1 minute intervals",
            "✅ Detailed performance metrics",
            "✅ Global monitoring locations"
        ]
    }
}

def print_setup_guide():
    """Print setup guide for external ping services"""
    
    print("🔧 EXTERNAL PING SERVICES SETUP")
    print("=" * 50)
    print("\nTo keep your Render app awake WITHOUT self-ping:")
    print()
    
    for service_name, info in EXTERNAL_PING_SERVICES.items():
        print(f"📡 {service_name}")
        print(f"   URL: {info['url']}")
        print(f"   Free: {info['free_tier']}")
        print(f"   Interval: {info['interval']}")
        print()
        print("   Setup Steps:")
        for step in info['setup']:
            print(f"   {step}")
        print()
        print("   Benefits:")
        for benefit in info['benefits']:
            print(f"   {benefit}")
        print()
        print("-" * 40)
        print()
    
    print("🎯 RECOMMENDATION:")
    print("Use UptimeRobot (free, reliable, 5min intervals)")
    print("Your Render app URL: https://your-app-name.onrender.com/health")
    print()
    print("✅ Result: App stays awake 24/7 dengan external monitoring")
    print("✅ Bonus: Real uptime monitoring dan alerts!")

if __name__ == "__main__":
    print_setup_guide()