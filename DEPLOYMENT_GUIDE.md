# 🚀 Complete Deployment Guide - Vehicle Dashboard

## ✅ What's Already Updated

- ✅ Spreadsheet ID updated to: `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`
- ✅ Code updated to work with your new Google Sheet structure
- ✅ All files ready for deployment

## 📋 Step-by-Step Deployment Instructions

### STEP 1: Prepare Your Google Sheets Service Account

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create or Select a Project**
   - Click "Select a project" → "New Project"
   - Name it (e.g., "vehicle-dashboard")
   - Click "Create"

3. **Enable Google Sheets API**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

4. **Create Service Account**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name: `vehicle-dashboard-service`
   - Click "Create and Continue"
   - Skip role assignment → Click "Done"

5. **Create and Download Key**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Click "Create" (file downloads automatically)
   - **IMPORTANT**: Save this file as `service-account.json` in your `backend/` folder

6. **Share Google Sheet with Service Account**
   - Open your Google Sheet: https://docs.google.com/spreadsheets/d/1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM/edit
   - Click "Share" button (top right)
   - Open the downloaded `service-account.json` file
   - Find the `client_email` field (looks like: `vehicle-dashboard@project-name.iam.gserviceaccount.com`)
   - Copy that email address
   - Paste it in the "Share" dialog
   - Give it **Editor** permissions
   - Click "Send" (you can uncheck "Notify people")

---

### STEP 2: Push to GitHub

1. **Open Terminal/PowerShell in your project folder**
   ```powershell
   cd C:\Users\ujins\OneDrive\Desktop\popular
   ```

2. **Check Git Status**
   ```powershell
   git status
   ```

3. **Add All Files**
   ```powershell
   git add .
   ```

4. **Commit Changes**
   ```powershell
   git commit -m "Update for new Google Sheet and prepare for Render deployment"
   ```

5. **Push to GitHub**
   ```powershell
   git push origin main
   ```
   (If your branch is `master`, use `git push origin master`)

**⚠️ IMPORTANT**: Make sure `backend/service-account.json` is in `.gitignore` (it should be already)

---

### STEP 3: Deploy to Render (New Account)

1. **Sign up/Login to Render**
   - Go to [render.com](https://render.com)
   - Sign up with a new account (or login if you have one)
   - Verify your email if needed

2. **Connect GitHub Repository**
   - In Render dashboard, click "New +" → "Web Service"
   - Click "Connect account" if not connected
   - Authorize Render to access your GitHub
   - Select your repository (`popular` or whatever you named it)

3. **Configure Web Service**
   - **Name**: `vehicle-dashboard-backend` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or `master`)
   - **Root Directory**: Leave empty (or set to `backend` if needed)
   - **Build Command**: 
     ```
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
     ```

4. **Set Environment Variables**
   - Scroll down to "Environment Variables"
   - Click "Add Environment Variable"
   
   **Add Variable 1:**
   - **Key**: `SPREADSHEET_ID`
   - **Value**: `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`
   - Click "Save"
   
   **Add Variable 2:**
   - **Key**: `GOOGLE_SERVICE_ACCOUNT_JSON`
   - **Value**: Open your `backend/service-account.json` file
   - Copy the ENTIRE contents
   - Remove ALL line breaks (make it one long line)
   - Paste it as the value
   - **Example format** (all on one line):
     ```
     {"type":"service_account","project_id":"...","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"...","universe_domain":"googleapis.com"}
     ```
   - Click "Save"

5. **Deploy**
   - Scroll to bottom
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - You'll see build logs in real-time

6. **Get Your Backend URL**
   - Once deployed, Render will show your service URL
   - It will look like: `https://vehicle-dashboard-backend.onrender.com`
   - **Copy this URL** - you'll need it!

---

### STEP 4: Test Your Deployment

1. **Visit Your Render URL**
   - Open: `https://your-service-name.onrender.com`
   - You should see the dashboard

2. **Check for Errors**
   - If you see "Unable to load data", check Render logs:
     - Go to your service in Render dashboard
     - Click "Logs" tab
     - Look for error messages

3. **Common Issues & Fixes**

   **Issue: "Permission denied" or "Spreadsheet not found"**
   - ✅ Check that service account email is shared on Google Sheet
   - ✅ Verify `SPREADSHEET_ID` is correct
   - ✅ Check `GOOGLE_SERVICE_ACCOUNT_JSON` is valid JSON (one line)

   **Issue: "Module not found"**
   - ✅ Check `requirements.txt` has all dependencies
   - ✅ Check build logs for installation errors

   **Issue: Service crashes on startup**
   - ✅ Check Render logs for specific error
   - ✅ Verify `Procfile` or start command is correct
   - ✅ Check Python version compatibility

---

### STEP 5: (Optional) Deploy Frontend to GitHub Pages

If you want a static frontend on GitHub Pages:

1. **Go to GitHub Repository**
2. **Settings → Pages**
3. **Source**: Deploy from branch
4. **Branch**: `main` / `root`
5. **Save**
6. **Wait 2-3 minutes**
7. **Visit**: `https://YOUR_USERNAME.github.io/YOUR_REPO/`

**Note**: GitHub Pages version will be static (no live data) unless you configure it to point to your Render backend.

---

## 📝 Quick Reference

### Your Google Sheet
- **URL**: https://docs.google.com/spreadsheets/d/1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM/edit
- **Form**: https://forms.gle/CuhyBAs4epcnSf9w8
- **Spreadsheet ID**: `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`

### Render Environment Variables Needed
```
SPREADSHEET_ID=1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM
GOOGLE_SERVICE_ACCOUNT_JSON={entire JSON as one line}
```

### Files Structure
```
popular/
├── index.html              # Frontend for GitHub Pages
├── backend/
│   ├── app.py              # Flask backend (✅ Updated)
│   ├── requirements.txt    # Dependencies
│   ├── Procfile           # Render config
│   ├── templates/
│   │   └── index.html     # Frontend for Flask
│   └── service-account.json # Local only (NOT in git)
├── render.yaml            # Render deployment config
├── .gitignore             # Excludes service-account.json
└── README.md              # Documentation
```

---

## ✅ Checklist Before Deploying

- [ ] Google Sheets API enabled
- [ ] Service account created and JSON downloaded
- [ ] Google Sheet shared with service account email
- [ ] `service-account.json` in `.gitignore`
- [ ] Code pushed to GitHub
- [ ] Render account created/ready
- [ ] Environment variables set in Render
- [ ] Deployment successful
- [ ] Dashboard loads and shows data

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Render Logs**: Service → Logs tab
2. **Check Google Sheets**: Verify service account has access
3. **Verify Environment Variables**: Double-check in Render dashboard
4. **Test Locally First**: Run `cd backend && python app.py` to test

---

## 🎉 You're Done!

Once deployed, your dashboard will:
- ✅ Fetch data from Google Sheets every 15 seconds
- ✅ Allow editing of status, service, registration, advisor, and remarks
- ✅ Display vehicle images from Google Drive
- ✅ Work on any device (responsive design)

**Your Render URL**: `https://your-service-name.onrender.com`

Enjoy your live dashboard! 🚀
