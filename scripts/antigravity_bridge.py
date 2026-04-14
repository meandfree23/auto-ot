import os
import sys
import json
import io
from pathlib import Path
import argparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from dotenv import load_dotenv

# V22.0 'Pure-Intel' Bridge: Connects Pipeline to Brain Engine with Real-Data Integration
# Downloads and reads content from PDF/Word files in Google Drive.

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

TOKEN_PATH = ROOT / "token.json"
SUMMARY_DIR = ROOT / "outputs" / "01_summaries"
DEEP_DIR = ROOT / "outputs" / "02_deep_analysis"
SCOPES = ["https://www.googleapis.com/auth/drive"]

def load_credentials() -> Credentials:
    """Load and refresh Google Drive credentials."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing {TOKEN_PATH}.")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
    return creds

def build_drive_service():
    """Build the Drive API service."""
    creds = load_credentials()
    return build("drive", "v3", credentials=creds)

def download_file(service, file_id: str, file_name: str) -> Path:
    """Download file from Google Drive to a temporary location."""
    temp_dir = ROOT / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / file_name
    
    print(f"[Bridge] Downloading file from Drive: {file_name} (ID: {file_id})")
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(str(file_path), "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.close()
    return file_path

def process_task(job_id: str, task_path_str: str):
    """Main entry point for REAL automated analysis."""
    print(f"[Bridge] Starting V22.0 'Pure-Intel' processing for Job ID: {job_id}")
    
    try:
        # 1. Load Task Data
        # unicodedata.normalize 로 macOS NFD/NFC 경로 충돌 방지
        import unicodedata
        task_path = Path(unicodedata.normalize("NFC", task_path_str))
        if not task_path.is_absolute():
            task_path = ROOT / unicodedata.normalize("NFC", task_path_str)

        task_data = json.loads(task_path.read_text(encoding="utf-8"))
        file_id = task_data.get("source", {}).get("file_id")
        file_name = task_data.get("source", {}).get("file_name", "document.pdf")
        
        if not file_id:
            print("[Bridge Error] No file_id found in task JSON.")
            return False

        # 2. Download Real Content
        service = build_drive_service()
        local_path = download_file(service, file_id, file_name)

        # 3. Extract Text and Analyze
        from scripts.brain_engine import extract_content, generate_reports
        
        content = extract_content(local_path)
        if not content or len(content.strip()) < 10:
            print("[Bridge Error] Failed to extract meaningful content from the document.")
            # Cleanup
            if local_path.exists(): local_path.unlink()
            return False

        print(f"[Bridge] Successfully extracted {len(content)} characters.")

        # 4. Generate Reports
        if generate_reports(job_id, content, file_name):
            print(f"[Bridge] Reports generated successfully.")
            if local_path.exists(): local_path.unlink()

            # HTML 생성은 Telegram 버튼(고도화 해줘)으로 수동 트리거됨
            return True

        if local_path.exists(): local_path.unlink()
        return False
        
    except Exception as e:
        print(f"[Bridge Error] V22.0 Processing failed: {e}")
        import traceback; traceback.print_exc()
        return False

def load_markdown(job_id: str):
    """Retrieve summary, deep, and question reports for a given job_id."""
    summary_path = SUMMARY_DIR / f"{job_id}_summary.md"
    deep_path = DEEP_DIR / f"{job_id}_deep_report.md"
    questions_path = ROOT / "outputs" / "questions" / f"{job_id}_questions.md"
    
    summary = summary_path.read_text(encoding="utf-8") if summary_path.exists() else None
    deep = deep_path.read_text(encoding="utf-8") if deep_path.exists() else None
    questions = questions_path.read_text(encoding="utf-8") if questions_path.exists() else None
    
    return summary, deep, questions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Strategic Bridge V22.0")
    parser.add_argument("command", nargs="?", default="process", help="Command")
    parser.add_argument("--task", help="Path to task JSON")
    parser.add_argument("--job-id", help="Explicit Job ID")
    
    args = parser.parse_args()
    
    if args.command == "process" and args.task and args.job_id:
        if process_task(args.job_id, args.task):
            sys.exit(0)
    sys.exit(1)
