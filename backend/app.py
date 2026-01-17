from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "1BwVVuz6g3YQFX1WZcY_OPbfs6vKaUH1CaEu5bjB1sYM")
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
    This mimics your Apps Script generateTableHTML data, but in JSON form.
    """
    try:
        service = get_sheets_service(readonly=True)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
        ).execute()
        values = result.get("values", [])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data from Google Sheets: {str(e)}"}), 500

    if not values:
        return jsonify({"headers": [], "rows": []})

    headers = values[0]
    data_rows = values[1:]

    # Last 9 entries (like your Apps Script)
    last_rows = data_rows[-9:] if len(data_rows) > 9 else data_rows

    # Calculate the starting sheet row index (1-based, including header row)
    # Header is row 1, data_rows[0] is row 2, so:
    start_data_index = len(data_rows) - len(last_rows)  # 0-based index into data_rows
    start_sheet_row = 2 + start_data_index

    # Skip timestamp + email columns (first two columns: A and B)
    # Keep all other columns from column C onwards
    trimmed_rows = []
    trimmed_headers = []
    sheet_row_indices = []
    
    # Extract headers starting from column C (index 2)
    trimmed_headers = headers[2:] if len(headers) > 2 else []
    
    for offset, row in enumerate(last_rows):
        filtered_row = []
        # Start from column C (index 2), skip timestamp and email
        for col_idx in range(2, len(headers)):
            # Get the cell value, handling cases where row might be shorter
            cell_value = row[col_idx] if col_idx < len(row) else ""
            filtered_row.append(cell_value)
        
        trimmed_rows.append(filtered_row)
        sheet_row_indices.append(start_sheet_row + offset)

    return jsonify(
        {
            "headers": trimmed_headers,
            "rows": trimmed_rows,
            "rowIndices": sheet_row_indices,  # actual sheet row numbers
        }
    )


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


