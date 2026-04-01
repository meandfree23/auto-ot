from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state"
TASK_DIR = ROOT / "incoming_tasks" / "tasks"
STATE_DIR.mkdir(parents=True, exist_ok=True)
TASK_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_PATH = ROOT / "token.json"
PAGE_TOKEN_PATH = STATE_DIR / "drive_start_page_token.txt"

# Configuration from environment (set in .env)
WATCH_FOLDER_ID = os.environ.get("WATCH_FOLDER_ID")
DEFAULT_PROJECT_TYPE = os.environ.get("DEFAULT_PROJECT_TYPE", "brand_film")
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "ko")
POLL_INTERVAL_SECONDS = int(os.environ.get("DRIVE_POLL_SECONDS", "60"))


def load_credentials() -> Credentials:
    """Load and refresh Google Drive credentials."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing {TOKEN_PATH}. Please follow authentication instructions.")
        
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def build_drive_service():
    """Build the Drive API service."""
    creds = load_credentials()
    return build("drive", "v3", credentials=creds)


def get_saved_page_token(service) -> str:
    """Get the start page token if not already saved."""
    if PAGE_TOKEN_PATH.exists():
        return PAGE_TOKEN_PATH.read_text(encoding="utf-8").strip()
    
    token_resp = service.changes().getStartPageToken(supportsAllDrives=True).execute()
    token = token_resp["startPageToken"]
    save_page_token(token)
    return token


def save_page_token(token: str) -> None:
    """Save the current page token."""
    PAGE_TOKEN_PATH.write_text(token, encoding="utf-8")


def is_target_file(file_obj: dict[str, Any]) -> bool:
    """Filter changes for relevant files in the watched folder."""
    if not file_obj or file_obj.get("trashed"):
        return False

    parents = file_obj.get("parents", []) or []
    if WATCH_FOLDER_ID not in parents:
        return False

    mime_type = file_obj.get("mimeType", "")
    allowed = {
        # PDF
        "application/pdf",
        # Word
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        # Excel
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # PowerPoint
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        # Text
        "text/plain",
        # Google Native
        "application/vnd.google-apps.document",
        "application/vnd.google-apps.spreadsheet",
        "application/vnd.google-apps.presentation"
    }
    return mime_type in allowed


def create_task_json(file_obj: dict[str, Any]) -> dict[str, Any]:
    """Generate task metadata for a detected file."""
    # Use timestamp + first 4 chars of file ID for uniqueness
    file_id = str(file_obj.get("id", ""))
    file_id_suffix = file_id[:4] if file_id else "xxxx"
    job_id = f"{datetime.now(timezone.utc).astimezone().strftime('%Y%m%d_%H%M%S')}_{file_id_suffix}_ot"
    return {
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_type": DEFAULT_PROJECT_TYPE,
        "language": DEFAULT_LANGUAGE,
        "priority": "high",
        "source": {
            "provider": "google_drive",
            "file_id": file_obj.get("id"),
            "file_name": file_obj.get("name"),
            "mime_type": file_obj.get("mimeType"),
            "web_view_link": file_obj.get("webViewLink"),
            "modified_time": file_obj.get("modifiedTime"),
        },
        "required_outputs": ["summary", "questions", "research", "solutions"],
        "human_review_required": True,
        "notes": "Automatically detected via Drive polling."
    }


def write_task(task: dict[str, Any]) -> Path:
    """Save task JSON to the tasks directory."""
    path = TASK_DIR / f"{task['job_id']}.json"
    path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def sync_existing_files(service) -> int:
    """List all existing files in the folder and create tasks for them."""
    query = f"'{WATCH_FOLDER_ID}' in parents and trashed = false"
    # Simple check to avoid creating duplicate tasks for existing files
    # Check if a task with the same file_id already exists in processed folders
    processed_ids = set()
    for d in ["done", "failed", "processing"]:
        p = ROOT / "state" / d
        if p.exists():
            for f in p.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    fid = data.get("source", {}).get("file_id")
                    if fid: processed_ids.add(fid)
                except: pass
    
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, parents, webViewLink, modifiedTime)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = results.get("files", [])
    count = 0
    for f in files:
        if is_target_file(f):
            if f.get("id") in processed_ids:
                continue
            
            task = create_task_json(f)
            write_task(task)
            print(f"Sync created task: {task['job_id']} for {f.get('name')}")
            count += 1
    return count


def poll_once(service) -> int:
    """Check for changes since the last token and create tasks."""
    page_token = get_saved_page_token(service)
    count = 0

    while page_token:
        response = service.changes().list(
            pageToken=page_token,
            spaces="drive",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields="nextPageToken,newStartPageToken,changes(fileId,file(id,name,mimeType,parents,webViewLink,modifiedTime,trashed))",
        ).execute()

        for change in response.get("changes", []):
            file_obj = change.get("file")
            if is_target_file(file_obj):
                task = create_task_json(file_obj)
                write_task(task)
                print(f"Created task: {task['job_id']} for {file_obj.get('name')}")
                count += 1

        if "newStartPageToken" in response:
            save_page_token(response["newStartPageToken"])
            break

        page_token = response.get("nextPageToken")
    
    return count


def main():
    """Continuous or one-shot polling loop."""
    import sys
    once_mode = "--once" in sys.argv
    sync_mode = "--sync" in sys.argv
    
    if not WATCH_FOLDER_ID:
        print("Error: WATCH_FOLDER_ID is not set in environment.")
        return

    service = build_drive_service()
    
    if sync_mode:
        print("Performing one-time sync of existing files...")
        count = sync_existing_files(service)
        print(f"Sync complete. Created {count} tasks.")
        return

    # BOOTSTRAP: Always sync once at the start to catch files missed during downtime.
    print("Initial bootstrap sync to catch pending files...")
    sync_existing_files(service)
    
    if once_mode:
        return

    print(f"Starting Drive polling (mode: continuous)...")
    while True:
        try:
            count = poll_once(service)
            if count > 0:
                print(f"Detected {count} new files.")
        except Exception as e:
            print(f"Polling error: {e}")
            import traceback; traceback.print_exc()
        
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
