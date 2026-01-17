# Vehicle Updates Dashboard

A real-time dashboard for displaying and managing vehicle service updates from Google Forms/Sheets.

## Features

- 📊 Real-time data display from Google Sheets
- ✏️ Editable cells for status, service, registration, advisor, and remarks
- 🔄 Auto-refresh every 15 seconds
- 📱 Fully responsive design
- 🖼️ Google Drive image support
- 🚀 Deployable on GitHub Pages (static) or Render (with backend)

## Deployment Options

### Option 1: GitHub Pages (Static Frontend Only)

**Best for**: Quick deployment, no backend required, but data won't update automatically.

1. Push your code to GitHub
2. In your GitHub repository:
   - Go to **Settings → Pages**
   - Under **Source**, choose `Deploy from a branch`
   - Select branch `main` (or `master`) and folder `/ (root)`
   - Save
3. After a few minutes, your site will be live at:
   - `https://YOUR_USERNAME.github.io/YOUR_REPO/`

**Note**: The GitHub Pages version runs in static mode (no backend calls), so it won't show live data. The page will load without errors.

### Option 2: Render (Full Stack with Backend)

**Best for**: Full functionality with live data updates from Google Sheets.

#### Prerequisites

1. **Google Sheets Setup**:
   - Create a Google Form that writes to a Google Sheet
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create a Service Account
   - Download the service account JSON key
   - Share your Google Sheet with the service account email (found in the JSON: `client_email`)

2. **Get your Spreadsheet ID**:
   - Open your Google Sheet
   - The URL looks like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part

#### Deploy to Render

1. **Push your code to GitHub** (make sure `service-account.json` is in `.gitignore`)

2. **Create a Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **New +** → **Web Service**
   - Connect your GitHub repository
   - Configure with these **EXACT** settings:
     - **Name**: `vehicle-dashboard-backend` (or your choice)
     - **Environment**: `Python 3`
     - **Root Directory**: `backend` ⚠️ **IMPORTANT: Set this to "backend"**
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
   
   **Note**: By setting Root Directory to `backend`, all commands run from the backend folder, so you don't need `cd backend &&` in the commands.

3. **Set Environment Variables on Render**:
   - Go to your Render service → **Environment**
   - Add these variables:
     - `SPREADSHEET_ID`: Your Google Spreadsheet ID (e.g., `1QHvyqRMowVCwWi2-WR2IEjIoTSR613bf1ve1waH6Reo`)
     - `GOOGLE_SERVICE_ACCOUNT_JSON`: Paste the entire contents of your `service-account.json` file as a single line JSON string
       - Tip: Copy the entire JSON file, remove all line breaks, and paste it as the value

4. **Deploy**:
   - Render will automatically build and deploy your service
   - Wait for deployment to complete
   - Your backend will be available at: `https://your-service-name.onrender.com`

5. **Update Frontend (if using separate frontend)**:
   - If you want to host the frontend separately (e.g., on GitHub Pages), update `index.html`:
     - Set `API_BASE` to your Render backend URL
     - Set `ENABLE_LIVE = true`

#### Render Environment Variables

```
SPREADSHEET_ID=your-spreadsheet-id-here
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"...",...}
```

**Important**: The `GOOGLE_SERVICE_ACCOUNT_JSON` must be the entire JSON object as a single-line string (no line breaks).

## Local Development

### Prerequisites

- Python 3.8+
- pip
- Google Sheets API credentials (service account JSON file)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd popular
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets**:
   - Place your `service-account.json` file in the `backend/` directory
   - Update `SPREADSHEET_ID` in `backend/app.py` (or set `SPREADSHEET_ID` environment variable)
   - Share your Google Sheet with the service account email

4. **Run the backend**:
   ```bash
   cd backend
   python app.py
   ```

5. **Access the dashboard**:
   - Open `http://localhost:5000` in your browser
   - The dashboard will automatically fetch data from Google Sheets

## Project Structure

```
popular/
├── backend/
│   ├── app.py             # Flask backend
│   ├── requirements.txt   # Python dependencies
│   ├── Procfile          # Heroku deployment config (optional)
│   ├── service-account.json  # Google service account (NOT in git, local only)
│   └── templates/
│       └── index.html     # Frontend served by Flask (displays all form data)
├── .gitignore           # Git ignore file
├── README.md            # This file
├── QUICK_START.md       # Quick deployment guide
└── GITHUB_PUSH_STEPS.md # GitHub push instructions
```

## Google Sheets Integration

### Required Google Sheets Setup

1. **Create a Google Form** that collects:
   - Timestamp (automatic)
   - Email (automatic)
   - Current Status
   - Current Service
   - Registration Number
   - Name of Service Advisor
   - Remarks
   - Vehicle Image (Google Drive link)

2. **Create a Google Sheet** linked to the form (Form Responses sheet)

3. **Set up Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing
   - Enable Google Sheets API
   - Create a Service Account
   - Download the JSON key file
   - Copy the service account email (from JSON: `client_email`)

4. **Share the Google Sheet**:
   - Open your Google Sheet
   - Click **Share**
   - Add the service account email with **Editor** permissions
   - This allows the backend to read and update the sheet

### Troubleshooting Google Sheets

If you see errors like "Permission denied" or "Spreadsheet not found":

1. **Check Service Account**:
   - Verify the service account JSON is valid
   - Ensure the service account email is shared on the Google Sheet

2. **Check Spreadsheet ID**:
   - Verify the `SPREADSHEET_ID` matches your Google Sheet URL
   - Format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

3. **Check API Access**:
   - Ensure Google Sheets API is enabled in your Google Cloud Project
   - Verify the service account has the correct permissions

4. **Create New Sheet/Form**:
   - If issues persist, create a new Google Form and Sheet
   - Follow the setup steps again with the new spreadsheet ID

## API Endpoints

When running with the Flask backend:

- `GET /` - Serve the dashboard HTML
- `GET /api/responses` - Get latest 9 responses from Google Sheets
- `POST /api/update-cell` - Update a cell in Google Sheets
  - Body: `{"rowIndex": int, "colIndex": int, "value": string}`

## Troubleshooting

### "Unable to load data. Please check the server."

- **GitHub Pages**: This is expected - GitHub Pages runs in static mode without a backend
- **Render/Local**: 
  - Check if backend is running
  - Verify environment variables are set correctly
  - Check Render logs for errors
  - Verify Google Sheets API credentials

### Backend fails to start on Render

- Check `requirements.txt` has all dependencies
- Verify `Procfile` or `startCommand` is correct
- Check Render logs for specific error messages
- Ensure Python version is compatible (3.8+)

### Google Sheets not updating

- Verify service account has Editor permissions on the sheet
- Check spreadsheet ID is correct
- Ensure Google Sheets API is enabled
- Check backend logs for API errors

## License

This project is open source and available under the MIT License.
