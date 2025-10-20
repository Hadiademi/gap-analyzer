# 🔐 User Credentials - Gap Analyzer

## 📋 **ACCESS CONTROL PËR 10 PERSONA**

### **👤 ADMINISTRATOR:**
- **Username:** `admin`
- **Password:** `password`
- **Access:** Full access to all features

### **👥 CLIENTS (1-10):**
- **Username:** `client1` - `client10`
- **Password:** `client1` - `client10` (same as username)
- **Access:** Full access to gap analysis and regulatory repository

---

## 🔑 **CREDENTIALS LIST:**

| Username | Password | Role |
|----------|----------|------|
| admin | password | Administrator |
| client1 | client1 | Client |
| client2 | client2 | Client |
| client3 | client3 | Client |
| client4 | client4 | Client |
| client5 | client5 | Client |
| client6 | client6 | Client |
| client7 | client7 | Client |
| client8 | client8 | Client |
| client9 | client9 | Client |
| client10 | client10 | Client |

---

## 🛡️ **SECURITY FEATURES:**

### **✅ Authentication:**
- ✅ Login required before access
- ✅ Password hashing (SHA256)
- ✅ Session management
- ✅ Logout functionality

### **✅ Access Control:**
- ✅ Only authorized users can access
- ✅ User session tracking
- ✅ Secure logout

---

## 📱 **HOW TO USE:**

### **1. Login:**
- Go to the application URL
- Enter username and password
- Click "Login"

### **2. Use Application:**
- Access Regulatory Repository
- Perform Gap Analysis
- Download Excel reports

### **3. Logout:**
- Click "Logout" button
- Session ends

---

## 🔧 **CUSTOMIZATION:**

### **To change passwords:**
1. Edit `modules/auth.py`
2. Update the `USERS` dictionary
3. Use SHA256 hash for new passwords

### **To add more users:**
1. Add new username/password pairs to `USERS` dictionary
2. Hash passwords using SHA256

---

**Status:** Ready for deployment with authentication
**Last Updated:** October 2025
