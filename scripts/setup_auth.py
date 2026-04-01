from __future__ import annotations

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = ROOT / "credentials.json"
TOKEN_PATH = ROOT / "token.json"

def main():
    """
    Grabs user credentials from the browser to create token.json.
    Requires credentials.json to be present in the root.
    """
    if not CREDENTIALS_PATH.exists():
        print(f"Error: {CREDENTIALS_PATH} not found.")
        print("Please download your OAuth 2.0 Client ID Credentials (JSON) from Google Cloud Console and save it as 'credentials.json' in the project root.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    print(f"Successfully saved credentials to {TOKEN_PATH}")

if __name__ == "__main__":
    main()
