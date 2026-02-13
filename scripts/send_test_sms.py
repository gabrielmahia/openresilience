"""
Send a REAL test SMS to your phone

This will actually send an SMS using Africa's Talking!
"""

import sys
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, 'src')

from openresilience.sms_alerts import SMSAlertService


def send_test_sms():
    """Send test SMS to your phone."""
    
    print("=" * 60)
    print("OpenResilience Kenya - Send Test SMS")
    print("=" * 60)
    
    # Initialize service
    sms = SMSAlertService()
    
    if not sms.available:
        print("\n❌ SMS service not available!")
        print("\nTroubleshooting:")
        print("1. Check environment variables are set:")
        print("   echo $AFRICASTALKING_USERNAME")
        print("   echo $AFRICASTALKING_API_KEY")
        print("2. Check API key is correct (from AT dashboard)")
        print("3. Make sure you're using SANDBOX credentials for testing")
        return
    
    print(f"\n✅ SMS service initialized")
    print(f"Username: {sms.username}")
    print(f"Mode: {'Sandbox (FREE)' if sms.username == 'sandbox' else 'Production'}")
    
    # Get phone number
    print("\n" + "=" * 60)
    print("Enter YOUR phone number to receive test SMS:")
    print("=" * 60)
    print("\nExamples:")
    print("  0712345678")
    print("  +254712345678")
    print("  254712345678")
    
    phone = input("\nYour phone number: ").strip()
    
    if not phone:
        print("\n❌ No phone number entered!")
        return
    
    # Format phone number
    formatted_phone = sms._format_kenyan_number(phone)
    print(f"\n✅ Formatted phone: {formatted_phone}")
    
    # Confirm
    print("\n" + "=" * 60)
    print(f"Ready to send test SMS to: {formatted_phone}")
    print("=" * 60)
    
    confirm = input("\nSend test SMS? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("\n❌ Cancelled. No SMS sent.")
        return
    
    # Send water stress alert
    print("\n📱 Sending water stress alert...")
    
    result = sms.send_water_stress_alert(
        phone_number=formatted_phone,
        county="Kiambu",
        stress_level=0.65,
        action="Reduce water use by 20%",
        language="en"
    )
    
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    
    if result.get('success'):
        print("\n✅ SMS SENT SUCCESSFULLY!")
        print(f"\nPhone: {result['phone']}")
        print(f"County: {result['county']}")
        print(f"Timestamp: {result['timestamp']}")
        print("\nMessage sent:")
        print("-" * 40)
        print(result['message'])
        print("-" * 40)
        
        print("\n" + "=" * 60)
        print("CHECK YOUR PHONE!")
        print("=" * 60)
        print("\nYou should receive an SMS in 5-30 seconds.")
        print("\nNote: In SANDBOX mode, you can only send to numbers")
        print("      registered in your Africa's Talking dashboard.")
        print("\nTo register your phone for testing:")
        print("1. Go to: https://account.africastalking.com/apps/sandbox")
        print("2. Settings → Test Numbers")
        print("3. Add your phone number")
        
    else:
        print("\n❌ SMS FAILED!")
        print(f"\nError: {result.get('error')}")
        print("\nCommon issues:")
        print("1. Sandbox mode: Phone must be registered in AT dashboard")
        print("2. Invalid API key: Check credentials")
        print("3. Insufficient credits: Top up account (production only)")
        print("4. Invalid phone format: Must be Kenya number (+254...)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    send_test_sms()
