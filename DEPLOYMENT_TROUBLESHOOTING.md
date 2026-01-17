# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Errors and Solutions

### 1. **ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'**

**Cause:** Render cannot find `requirements.txt` because:
- File is not committed to GitHub
- Root Directory is not set correctly in Render dashboard
- File is in wrong location

**Solutions:**

#### ✅ Solution A: Commit Files to GitHub (REQUIRED)
```powershell
# Check what needs to be committed
git status

# Add backend files
git add backend/requirements.txt
git add backend/app.py
git add backend/templates/index.html
git add backend/Procfile

# Or add everything
git add .

# Commit
git commit -m "Fix: Add all backend files for Render deployment"

# Push to GitHub
git push origin main
```

#### ✅ Solution B: Verify Render Dashboard Settings
In Render Dashboard → Web Service → Settings:
- **Root Directory**: Must be set to `backend` (not empty, not `/backend`)
- **Build Command**: `pip install -r requirements.txt` (not `cd backend && ...`)
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`

#### ✅ Solution C: Verify File Location
The file structure must be:
```
your-repo/
└── backend/
    ├── requirements.txt  ← Must exist here
    ├── app.py
    └── templates/
        └── index.html
```

---

### 2. **ModuleNotFoundError or ImportError**

**Cause:** Dependencies not installed or missing from `requirements.txt`

**Solutions:**
- Check `backend/requirements.txt` contains all packages:
  ```
  flask==3.0.3
  flask-cors==4.0.0
  google-api-python-client==2.153.0
  google-auth==2.35.0
  google-auth-httplib2==0.2.0
  google-auth-oauthlib==1.2.1
  gunicorn==23.0.0
  ```
- Verify build command runs: `pip install -r requirements.txt`
- Check Render build logs for installation errors

---

### 3. **Google Sheets API Connection Errors**

#### Error: "Permission denied" or "403 Forbidden"

**Causes:**
- Service account email not shared on Google Sheet
- Service account doesn't have Editor permission
- GOOGLE_SERVICE_ACCOUNT_JSON environment variable missing or invalid

**Solutions:**

1. **Share Google Sheet with Service Account:**
   - Open your Google Sheet
   - Click **Share** button (top right)
   - Add the service account email (from JSON file: `client_email`)
   - Set permission to **Editor** (not Viewer)
   - Click **Send**

2. **Verify Environment Variable:**
   - Render Dashboard → Your Service → Environment
   - Check `GOOGLE_SERVICE_ACCOUNT_JSON` exists
   - Value must be valid JSON (entire file contents as one line)
   - Remove all line breaks and extra spaces
   - Example format: `{"type":"service_account","project_id":"...","private_key_id":"...",...}`

3. **Verify JSON is Valid:**
   - Use online JSON validator: https://jsonlint.com/
   - Paste the entire `service-account.json` content
   - Ensure no trailing commas or syntax errors

---

#### Error: "Spreadsheet not found" or "Unable to parse range"

**Causes:**
- SPREADSHEET_ID is incorrect
- Sheet name doesn't match (default is "Form Responses 1")
- Range format is wrong

**Solutions:**

1. **Get Correct Spreadsheet ID:**
   - Open your Google Sheet
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part (long alphanumeric string)

2. **Verify Sheet Name:**
   - In Google Sheets, check the sheet tab name at bottom
   - Default: `Form Responses 1`
   - In `app.py`, `RANGE_NAME = "Form Responses 1!A:Z"`
   - If different, update `RANGE_NAME` in `app.py`

3. **Set SPREADSHEET_ID Environment Variable:**
   - Render Dashboard → Environment
   - Add: `SPREADSHEET_ID` = `your-actual-spreadsheet-id`

---

#### Error: "Google Sheets API not enabled"

**Solutions:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Navigate to **APIs & Services** → **Library**
4. Search for "Google Sheets API"
5. Click **Enable**

---

### 4. **Flask Application Errors**

#### Error: "TemplateNotFound: index.html"

**Cause:** Templates folder not found or wrong path

**Solution:**
- Ensure `backend/templates/index.html` exists
- Flask automatically looks in `templates/` folder relative to app.py
- Structure must be:
  ```
  backend/
  ├── app.py
  └── templates/
      └── index.html
  ```

#### Error: "Address already in use" or Port errors

**Cause:** Render sets PORT automatically, app must use `$PORT`

**Solution:**
- Start command must be: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Never hardcode port numbers (like `:5000`)

---

### 5. **Gunicorn/WSCGI Errors**

#### Error: "Failed to find application object 'app' in 'app'"

**Cause:** 
- `app.py` file name or Flask instance name is wrong
- Start command is incorrect

**Solution:**
- Ensure file is named `app.py` (not `application.py`)
- Ensure Flask instance is named `app`: `app = Flask(__name__)`
- Start command: `gunicorn app:app` (first `app` = filename, second `app` = Flask instance)

---

### 6. **CORS Errors (Frontend can't connect to backend)**

**Error:** "Access to fetch at '...' from origin '...' has been blocked by CORS policy"

**Cause:** CORS not enabled in Flask app

**Solution:**
- Already enabled in `app.py`: `CORS(app)`
- If still seeing errors, check:
  - Frontend URL is correct
  - API_BASE in index.html points to Render URL
  - Backend is actually running (not sleeping)

---

### 7. **Render Service Sleeps (Free Tier)**

**Symptoms:**
- First request after 15 minutes takes 30+ seconds
- Service appears "down" but actually sleeping

**Solutions:**
- Wait 30 seconds for first request (normal for free tier)
- Upgrade to paid plan for always-on service
- Or: Add uptime monitoring service (UptimeRobot) to ping every 14 minutes

---

### 8. **Environment Variables Not Loading**

**Error:** Variables show as empty or None

**Solutions:**
1. **Verify in Render Dashboard:**
   - Go to your service → Environment
   - Variables should be listed with checkmarks
   - Values are hidden (for security)

2. **Redeploy After Adding Variables:**
   - After adding/modifying environment variables
   - Click **Manual Deploy** → **Deploy latest commit**
   - Variables are loaded at build/start time

3. **Check Variable Names:**
   - Must be exactly: `SPREADSHEET_ID` and `GOOGLE_SERVICE_ACCOUNT_JSON`
   - Case-sensitive
   - No spaces or extra characters

---

## ✅ Pre-Deployment Checklist

Before deploying to Render, ensure:

- [ ] All files committed to GitHub:
  - [ ] `backend/requirements.txt`
  - [ ] `backend/app.py`
  - [ ] `backend/templates/index.html`
  - [ ] `backend/Procfile`
- [ ] `.gitignore` excludes:
  - [ ] `backend/service-account.json` (sensitive file)
  - [ ] `.venv/` (virtual environment)
- [ ] Google Cloud setup:
  - [ ] Google Sheets API enabled
  - [ ] Service account created
  - [ ] JSON key downloaded (local only)
  - [ ] Service account email shared on Google Sheet (Editor permission)
- [ ] Render Dashboard settings:
  - [ ] Root Directory: `backend`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
  - [ ] Environment Variables:
    - [ ] `SPREADSHEET_ID` (your spreadsheet ID)
    - [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` (entire JSON as one line)

---

## 🔍 How to Debug Render Deployment

### Check Build Logs:
1. Render Dashboard → Your Service → **Logs**
2. Look for build errors (red text)
3. Common issues:
   - `ERROR: Could not find a version that satisfies...` → Package version issue
   - `ModuleNotFoundError` → Missing package in requirements.txt
   - `FileNotFoundError` → Wrong file path or missing file

### Check Runtime Logs:
1. Render Dashboard → Your Service → **Logs** (after build)
2. Look for application errors
3. Common issues:
   - `Permission denied` → Google Sheets sharing issue
   - `JSONDecodeError` → Invalid GOOGLE_SERVICE_ACCOUNT_JSON
   - `404 Not Found` → Route/endpoint not defined

### Test Locally First:
```powershell
cd backend
python app.py
# Open http://localhost:5000
# Check if it works locally before deploying
```

---

## 📞 Still Having Issues?

1. **Check Render Logs:** Most detailed error info
2. **Verify File Structure:** Must match expected layout
3. **Test Environment Variables:** Use local testing
4. **Google Cloud Console:** Verify API enabled and service account permissions
5. **GitHub Repository:** Ensure all files are committed and pushed

---

**Last Updated:** Check that all files are in correct locations and committed to git before deploying!
