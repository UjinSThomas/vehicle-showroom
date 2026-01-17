# ⚡ Quick Start - Everything You Need

## ✅ What's Already Done

1. ✅ **Spreadsheet ID Updated**: `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`
2. ✅ **Code Updated**: Works with your new Google Sheet structure
3. ✅ **Editable Columns**: Updated to match your sheet headers:
   - CURRENT STATUS
   - SERVICE
   - Registration Number
   - Name of Service Advisor
4. ✅ **All Files Ready**: Template files, Procfile, requirements.txt all set

## 🚀 3 Simple Steps to Deploy

### 1️⃣ Push to GitHub (5 minutes)
See `GITHUB_PUSH_STEPS.md` for exact commands.

**Quick version:**
```powershell
cd C:\Users\ujins\OneDrive\Desktop\popular
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2️⃣ Set Up Google Service Account (10 minutes)
See `DEPLOYMENT_GUIDE.md` Step 1 for details.

**Quick checklist:**
- [ ] Create Google Cloud project
- [ ] Enable Google Sheets API
- [ ] Create service account
- [ ] Download JSON key → save as `backend/service-account.json`
- [ ] Share Google Sheet with service account email (Editor permission)

### 3️⃣ Deploy to Render (15 minutes)

**IMPORTANT:** Configure Render manually through the dashboard (render.yaml is not used).

**Quick checklist:**
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Create Web Service with these **EXACT** settings:
  - **Name**: `vehicle-dashboard-backend`
  - **Environment**: `Python 3`
  - **Root Directory**: `backend` ⚠️ **Set this to "backend"**
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
- [ ] Set Environment Variables (in Render dashboard → Environment):
  - `SPREADSHEET_ID` = `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`
  - `GOOGLE_SERVICE_ACCOUNT_JSON` = (entire JSON file as one line, remove all line breaks)
- [ ] Deploy and wait

## 📋 Your Links

- **Google Form**: https://forms.gle/CuhyBAs4epcnSf9w8
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM/edit
- **Spreadsheet ID**: `1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM`

## 🎯 What You'll Get

After deployment, your dashboard will:
- ✅ Show last 9 vehicle entries from Google Sheets
- ✅ Auto-refresh every 15 seconds
- ✅ Allow editing of: Status, Service, Registration, Advisor
- ✅ Display vehicle images from Google Drive
- ✅ Work on mobile and desktop

## 📚 Full Documentation

- **`DEPLOYMENT_GUIDE.md`**: Complete step-by-step guide
- **`GITHUB_PUSH_STEPS.md`**: Quick GitHub commands
- **`README.md`**: Full project documentation

## ⚠️ Important Notes

1. **Service Account JSON**: 
   - Keep `backend/service-account.json` local only
   - For Render: Copy entire JSON as one line in environment variable
   - Make sure it's in `.gitignore` (already done)

2. **Render Free Tier**:
   - Services sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds
   - Consider upgrading for always-on service

3. **Google Sheets**:
   - Service account must have Editor access
   - Check service account email in JSON file
   - Share sheet with that email address

## 🆘 Troubleshooting

**"Unable to load data" error:**
- Check Render logs for specific error
- Verify service account is shared on Google Sheet
- Check environment variables are set correctly

**Service won't start:**
- Check Render logs
- Verify build command and start command
- Check Python version compatibility

**Can't edit cells:**
- Verify column names match exactly (case-sensitive)
- Check Render logs for update errors
- Verify service account has Editor permission

## ✅ Final Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] Service account JSON downloaded
- [ ] Google Sheet shared with service account
- [ ] Render account ready
- [ ] Environment variables prepared

After deploying:
- [ ] Dashboard loads without errors
- [ ] Data appears from Google Sheets
- [ ] Can edit cells successfully
- [ ] Images display correctly

---

**Need help?** Check `DEPLOYMENT_GUIDE.md` for detailed instructions!
