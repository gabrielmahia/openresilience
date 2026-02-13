"""
SMS Alert Service for OpenResilience Kenya

Provides free water alerts via SMS for farmers without smartphones.

Features:
- Weekly water stress updates
- Critical shortage warnings
- Planting season reminders
- Water truck schedules

Uses Africa's Talking API - Kenya's leading SMS platform
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib


class SMSAlertService:
    """
    Manages SMS subscriptions and sends alerts via Africa's Talking.
    
    Subscription: SMS 'MAJI' to 22555
    Cost: Free (standard SMS rates apply)
    """
    
    def __init__(self, api_key: str = None, username: str = None):
        """
        Initialize SMS service.
        
        Args:
            api_key: Africa's Talking API key (or from environment)
            username: Africa's Talking username (or from environment)
        """
        self.api_key = api_key or os.getenv('AFRICASTALKING_API_KEY')
        self.username = username or os.getenv('AFRICASTALKING_USERNAME', 'sandbox')
        
        # Initialize Africa's Talking
        try:
            import africastalking
            africastalking.initialize(self.username, self.api_key)
            self.sms = africastalking.SMS
            self.available = True
        except ImportError:
            print("Africa's Talking SDK not installed. Run: pip install africastalking")
            self.available = False
        except Exception as e:
            print(f"SMS service initialization failed: {e}")
            self.available = False
    
    def send_alert(
        self,
        phone_number: str,
        message: str,
        county: str = None
    ) -> Dict[str, any]:
        """
        Send SMS alert to a phone number.
        
        Args:
            phone_number: Kenyan phone number (+254...)
            message: Alert message (max 160 chars for single SMS)
            county: County name for tracking
        
        Returns:
            Dict with status and details
        """
        if not self.available:
            return {
                'success': False,
                'error': 'SMS service not available',
                'message': message
            }
        
        # Format phone number for Kenya
        phone = self._format_kenyan_number(phone_number)
        
        try:
            response = self.sms.send(message, [phone])
            
            return {
                'success': True,
                'phone': phone,
                'county': county,
                'message': message,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'phone': phone,
                'message': message
            }
    
    def send_water_stress_alert(
        self,
        phone_number: str,
        county: str,
        stress_level: float,
        action: str,
        language: str = 'en'
    ) -> Dict[str, any]:
        """
        Send water stress alert.
        
        Args:
            phone_number: Recipient phone
            county: County name
            stress_level: Water stress (0-1)
            action: Required action
            language: 'en' or 'sw'
        
        Returns:
            Send status
        """
        if language == 'sw':
            # Kiswahili message
            if stress_level >= 0.7:
                status = "DHARURA"  # Emergency
                emoji = "🔴"
            elif stress_level >= 0.5:
                status = "HATARI"  # Danger
                emoji = "🟠"
            else:
                status = "WASTANI"  # Moderate
                emoji = "🟡"
            
            message = (
                f"{emoji} OPENRESILIENCE\n"
                f"{county}: {status}\n"
                f"Hatua: {action}\n"
                f"Tuma STOP kwa 22555 kusitisha"
            )
        else:
            # English message
            if stress_level >= 0.7:
                status = "CRITICAL"
                emoji = "🔴"
            elif stress_level >= 0.5:
                status = "HIGH"
                emoji = "🟠"
            else:
                status = "MODERATE"
                emoji = "🟡"
            
            message = (
                f"{emoji} OPENRESILIENCE\n"
                f"{county}: {status}\n"
                f"Action: {action}\n"
                f"SMS STOP to 22555 to unsubscribe"
            )
        
        return self.send_alert(phone_number, message, county)
    
    def send_planting_reminder(
        self,
        phone_number: str,
        county: str,
        season: str,
        recommended_crops: List[str],
        language: str = 'en'
    ) -> Dict[str, any]:
        """
        Send planting season reminder.
        
        Args:
            phone_number: Recipient phone
            county: County name
            season: Season name
            recommended_crops: List of crops to plant
            language: 'en' or 'sw'
        
        Returns:
            Send status
        """
        crops = ", ".join(recommended_crops[:3])  # Max 3 crops to fit SMS
        
        if language == 'sw':
            message = (
                f"🌱 MSIMU WA KUPANDA\n"
                f"{county}: {season}\n"
                f"Panda: {crops}\n"
                f"OpenResilience Kenya"
            )
        else:
            message = (
                f"🌱 PLANTING SEASON\n"
                f"{county}: {season}\n"
                f"Plant: {crops}\n"
                f"OpenResilience Kenya"
            )
        
        return self.send_alert(phone_number, message, county)
    
    def send_water_truck_schedule(
        self,
        phone_number: str,
        location: str,
        time: str,
        cost: str,
        language: str = 'en'
    ) -> Dict[str, any]:
        """
        Send water truck schedule.
        
        Args:
            phone_number: Recipient phone
            location: Delivery location
            time: Delivery time
            cost: Cost per 20L
            language: 'en' or 'sw'
        
        Returns:
            Send status
        """
        if language == 'sw':
            message = (
                f"🚛 LORI LA MAJI\n"
                f"Mahali: {location}\n"
                f"Saa: {time}\n"
                f"Bei: {cost}\n"
                f"OpenResilience"
            )
        else:
            message = (
                f"🚛 WATER TRUCK\n"
                f"Location: {location}\n"
                f"Time: {time}\n"
                f"Cost: {cost}\n"
                f"OpenResilience"
            )
        
        return self.send_alert(phone_number, message)
    
    def send_weekly_summary(
        self,
        phone_number: str,
        county: str,
        wsi: float,
        forecast: str,
        tip: str,
        language: str = 'en'
    ) -> Dict[str, any]:
        """
        Send weekly water stress summary.
        
        Args:
            phone_number: Recipient phone
            county: County name
            wsi: Water Stress Index
            forecast: Short forecast
            tip: Water-saving tip
            language: 'en' or 'sw'
        
        Returns:
            Send status
        """
        if language == 'sw':
            message = (
                f"📊 RIPOTI YA WIKI\n"
                f"{county}: Shinikizo {int(wsi*100)}%\n"
                f"Ubashiri: {forecast}\n"
                f"Ushauri: {tip}\n"
                f"OpenResilience"
            )
        else:
            message = (
                f"📊 WEEKLY SUMMARY\n"
                f"{county}: Stress {int(wsi*100)}%\n"
                f"Forecast: {forecast}\n"
                f"Tip: {tip}\n"
                f"OpenResilience"
            )
        
        return self.send_alert(phone_number, message, county)
    
    def _format_kenyan_number(self, phone: str) -> str:
        """
        Format phone number to Kenya format (+254...).
        
        Args:
            phone: Raw phone number
        
        Returns:
            Formatted +254... number
        """
        # Remove spaces and special chars
        clean = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # Convert to +254 format
        if clean.startswith('+254'):
            return clean
        elif clean.startswith('254'):
            return f'+{clean}'
        elif clean.startswith('0'):
            return f'+254{clean[1:]}'
        elif clean.startswith('7') or clean.startswith('1'):
            return f'+254{clean}'
        else:
            return clean
    
    def parse_incoming_sms(self, from_number: str, text: str) -> Dict[str, any]:
        """
        Parse incoming SMS for subscription/commands.
        
        Commands:
        - MAJI: Subscribe to alerts
        - STOP: Unsubscribe
        - HELP: Get help
        - STATUS <county>: Get current status
        
        Args:
            from_number: Sender phone number
            text: SMS text
        
        Returns:
            Dict with command and response
        """
        text_upper = text.strip().upper()
        phone = self._format_kenyan_number(from_number)
        
        if text_upper == 'MAJI':
            return {
                'command': 'subscribe',
                'phone': phone,
                'response': (
                    "✅ Welcome to OpenResilience!\n"
                    "You'll receive weekly water alerts.\n"
                    "SMS STOP to unsubscribe.\n"
                    "SMS HELP for commands."
                )
            }
        
        elif text_upper == 'STOP':
            return {
                'command': 'unsubscribe',
                'phone': phone,
                'response': (
                    "You've unsubscribed from OpenResilience alerts.\n"
                    "SMS MAJI to 22555 to resubscribe anytime."
                )
            }
        
        elif text_upper == 'HELP':
            return {
                'command': 'help',
                'phone': phone,
                'response': (
                    "OpenResilience Commands:\n"
                    "MAJI - Subscribe\n"
                    "STOP - Unsubscribe\n"
                    "STATUS <county> - Check status\n"
                    "Free service, SMS rates apply"
                )
            }
        
        elif text_upper.startswith('STATUS'):
            # Extract county name
            parts = text_upper.split()
            county = parts[1] if len(parts) > 1 else None
            
            return {
                'command': 'status_request',
                'phone': phone,
                'county': county,
                'response': None  # Will be filled by app with real data
            }
        
        else:
            return {
                'command': 'unknown',
                'phone': phone,
                'response': (
                    "Unknown command.\n"
                    "SMS HELP to 22555 for available commands.\n"
                    "OpenResilience Kenya"
                )
            }


# Subscription database (in production, use real database)
class SubscriptionManager:
    """
    Manages SMS subscriptions.
    
    In production, use PostgreSQL or similar.
    """
    
    def __init__(self):
        self.subscriptions = {}  # phone -> {county, language, active}
    
    def subscribe(
        self,
        phone: str,
        county: str,
        language: str = 'en'
    ) -> bool:
        """
        Subscribe phone number to alerts.
        
        Args:
            phone: Phone number
            county: County to monitor
            language: 'en' or 'sw'
        
        Returns:
            Success status
        """
        self.subscriptions[phone] = {
            'county': county,
            'language': language,
            'active': True,
            'subscribed_at': datetime.now().isoformat()
        }
        return True
    
    def unsubscribe(self, phone: str) -> bool:
        """
        Unsubscribe phone number.
        
        Args:
            phone: Phone number
        
        Returns:
            Success status
        """
        if phone in self.subscriptions:
            self.subscriptions[phone]['active'] = False
            self.subscriptions[phone]['unsubscribed_at'] = datetime.now().isoformat()
            return True
        return False
    
    def get_subscribers_for_county(self, county: str) -> List[Dict]:
        """
        Get all active subscribers for a county.
        
        Args:
            county: County name
        
        Returns:
            List of subscriber dicts
        """
        return [
            {'phone': phone, **data}
            for phone, data in self.subscriptions.items()
            if data.get('active') and data.get('county') == county
        ]
    
    def get_all_active_subscribers(self) -> List[Dict]:
        """
        Get all active subscribers.
        
        Returns:
            List of subscriber dicts
        """
        return [
            {'phone': phone, **data}
            for phone, data in self.subscriptions.items()
            if data.get('active')
        ]


# Export
__all__ = [
    'SMSAlertService',
    'SubscriptionManager'
]
