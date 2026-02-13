"""
Send weekly water stress alerts to all subscribers

Run this script every Sunday to send updates to farmers.
Schedule with cron: 0 8 * * 0 (Every Sunday at 8 AM)
"""

import sys
import os
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, 'src')

from openresilience.sms_alerts import SMSAlertService, SubscriptionManager


def send_weekly_alerts():
    """Send weekly alerts to all active subscribers."""
    
    print("=" * 60)
    print("OpenResilience Kenya - Weekly SMS Alerts")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Initialize services
    sms = SMSAlertService()
    sub_manager = SubscriptionManager()
    
    if not sms.available:
        print("\n❌ SMS service not available!")
        return
    
    # Get all active subscribers
    subscribers = sub_manager.get_all_active_subscribers()
    
    print(f"\n📊 Active subscribers: {len(subscribers)}")
    
    if len(subscribers) == 0:
        print("\n⚠️  No active subscribers. Nothing to send.")
        return
    
    # Send alerts
    sent_count = 0
    failed_count = 0
    
    for sub in subscribers:
        phone = sub['phone']
        county = sub.get('county', 'Kiambu')
        language = sub.get('language', 'en')
        
        print(f"\n📱 Sending to {phone} ({county}, {language})...")
        
        # TODO: Get real data from database for this county
        # For now, use sample data
        wsi = 0.53  # Example water stress
        forecast = "Worsening"
        tip = "Harvest rainwater"
        
        # Send weekly summary
        result = sms.send_weekly_summary(
            phone_number=phone,
            county=county,
            wsi=wsi,
            forecast=forecast,
            tip=tip,
            language=language
        )
        
        if result.get('success'):
            print(f"   ✅ Sent successfully")
            sent_count += 1
        else:
            print(f"   ❌ Failed: {result.get('error')}")
            failed_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("WEEKLY ALERTS SUMMARY")
    print("=" * 60)
    print(f"✅ Sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total: {len(subscribers)}")
    
    if sent_count > 0:
        cost_estimate = sent_count * 0.80  # KES per SMS
        print(f"\n💰 Estimated cost: {cost_estimate:.2f} KES (~${cost_estimate/130:.2f} USD)")
    
    print("=" * 60)


if __name__ == "__main__":
    send_weekly_alerts()
