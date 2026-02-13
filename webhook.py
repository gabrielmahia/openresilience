"""
Webhook to handle incoming SMS from Africa's Talking

Deploy this to receive SMS from farmers and auto-respond.
"""

from flask import Flask, request, jsonify
import sys
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, 'src')

from openresilience.sms_alerts import SMSAlertService, SubscriptionManager

app = Flask(__name__)

# Initialize services
sms_service = SMSAlertService()
sub_manager = SubscriptionManager()


@app.route('/sms/callback', methods=['POST'])
def handle_incoming_sms():
    """
    Handle incoming SMS from Africa's Talking.
    
    Called when someone sends SMS to your shortcode/number.
    """
    
    # Get SMS details from Africa's Talking
    from_number = request.values.get('from', '')
    to_number = request.values.get('to', '')
    text = request.values.get('text', '')
    date = request.values.get('date', '')
    id = request.values.get('id', '')
    
    print(f"\n📱 Incoming SMS:")
    print(f"  From: {from_number}")
    print(f"  To: {to_number}")
    print(f"  Text: {text}")
    print(f"  Date: {date}")
    print(f"  ID: {id}")
    
    # Parse command
    result = sms_service.parse_incoming_sms(from_number, text)
    
    print(f"\n🔍 Parsed command: {result['command']}")
    
    # Handle different commands
    if result['command'] == 'subscribe':
        # Subscribe user
        # TODO: Get county from user (for now, default to Kiambu)
        sub_manager.subscribe(result['phone'], 'Kiambu', 'en')
        
        print(f"✅ Subscribed: {result['phone']}")
        
        # Send confirmation
        if result['response']:
            sms_service.send_alert(result['phone'], result['response'])
    
    elif result['command'] == 'unsubscribe':
        # Unsubscribe user
        sub_manager.unsubscribe(result['phone'])
        
        print(f"✅ Unsubscribed: {result['phone']}")
        
        # Send confirmation
        if result['response']:
            sms_service.send_alert(result['phone'], result['response'])
    
    elif result['command'] == 'help':
        # Send help message
        if result['response']:
            sms_service.send_alert(result['phone'], result['response'])
    
    elif result['command'] == 'status_request':
        # Get current status for county
        county = result.get('county', 'Kiambu')
        
        # TODO: Get real data from database
        # For now, send sample
        sample_response = (
            f"📊 {county.upper()}\n"
            f"Water Stress: 53% (HIGH)\n"
            f"Action: Reduce water 20%\n"
            f"OpenResilience Kenya"
        )
        
        sms_service.send_alert(result['phone'], sample_response)
    
    else:
        # Unknown command
        if result['response']:
            sms_service.send_alert(result['phone'], result['response'])
    
    # Return success to Africa's Talking
    return jsonify({'status': 'success'}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'OpenResilience SMS Webhook',
        'sms_available': sms_service.available
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("OpenResilience SMS Webhook Server")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /sms/callback  - Handle incoming SMS")
    print("  GET  /health        - Health check")
    print("\nTo deploy publicly, use ngrok:")
    print("  ngrok http 5000")
    print("\nThen configure webhook URL in Africa's Talking dashboard")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
