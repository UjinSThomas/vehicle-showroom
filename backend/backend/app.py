from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "17XpNqUCANkaJBjOvEnPct3fr3q3SaNXD13zuTcCQsEQ")
RANGE_NAME = "Form Responses 1!A:Z"

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for all routes

# Serve logo from backend folder
@app.route('/static/logo.png')
def serve_logo():
    return send_from_directory(os.path.dirname(__file__), 'logo.png')


def get_sheets_service(readonly: bool = True):
    """
    Build and return a Google Sheets API service using a service account.
    Share the sheet with the service account email.
    Supports both file path and environment variable (JSON string) for service account.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
        if readonly
        else "https://www.googleapis.com/auth/spreadsheets"
    ]

    # Try to get service account from environment variable first (for Render)
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
        try:
            # Parse JSON string from environment variable
            service_account_info = json.loads(service_account_json)
            creds = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=scopes,
            )
        except json.JSONDecodeError:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON must be valid JSON")
    else:
        # Fall back to file path (for local development)
        service_account_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
        if not os.path.exists(service_account_file):
            raise FileNotFoundError(
                f"Service account file not found: {service_account_file}. "
                "Set GOOGLE_SERVICE_ACCOUNT_JSON environment variable or provide service-account.json file."
            )
        creds = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=scopes,
        )
    
    return build("sheets", "v4", credentials=creds)


@app.route("/")
def index():
    """
    Serve the dashboard HTML.
    The page uses JS to call /api/responses every few seconds.
    """
    return render_template("index.html")


@app.get("/api/responses")
def get_responses():
    """
    Return the latest responses from the Google Sheet as JSON.
    Shows ALL columns except Timestamp.
    """
    try:
        service = get_sheets_service(readonly=True)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
        ).execute()
        values = result.get("values", [])
        
        print(f"DEBUG: Fetched {len(values)} rows from sheet")
        
    except Exception as e:
        print(f"ERROR: Failed to fetch data: {str(e)}")
        return jsonify({"error": f"Failed to fetch data from Google Sheets: {str(e)}"}), 500

    if not values:
        return jsonify({"headers": [], "rows": []})

    # First row is headers
    all_headers = values[0]
    all_data_rows = values[1:]
    
    print(f"DEBUG: All headers: {all_headers}")

    # Skip ONLY Timestamp (column A, index 0)
    # Show EVERYTHING else including VEHICLE IMAGE, Email, etc.
    headers_to_show = all_headers[1:]  # Start from index 1 (skip only Timestamp)
    
    print(f"DEBUG: Headers to display: {headers_to_show}")

    rows_to_show = []
    row_indices = []
    
    for row_idx, row in enumerate(all_data_rows):
        # Skip only first column (Timestamp)
        row_data = []
        for col_idx in range(1, len(all_headers)):
            cell_value = row[col_idx] if col_idx < len(row) else ""
            row_data.append(cell_value)
        
        rows_to_show.append(row_data)
        row_indices.append(row_idx + 2)  # +2 because row 1 is header

    # Column mapping: display column index -> actual sheet column (1-based)
    column_mapping = {}
    for display_idx in range(len(headers_to_show)):
        column_mapping[display_idx] = display_idx + 2  # +2 because we skip column A(1)

    return jsonify({
        "headers": headers_to_show,
        "rows": rows_to_show,
        "rowIndices": row_indices,
        "columnMapping": column_mapping,
    })


@app.post("/api/update-cell")
def update_cell():
    """
    Update a single cell in the Google Sheet.
    Expects JSON body: { "rowIndex": <int>, "colIndex": <int>, "value": <str> }
    - rowIndex and colIndex are 1-based sheet coordinates.
    """
    try:
        payload = request.get_json(force=True, silent=False)
        if not payload:
            return jsonify({"success": False, "error": "No payload provided"}), 400
        
        row_index = int(payload.get("rowIndex", 0))
        col_index = int(payload.get("colIndex", 0))
        value = payload.get("value", "")

        if row_index < 1 or col_index < 1:
            return jsonify({"success": False, "error": "Invalid indices"}), 400

        service = get_sheets_service(readonly=False)
        sheet = service.spreadsheets()
        range_a1 = f"Form Responses 1!R{row_index}C{col_index}"

        body = {"values": [[value]]}
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_a1,
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"success": False, "error": f"Invalid input: {str(e)}"}), 400
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)