# SMS Alert Service - QUICK START GUIDE

**Time needed: 10-15 minutes**  
**Cost: FREE (for testing)**

---

## 🎯 **What You'll Do**

1. ✅ Create FREE Africa's Talking account
2. ✅ Run interactive setup wizard (does everything for you!)
3. ✅ Send test SMS to YOUR phone
4. ✅ (Optional) Upgrade to production
5. ✅ (Optional) Get shortcode 22555

---

## 🚀 **LET'S START!**

### **ONE COMMAND TO RULE THEM ALL:**

```bash
cd /path/to/openresilience
python setup_sms.py
```

**That's it!** The wizard will guide you through EVERYTHING step-by-step.

---

## 📋 **What the Wizard Does**

The `setup_sms.py` script will:

1. ✅ Check your Python version
2. ✅ Install required packages (africastalking, python-dotenv, flask)
3. ✅ Ask for your Africa's Talking credentials
4. ✅ Create .env file automatically
5. ✅ Test connection
6. ✅ Send test SMS to your phone
7. ✅ Explain next steps

**You just follow the prompts!**

---

## 🔑 **Before You Start**

### **Get Africa's Talking Account (5 minutes):**

1. Open: https://account.africastalking.com/auth/register
2. Fill in:
   - Email: [your email]
   - Password: [create password]
   - Phone: [your Kenya phone]
3. Verify email
4. Click "Go to Sandbox" (top right)
5. Settings → API Key → Generate
6. **COPY THE API KEY** (starts with `atsk_`)

**Keep this tab open!** You'll need to paste the API key into the wizard.

---

## 💻 **Step-by-Step Commands**

### **1. Open Terminal**

**Mac:** Applications → Utilities → Terminal  
**Windows:** Press Win+R, type `cmd`, press Enter

### **2. Navigate to Project**

```bash
cd ~/openresilience
# OR wherever you cloned the repo
```

### **3. Run Setup Wizard**

```bash
python setup_sms.py
```

### **4. Follow the Prompts**

The wizard will ask you:

```
Username (usually 'sandbox' for testing):
  Username: sandbox

API Key (starts with 'atsk_'):
  API Key: [PASTE YOUR KEY HERE]
```

**Tip:** Right-click to paste in terminal!

### **5. Register Your Test Phone**

When prompted, go to:
- https://account.africastalking.com/apps/sandbox
- Settings → SMS → Test Phone Numbers
- Add your Kenya phone number (+254...)

### **6. Send Test SMS**

The wizard will ask:

```
Ready to send test SMS? (yes/no): yes

Enter YOUR phone number to receive test SMS:
Your phone number: 0712345678

Send test SMS? (yes/no): yes
```

**CHECK YOUR PHONE!** You should get SMS in 5-30 seconds! 📱

---

## ✅ **What You Get**

After setup, you can:

```bash
# Send test SMS anytime
python scripts/send_test_sms.py

# Test all functionality
python scripts/test_sms.py

# Send weekly alerts (when you have subscribers)
python scripts/send_weekly_alerts.py
```

---

## 🐛 **Troubleshooting**

### **"pip: command not found"**

```bash
python -m ensurepip
# Then try again
```

### **"africastalking not found"**

```bash
pip install africastalking python-dotenv flask
# Then try again
```

### **"SMS service not available"**

Check your .env file:
```bash
cat .env
```

Should show:
```
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=atsk_your_key_here
```

### **"Phone not registered" (Sandbox mode)**

1. Go to: https://account.africastalking.com/apps/sandbox
2. Settings → SMS → Test Phone Numbers
3. Add your number (+254...)
4. Try again

### **Test SMS not received**

- ✅ Check phone is registered in sandbox
- ✅ Check phone number format (+254712345678)
- ✅ Wait up to 2 minutes
- ✅ Check Africa's Talking dashboard logs

---

## 🚀 **Next Steps After Setup**

### **1. Test More**

Send SMS to different formats:
- 0712345678
- +254712345678
- 712345678

### **2. Upgrade to Production (When Ready)**

**When:** You're ready to send to ANY Kenya phone

**Cost:** ~0.80 KES per SMS (~$0.006 USD)

**Steps:**
1. Africa's Talking dashboard → "Go to Production"
2. Top up account (1,000 KES minimum)
3. Get NEW production API key
4. Update .env:
   ```bash
   AFRICASTALKING_USERNAME=your_production_username
   AFRICASTALKING_API_KEY=atsk_your_production_key
   ```

### **3. Apply for Shortcode (Recommended)**

**Email:** solutions@africastalking.com  
**Subject:** "Shortcode Application - OpenResilience Kenya"

**Include:**
- Organization name
- Use case: Water stress alerts for farmers
- Expected volume: [estimate]
- Preferred shortcode: 22555

**Cost:** ~5,000 KES/month (~$40 USD)  
**Timeline:** 2-4 weeks

### **4. Deploy Webhook (For Auto-Subscriptions)**

**Deploy webhook.py to Heroku:**

```bash
heroku create openresilience-sms
git push heroku main
heroku config:set AFRICASTALKING_USERNAME=your_username
heroku config:set AFRICASTALKING_API_KEY=your_api_key
```

**Configure in Africa's Talking:**
- Dashboard → SMS → Settings
- Callback URL: `https://your-app.herokuapp.com/sms/callback`

### **5. Schedule Weekly Alerts**

**Cron job (run every Sunday at 8 AM):**

```bash
crontab -e
```

Add:
```
0 8 * * 0 cd /path/to/openresilience && python scripts/send_weekly_alerts.py
```

---

## 💰 **Cost Calculator**

### **Pilot (100 farmers):**
- 100 farmers × 1 SMS/week × 4 weeks = 400 SMS/month
- 400 × 0.80 KES = **320 KES/month (~$2.50 USD)**

### **County-wide (1,000 farmers):**
- 1,000 farmers × 1 SMS/week × 4 weeks = 4,000 SMS/month
- Shortcode: 5,000 KES/month
- SMS: 4,000 × 0.80 = 3,200 KES
- **Total: 8,200 KES/month (~$65 USD)**

### **National (10,000 farmers):**
- 10,000 farmers × 1 SMS/week × 4 weeks = 40,000 SMS/month
- Shortcode: 50,000 KES/month
- SMS: 40,000 × 0.60 = 24,000 KES
- **Total: 74,000 KES/month (~$585 USD)**

**Per farmer: $0.02-0.06/month** ✅ Very affordable!

---

## 📚 **Documentation**

- `docs/SMS_SETUP.md` - Complete 500+ line guide
- `src/openresilience/sms_alerts.py` - Code documentation
- Africa's Talking docs: https://developers.africastalking.com/

---

## 💡 **Pro Tips**

1. **Start in Sandbox** - Test thoroughly before upgrading
2. **Register multiple test phones** - Test with team members
3. **Keep API keys secret** - Never commit .env to Git
4. **Monitor costs** - Check Africa's Talking dashboard daily
5. **Test message length** - Keep under 160 chars to save costs
6. **Use bilingual** - English + Kiswahili reaches more farmers

---

## 🆘 **Get Help**

**Africa's Talking:**
- Support: support@africastalking.com
- Phone: +254 20 524 2223
- Docs: https://developers.africastalking.com/

**OpenResilience:**
- GitHub Issues: Report bugs
- Email: [Your Email]

---

## ✨ **You're Ready!**

Just run:

```bash
python setup_sms.py
```

And follow the wizard! It does EVERYTHING for you! 🚀

---

**Questions? The wizard will help you at each step!** 💪
