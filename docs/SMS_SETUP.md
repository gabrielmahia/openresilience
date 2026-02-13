# SMS Alert Service Setup Guide

## 🎯 **Overview**

Provide **FREE water alerts via SMS** for farmers without smartphones or internet.

**Features:**
- ✅ Weekly water stress updates
- ✅ Critical shortage warnings
- ✅ Planting season reminders
- ✅ Water truck schedules

**Target Users:**
- Farmers with basic phones (no smartphone needed)
- Community members in rural areas
- Anyone without reliable internet

---

## 📱 **How It Works**

### **For Farmers:**

1. **Subscribe:** SMS `MAJI` to `22555`
2. **Receive:** Weekly alerts about water conditions
3. **Unsubscribe:** SMS `STOP` to `22555` anytime

**Cost:** FREE service (standard SMS rates apply - typically 1 KES per SMS)

### **Commands:**

| Command | Description |
|---------|-------------|
| `MAJI` | Subscribe to water alerts |
| `STOP` | Unsubscribe from alerts |
| `HELP` | Get list of commands |
| `STATUS <county>` | Check current water status |

---

## 🔧 **Technical Setup**

### **1. Get Africa's Talking Account**

**Africa's Talking** is Kenya's leading SMS platform.

**Signup:**
1. Go to: https://africastalking.com/
2. Create account
3. Choose Kenya as country
4. Verify phone number

**Pricing:**
- **Sandbox:** FREE (for testing, limited to 100 SMS/day)
- **Production:** ~0.80 KES per SMS (~$0.006 USD)
- **Bulk rates:** Lower costs for high volume

### **2. Get API Credentials**

**Dashboard → Settings → API Key**

You'll need:
- `username`: Your Africa's Talking username
- `api_key`: Your API key (keep this SECRET!)

**For testing:**
- Username: `sandbox`
- API Key: Generate in sandbox dashboard

### **3. Set Up Shortcode**

**What's a Shortcode?**
A 5-digit number (like `22555`) that farmers can SMS.

**Options:**

**A) Shared Shortcode (Cheaper)**
- Cost: ~5,000 KES/month (~$40 USD)
- Number: Shared with other services
- Keywords: You get exclusive keywords like `MAJI`

**B) Dedicated Shortcode (Premium)**
- Cost: ~50,000 KES/month (~$400 USD)
- Number: Exclusive to your service
- All SMS to this number come to you

**For MVP:** Start with **regular long number** (cheaper):
- Cost: FREE
- Example: Farmers SMS to `+254712345678`
- Limitation: Longer number to remember

### **4. Install Dependencies**

```bash
pip install africastalking
```

Add to `requirements.txt`:
```
africastalking>=1.2.8
```

### **5. Configure Environment Variables**

Create `.env` file (NEVER commit this!):

```bash
# Africa's Talking Credentials
AFRICASTALKING_USERNAME=your_username_here
AFRICASTALKING_API_KEY=your_api_key_here

# Shortcode (or long number for testing)
SMS_SHORTCODE=22555
```

### **6. Initialize Service**

```python
from openresilience.sms_alerts import SMSAlertService

# Initialize (reads from environment)
sms_service = SMSAlertService()

# Send test alert
result = sms_service.send_water_stress_alert(
    phone_number='+254712345678',
    county='Kiambu',
    stress_level=0.65,
    action='Reduce water use by 20%',
    language='en'
)

print(result)
```

---

## 💰 **Cost Estimation**

### **Scenario 1: Small Pilot (100 farmers)**

**Setup:**
- Long number (no shortcode): FREE
- Africa's Talking account: FREE sandbox

**Monthly costs:**
- 100 farmers × 1 weekly SMS = 400 SMS/month
- Cost: 400 × 0.80 KES = **320 KES/month (~$2.50 USD)**

**Total: ~$2.50/month** ✅ Very affordable!

### **Scenario 2: County-Wide (1,000 farmers)**

**Setup:**
- Shared shortcode: 5,000 KES/month
- Africa's Talking production: SMS fees

**Monthly costs:**
- Shortcode: 5,000 KES (~$40)
- 1,000 farmers × 1 weekly SMS = 4,000 SMS/month
- SMS cost: 4,000 × 0.80 KES = 3,200 KES (~$25)

**Total: ~$65/month**

### **Scenario 3: National (10,000 farmers)**

**Setup:**
- Dedicated shortcode: 50,000 KES/month
- Bulk SMS rates: ~0.60 KES/SMS

**Monthly costs:**
- Shortcode: 50,000 KES (~$400)
- 10,000 farmers × 1 weekly SMS = 40,000 SMS/month
- SMS cost: 40,000 × 0.60 KES = 24,000 KES (~$185)

**Total: ~$585/month**

**Cost per farmer: ~$0.06/month** (very affordable at scale!)

---

## 📊 **Message Templates**

### **Water Stress Alert (English)**

```
🔴 OPENRESILIENCE
Kiambu: CRITICAL
Action: Reduce water use by 40%
SMS STOP to 22555 to unsubscribe
```
*Characters: 96 / 160 (fits in single SMS)*

### **Water Stress Alert (Kiswahili)**

```
🔴 OPENRESILIENCE
Kiambu: DHARURA
Hatua: Punguza maji 40%
Tuma STOP kwa 22555 kusitisha
```
*Characters: 88 / 160*

### **Planting Reminder (English)**

```
🌱 PLANTING SEASON
Kiambu: Long Rains
Plant: Maize, Beans, Potatoes
OpenResilience Kenya
```
*Characters: 85 / 160*

### **Weekly Summary (English)**

```
📊 WEEKLY SUMMARY
Kiambu: Stress 65%
Forecast: Worsening
Tip: Harvest rainwater now
OpenResilience
```
*Characters: 95 / 160*

**All messages fit in single SMS = lower costs!**

---

## 🚀 **Deployment Steps**

### **Step 1: Testing (Sandbox)**

```bash
# Use sandbox credentials
export AFRICASTALKING_USERNAME=sandbox
export AFRICASTALKING_API_KEY=your_sandbox_key

# Run test
python scripts/test_sms.py
```

### **Step 2: Pilot (10-100 farmers)**

1. Get production API key
2. Use long number (no shortcode yet)
3. Manually register 10-100 farmers
4. Send weekly alerts
5. Collect feedback

### **Step 3: Scale (100-1,000 farmers)**

1. Apply for shared shortcode
2. Set up webhook for incoming SMS
3. Automate subscription (SMS MAJI to 22555)
4. Monitor delivery rates

### **Step 4: National (1,000+ farmers)**

1. Upgrade to dedicated shortcode
2. Set up database (PostgreSQL)
3. Add analytics dashboard
4. Partner with Safaricom for bulk rates

---

## 🔌 **Integration with App**

### **Add to Streamlit App**

```python
# In app.py

# Show SMS service info
with st.expander("📱 SMS Alert Service"):
    st.markdown("""
    ### Free Water Alerts via SMS
    
    **No smartphone or internet needed!**
    
    **Receive:**
    - Weekly water stress updates
    - Critical shortage warnings
    - Planting season reminders
    - Water truck schedules
    
    **To register:** SMS `MAJI` to `22555`
    
    **Cost:** Free service (standard SMS rates apply)
    """)
```

### **Webhook for Incoming SMS**

```python
# webhook.py - Handle incoming SMS

from flask import Flask, request
from openresilience.sms_alerts import SMSAlertService, SubscriptionManager

app = Flask(__name__)
sms_service = SMSAlertService()
sub_manager = SubscriptionManager()

@app.route('/sms/callback', methods=['POST'])
def handle_incoming_sms():
    # Parse incoming SMS
    from_number = request.values.get('from')
    text = request.values.get('text')
    
    # Process command
    result = sms_service.parse_incoming_sms(from_number, text)
    
    if result['command'] == 'subscribe':
        # Add to database
        sub_manager.subscribe(result['phone'], 'Kiambu', 'en')
    
    elif result['command'] == 'unsubscribe':
        # Remove from database
        sub_manager.unsubscribe(result['phone'])
    
    # Send response
    sms_service.send_alert(from_number, result['response'])
    
    return 'OK', 200
```

---

## 📈 **Analytics & Monitoring**

### **Track:**
- Subscription rate
- Delivery success rate
- Unsubscribe rate
- Response rate (to commands)
- Cost per farmer

### **Tools:**
- Africa's Talking dashboard (built-in analytics)
- Google Analytics (track web subscriptions)
- Custom database queries

---

## ⚠️ **Important Notes**

### **Compliance:**
- ✅ Get consent before sending SMS
- ✅ Provide easy unsubscribe (SMS STOP)
- ✅ Don't send marketing without permission
- ✅ Follow Kenya Communications Authority rules

### **Best Practices:**
- ✅ Send at reasonable hours (8am-8pm)
- ✅ Keep messages under 160 characters (single SMS)
- ✅ Use clear, simple language
- ✅ Include unsubscribe instructions
- ✅ Test thoroughly before scale

### **Security:**
- ✅ Never commit API keys to Git
- ✅ Use environment variables
- ✅ Rate limit API calls
- ✅ Validate phone numbers
- ✅ Encrypt database

---

## 🎯 **Next Steps**

**Immediate (Week 1):**
1. Get Africa's Talking sandbox account
2. Test SMS sending
3. Add SMS info to app

**Short-term (Month 1):**
1. Get production API key
2. Pilot with 10-50 farmers
3. Collect feedback
4. Refine messages

**Medium-term (Month 3):**
1. Apply for shortcode
2. Set up webhook
3. Automate subscriptions
4. Scale to 100-500 farmers

**Long-term (Month 6+):**
1. Dedicated shortcode
2. Multi-county coverage
3. 1,000+ farmers
4. Analytics dashboard

---

## 📞 **Support**

**Africa's Talking:**
- Documentation: https://developers.africastalking.com/
- Support: support@africastalking.com
- Phone: +254 20 524 2223

**OpenResilience:**
- GitHub Issues: Report problems
- Email: [Your Email]

---

## ✅ **Success Metrics**

**Target (6 months):**
- 1,000+ active subscribers
- 95%+ delivery rate
- <5% unsubscribe rate
- <$0.10 cost per farmer per month

**Impact:**
- Farmers receive timely water alerts
- Reduced water waste
- Better planting decisions
- Improved food security

---

**SMS alerts = Democratizing access to resilience data!** 📱🌍
