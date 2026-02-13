# Streamlit Cloud Deployment - SMS Integration

## 🎯 **Configure SMS in 3 Steps** (No Local Setup!)

---

## **STEP 1: Add Your API Key to Streamlit Secrets**

### **Go to your Streamlit Cloud dashboard:**

1. Open: https://share.streamlit.io/
2. Find your app: `openresilience-whereisthewater`
3. Click the **⚙️ Settings** (gear icon)
4. Click **"Secrets"** in the left sidebar

### **Paste this EXACTLY:**

```toml
[africastalking]
username = "sandbox"
api_key = "atsk_af1c1aca99e7d89a400c8b69617474824d238fc6beec4e53a19bb8bebae763505e774675"
```

### **Click "Save"**

**That's it!** The app will automatically restart with SMS enabled! ✅

---

## **STEP 2: Test SMS from the Web App**

### **After the app restarts (30 seconds):**

1. **Open your app:** https://openresilience-whereisthewater.streamlit.app/
2. **Scroll down** to "📱 SMS Alert Service"
3. **Click to expand it**
4. **You'll see:** "✅ SMS Service Connected! Ready to send alerts!"
5. **Click the** "📤 Send Test Alert" **tab**
6. **Enter YOUR Kenya phone number:** `0712345678`
7. **Click** "📤 Send Test SMS"
8. **CHECK YOUR PHONE!** 📱

**SMS arrives in 5-30 seconds!** 🎉

---

## **STEP 3 (IMPORTANT): Register Test Phone in Sandbox**

### **Sandbox Mode Requirement:**

Africa's Talking Sandbox only sends to **registered test numbers** (for security).

### **Register your phone:**

1. **Go to:** https://account.africastalking.com/apps/sandbox
2. **Click:** "Settings" (left sidebar)
3. **Click:** "SMS" tab
4. **Scroll to:** "Test Phone Numbers"
5. **Click:** "+ Add Phone Number"
6. **Enter:** Your number (+254712345678)
7. **Click:** "Save"

### **Now test again from the app!**

---

## ✅ **What You Get**

### **From the Streamlit App, you can:**

- ✅ Send test SMS to ANY registered number
- ✅ Preview messages before sending
- ✅ Choose language (English/Kiswahili)
- ✅ Select any county
- ✅ See character count
- ✅ Get instant confirmation

### **Farmers can:**

- 📱 Receive water stress alerts on basic phones
- 🌾 Get planting season reminders
- 📊 Weekly water summaries
- 🚛 Water truck schedules

---

## 🚀 **Upgrade to Production (When Ready)**

### **Current: Sandbox Mode**
- ✅ FREE forever
- ⚠️ Only sends to registered test numbers
- ⚠️ Limited to 100 SMS/day

### **Production Mode:**
- ✅ Send to ANY Kenya phone
- ✅ Unlimited SMS
- 💰 Cost: ~0.80 KES per SMS (~$0.006 USD)

### **To Upgrade:**

1. **Africa's Talking Dashboard** → "Go to Production"
2. **Top up account:** 1,000 KES minimum (~$8 USD)
3. **Get NEW production API key**
4. **Update Streamlit Secrets:**
   ```toml
   [africastalking]
   username = "your_production_username"  # NOT "sandbox"
   api_key = "atsk_your_new_production_key_here"
   ```
5. **Save** → App restarts → Production mode active! ✅

---

## 💡 **Pro Tips**

### **Testing:**
- Register 2-3 test phones in sandbox
- Test different counties
- Test both languages
- Check character counts

### **Going Live:**
- Start with small pilot (10-50 farmers)
- Collect feedback
- Refine messages
- Then scale up!

### **Cost Management:**
- Each SMS = ~0.80 KES (~$0.006 USD)
- 100 farmers × 1 SMS/week × 4 weeks = 400 SMS/month = ~320 KES (~$2.50 USD)
- Very affordable! ✅

---

## 🐛 **Troubleshooting**

### **"SMS service not configured"**

**Fix:** Add secrets to Streamlit Cloud:
- Settings → Secrets → Paste config → Save

### **"SMS service initialized but not available"**

**Fix:** Check API key is correct:
- Must start with `atsk_`
- Copy/paste exactly from Africa's Talking dashboard

### **"Failed to send SMS"**

**Sandbox mode:** Phone must be registered
1. Go to Africa's Talking sandbox
2. Settings → SMS → Test Phone Numbers
3. Add your number
4. Try again

**Production mode:** Check account balance
- Dashboard → Account balance
- Top up if needed

### **Test SMS not arriving**

- ✅ Wait up to 2 minutes
- ✅ Check number format (+254712345678)
- ✅ Check phone is registered (sandbox)
- ✅ Check Africa's Talking logs (Dashboard → Logs)

---

## 📊 **Monitor Usage**

### **Africa's Talking Dashboard:**
- **Logs:** See all SMS sent
- **Balance:** Check remaining credits
- **Analytics:** Delivery rates, failed messages

### **Streamlit App:**
- Shows success/failure immediately
- Displays formatted phone number
- Preview before sending

---

## 🎉 **You're Done!**

SMS alerts are now LIVE in your Streamlit app!

**No local setup needed!**  
**No Python installation needed!**  
**Everything works in the cloud!** ☁️

---

## 📞 **Support**

**Africa's Talking:**
- Email: support@africastalking.com
- Phone: +254 20 524 2223

**Streamlit:**
- Docs: https://docs.streamlit.io/
- Community: https://discuss.streamlit.io/

**OpenResilience:**
- GitHub Issues: Report problems
- Email: [Your Email]

---

**Ready to send alerts?** Go to your app and click "📱 SMS Alert Service"! 🚀
