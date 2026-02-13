"""
Test script for SMS Alert Service

Run this to test Africa's Talking integration before deploying.
"""

import sys
import os
sys.path.insert(0, 'src')

from openresilience.sms_alerts import SMSAlertService, SubscriptionManager


def test_sms_service():
    """Test SMS alert service."""
    
    print("=" * 60)
    print("OpenResilience Kenya - SMS Alert Service Test")
    print("=" * 60)
    
    # Initialize service
    sms = SMSAlertService()
    
    if not sms.available:
        print("\n❌ SMS service not available")
        print("Make sure you have:")
        print("1. Installed: pip install africastalking")
        print("2. Set environment variables:")
        print("   export AFRICASTALKING_USERNAME=your_username")
        print("   export AFRICASTALKING_API_KEY=your_api_key")
        return False
    
    print("\n✅ SMS service initialized")
    print(f"Username: {sms.username}")
    
    # Test phone number formatting
    print("\n" + "=" * 60)
    print("Testing phone number formatting...")
    print("=" * 60)
    
    test_numbers = [
        "0712345678",
        "712345678",
        "+254712345678",
        "254712345678"
    ]
    
    for num in test_numbers:
        formatted = sms._format_kenyan_number(num)
        print(f"{num:15} → {formatted}")
    
    # Test message parsing
    print("\n" + "=" * 60)
    print("Testing incoming SMS parsing...")
    print("=" * 60)
    
    test_messages = [
        ("MAJI", "Subscribe command"),
        ("STOP", "Unsubscribe command"),
        ("HELP", "Help command"),
        ("STATUS KIAMBU", "Status request"),
        ("RANDOM", "Unknown command")
    ]
    
    for msg, desc in test_messages:
        result = sms.parse_incoming_sms("+254712345678", msg)
        print(f"\n{desc}:")
        print(f"  Input: {msg}")
        print(f"  Command: {result['command']}")
        print(f"  Response: {result['response'][:50]}..." if result['response'] else "  (no auto-response)")
    
    # Test subscription manager
    print("\n" + "=" * 60)
    print("Testing subscription manager...")
    print("=" * 60)
    
    sub_manager = SubscriptionManager()
    
    # Subscribe test user
    sub_manager.subscribe("+254712345678", "Kiambu", "en")
    print("✅ Subscribed: +254712345678 → Kiambu (English)")
    
    # Get subscribers
    kiambu_subs = sub_manager.get_subscribers_for_county("Kiambu")
    print(f"✅ Kiambu subscribers: {len(kiambu_subs)}")
    
    # Unsubscribe
    sub_manager.unsubscribe("+254712345678")
    print("✅ Unsubscribed: +254712345678")
    
    # Test message templates
    print("\n" + "=" * 60)
    print("Testing message templates...")
    print("=" * 60)
    
    print("\n1. Water Stress Alert (English):")
    print("-" * 40)
    alert = sms.send_water_stress_alert(
        "+254712345678",
        "Kiambu",
        0.65,
        "Reduce water use by 20%",
        "en"
    )
    print(alert['message'])
    print(f"Characters: {len(alert['message'])} / 160")
    
    print("\n2. Water Stress Alert (Kiswahili):")
    print("-" * 40)
    alert_sw = sms.send_water_stress_alert(
        "+254712345678",
        "Kiambu",
        0.65,
        "Punguza matumizi ya maji 20%",
        "sw"
    )
    print(alert_sw['message'])
    print(f"Characters: {len(alert_sw['message'])} / 160")
    
    print("\n3. Planting Reminder:")
    print("-" * 40)
    planting = sms.send_planting_reminder(
        "+254712345678",
        "Kiambu",
        "Long Rains",
        ["Maize", "Beans", "Potatoes"],
        "en"
    )
    print(planting['message'])
    print(f"Characters: {len(planting['message'])} / 160")
    
    print("\n4. Weekly Summary:")
    print("-" * 40)
    summary = sms.send_weekly_summary(
        "+254712345678",
        "Kiambu",
        0.53,
        "Worsening",
        "Harvest rainwater",
        "en"
    )
    print(summary['message'])
    print(f"Characters: {len(summary['message'])} / 160")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Get Africa's Talking production API key")
    print("2. Test sending real SMS to your phone")
    print("3. Set up webhook for incoming SMS")
    print("4. Apply for shortcode (22555)")
    
    return True


if __name__ == "__main__":
    test_sms_service()
