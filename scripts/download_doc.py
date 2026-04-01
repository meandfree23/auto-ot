import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

# High-fidelity download script for docx
ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = ROOT / "token.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

def download_file(file_id: str, dest_path: str):
    load_dotenv()
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    service = build("drive", "v3", credentials=creds)
    
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

if __name__ == "__main__":
    file_id = "1aId4X1iagwe8F1q0PXb47RosPjk2O3Rs"
    download_file(file_id, "tmp_jeil.docx")
