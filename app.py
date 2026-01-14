from flask import Flask, jsonify, render_template, request, send_from_directory
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SPREADSHEET_ID = "1QHvyqRMowVCwWi2-WR2IEjIoTSR613bf1ve1waH6Reo"
RANGE_NAME = "Form Responses 1!A:Z"

# Path to service account JSON (can be overridden by env var)
SERVICE_ACCOUNT_FILE = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", "service-account.json"
)

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Serve logo from backend folder
@app.route('/static/logo.png')
def serve_logo():
    return send_from_directory(os.path.dirname(__file__), 'logo.png')


def get_sheets_service(readonly: bool = True):
    """
    Build and return a Google Sheets API service using a service account.
    Share the sheet with the service account email.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
        if readonly
        else "https://www.googleapis.com/auth/spreadsheets"
    ]

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
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
    service = get_sheets_service(readonly=True)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
    ).execute()
    values = result.get("values", [])

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

        # Skip timestamp + email columns (first two columns)
    # Also filter out "washing" and "mode" columns
    columns_to_exclude = {"washing", "mode"}  # case-insensitive matching
    
    trimmed_rows = []
    trimmed_headers = []
    sheet_row_indices = []
    
    for offset, row in enumerate(last_rows):
        filtered_row = []
        filtered_headers = []
        for col_idx, header in enumerate(headers[2:], start=2):  # Start from column 2 (skip timestamp + email)
            header_lower = header.strip().lower() if header else ""
            # Skip columns that match "washing" or "mode" (case-insensitive)
            if header_lower not in columns_to_exclude:
                filtered_headers.append(header)
                # Get the cell value, handling cases where row might be shorter
                cell_value = row[col_idx] if col_idx < len(row) else ""
                filtered_row.append(cell_value)
        
        # Only set trimmed_headers once (they're the same for all rows)
        if not trimmed_headers:
            trimmed_headers = filtered_headers
        
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
        row_index = int(payload.get("rowIndex"))
        col_index = int(payload.get("colIndex"))
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
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


