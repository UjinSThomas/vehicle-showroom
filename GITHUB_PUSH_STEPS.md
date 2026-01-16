# 📤 Quick GitHub Push Steps

## Step-by-Step Commands

Open PowerShell in your project folder and run these commands:

```powershell
# 1. Navigate to project folder
cd C:\Users\ujins\OneDrive\Desktop\popular

# 2. Check current status
git status

# 3. Add all files (except those in .gitignore)
git add .

# 4. Commit changes
git commit -m "Update for new Google Sheet (ID: 1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM) and prepare for Render deployment"

# 5. Push to GitHub
git push origin main
```

**If you get an error about branch name:**
- If it says "master" instead of "main", use: `git push origin master`
- Or check your branch: `git branch`

**If you need to set up Git for the first time:**
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**If repository doesn't exist on GitHub yet:**
1. Go to github.com
2. Click "New repository"
3. Name it (e.g., "vehicle-dashboard")
4. Don't initialize with README
5. Copy the repository URL
6. Run: `git remote add origin YOUR_REPO_URL`
7. Then: `git push -u origin main`

---

## ✅ Verify Before Pushing

Make sure these files are NOT being committed:
- ❌ `backend/service-account.json` (should be in .gitignore)

Check with:
```powershell
git status
```

If `service-account.json` shows up, it's not in .gitignore. Check `.gitignore` file.
