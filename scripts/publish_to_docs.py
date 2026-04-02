from __future__ import annotations

import json
import os
import re
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

warnings.filterwarnings("ignore", category=FutureWarning)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

import subprocess
load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"
STATE_DIR = ROOT / "state"
LOG_DIR = OUTPUTS_DIR / "logs"
TOKEN_PATH = ROOT / "token.json"
RUN_HISTORY_PATH = STATE_DIR / "run_history.json"

# Google Drive folder ID for published documents (from environment)
OUTPUT_FOLDER_ID = os.environ.get("OUTPUT_FOLDER_ID")

# Specification for documents to publish: (category, search_dir, title_suffix, is_required)
DOC_SPECS = [
    ("deep_report", OUTPUTS_DIR / "02_deep_analysis", "02_OT_심층리포트", True),
    ("summary", OUTPUTS_DIR / "summaries", "01_OT_한장요약", False),
    ("questions", OUTPUTS_DIR / "questions", "02_OT_핵심질문", False),
    ("research", OUTPUTS_DIR / "research", "03_OT_리서치팩", False),
    ("solutions", OUTPUTS_DIR / "solutions", "04_OT_해결방향3안", False),
]


def ensure_dirs() -> None:
    """Ensure necessary directories exist."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def load_credentials() -> Credentials:
    """Load and refresh Google credentials."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing {TOKEN_PATH}. Please run authentication first.")
        
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def build_services():
    """Build Google Docs and Drive services with scope error handling."""
    try:
        creds = load_credentials()
        docs_service = build("docs", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        return docs_service, drive_service
    except Exception as e:
        if "insufficient authentication scopes" in str(e).lower():
            print("\n" + "="*60)
            print("[CRITICAL] Google API 권한 부족 (403 Forbidden)")
            print("사유: 현재 발급된 token.json에 필요한 권한(Scopes)이 포함되어 있지 않습니다.")
            print("조치 방법:")
            print("  1. Google Cloud Console에서 'Google Docs API'가 활성화되어 있는지 확인하세요.")
            print(f"  2. {TOKEN_PATH.name} 파일을 삭제한 후 파이프라인을 재실행하여 재인증을 진행하세요.")
            print("="*60 + "\n")
        raise


def utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    """Helper to load JSON with diagnostic logging."""
    if not path.exists():
        return default
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        print(f"[Error] JSON file is empty: {path}")
        return default
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"[Error] Failed to parse JSON from {path}: {e}")
        print(f"[Error] Content snippet: {content[:100]!r}")
        raise


def save_json(path: Path, payload: Any) -> None:
    """Helper to save JSON to a file."""
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def normalize_markdown(md: str) -> str:
    """
    Convert basic markdown to plain text for Google Docs insertion.
    This is a simplified robust approach.
    """
    text = md.replace("\r\n", "\n").replace("\r", "\n")

    # fenced code blocks -> block markers
    text = re.sub(r"```.*?\n(.*?)```", lambda m: "\n[code]\n" + m.group(1).strip() + "\n[/code]\n", text, flags=re.DOTALL)

    # headings -> clean title lines
    text = re.sub(r"^###\s+(.*)$", r"\n\1\n", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s+(.*)$", r"\n\1\n", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s+(.*)$", r"\n\1\n", text, flags=re.MULTILINE)

    # bold / italic markers removal
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # markdown links: [text](url) -> text (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)

    # bullet points -> unicode bullets
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.MULTILINE)

    # Clean up excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text + "\n"


def add_document_preamble(
    *,
    title: str,
    body_text: str,
    job_id: str,
    source_file_name: str,
    source_file_link: str,
) -> str:
    """Add a header block to the document content."""
    timestamp = utc_now_iso()
    preamble = (
        f"{title}\n\n"
        f"제작 시각: {timestamp}\n"
        f"Job ID: {job_id}\n"
        f"원본 파일: {source_file_name}\n"
        f"원본 링크: {source_file_link}\n\n"
        f"----------------------------------------\n\n"
    )
    return preamble + body_text


def create_doc(docs_service, title: str) -> tuple[str, str]:
    """Create a new Google Doc and return ID and URL."""
    resp = docs_service.documents().create(body={"title": title}).execute()
    document_id = resp["documentId"]
    doc_url = f"https://docs.google.com/document/d/{document_id}/edit"
    return document_id, doc_url


def insert_text_into_doc(docs_service, document_id: str, text: str) -> None:
    """Batch update a Google Doc with text."""
    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": text,
            }
        }
    ]
    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests},
    ).execute()


def move_file_to_folder(drive_service, file_id: str, target_folder_id: str) -> None:
    """Move a file to a specific folder on Drive."""
    file_meta = drive_service.files().get(fileId=file_id, fields="id, parents").execute()
    previous_parents = ",".join(file_meta.get("parents", []))

    drive_service.files().update(
        fileId=file_id,
        addParents=target_folder_id,
        removeParents=previous_parents,
        fields="id, parents",
        supportsAllDrives=True,
    ).execute()


def find_task_json(job_id: str) -> Path:
    """Find the task JSON for a given job ID across all possible locations."""
    search_paths = [
        ROOT / "incoming_tasks" / "tasks" / f"{job_id}.json",
        STATE_DIR / "processing" / f"{job_id}.json",
        STATE_DIR / "done" / f"{job_id}.json",
        STATE_DIR / "failed" / f"{job_id}.json",
    ]
    for path in search_paths:
        if path.exists():
            return path
    raise FileNotFoundError(f"Task JSON not found for Job ID {job_id} in {search_paths}")


def load_task(job_id: str) -> dict[str, Any]:
    """Load task metadata with robust error reporting."""
    task_path = find_task_json(job_id)
    content = task_path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Task JSON file is empty: {task_path} (Size: {task_path.stat().st_size})")
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"[Error] Failed to parse task JSON for {job_id} at {task_path}")
        print(f"Content length: {len(content)}")
        print(f"Content preview: {content[:50]!r}")
        raise


def source_markdown_path(job_id: str, category: str, base_dir: Path) -> Path | None:
    """Find the markdown file for a specific output category. Returns None if not found."""
    if not base_dir.exists():
        return None
        
    candidates = [
        base_dir / f"{job_id}_{category}.md",
        base_dir / f"{job_id}_ot_{category}.md", 
        base_dir / f"{job_id}_summary.md" if category == "summary" else None,
        base_dir / f"{job_id}_deep_report.md" if category == "deep_report" else None,
    ]
    for path in candidates:
        if path and path.exists():
            return path
    return None


def publish_one(
    *,
    docs_service,
    drive_service,
    job_id: str,
    title_suffix: str,
    md_path: Path,
    source_file_name: str,
    source_file_link: str,
) -> dict[str, str]:
    """Publish a single markdown file as a Google Doc."""
    # Use the original filename (without extension) for the document title
    base_name = os.path.splitext(source_file_name)[0]
    title = f"[{base_name}]_{title_suffix}"
    raw_md = md_path.read_text(encoding="utf-8")
    plain_text = normalize_markdown(raw_md)
    full_text = add_document_preamble(
        title=title,
        body_text=plain_text,
        job_id=job_id,
        source_file_name=source_file_name,
        source_file_link=source_file_link,
    )

    document_id, doc_url = create_doc(docs_service, title)
    insert_text_into_doc(docs_service, document_id, full_text)
    
    if OUTPUT_FOLDER_ID:
        move_file_to_folder(drive_service, document_id, OUTPUT_FOLDER_ID)

    return {
        "title": title,
        "document_id": document_id,
        "url": doc_url,
        "source_markdown": str(md_path),
    }


def append_run_history(entry: dict[str, Any]) -> None:
    """Update global run history."""
    history = load_json(RUN_HISTORY_PATH, default=[])
    history.append(entry)
    save_json(RUN_HISTORY_PATH, history)


def upload_binary_file(drive_service, file_path: Path, folder_id: str | None, mime_type: str) -> dict[str, str]:
    """Upload a binary file (docx, html, etc.) to Drive and return ID and URL."""
    from googleapiclient.http import MediaFileUpload
    
    file_metadata: dict[str, Any] = {
        "name": file_path.name,
        "parents": [folder_id] if folder_id else []
    }
    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
    
    file_resp = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()
    
    # Ensure the file is readable by anyone with the link
    drive_service.permissions().create(
        fileId=file_resp["id"],
        body={"type": "anyone", "role": "reader"}
    ).execute()
    
    return {
        "title": file_path.name,
        "document_id": file_resp["id"],
        "url": file_resp.get("webViewLink", ""),
        "local_path": str(file_path)
    }

def git_sync_reports(job_id: str) -> bool:
    """Commit and push new reports to GitHub for Pages deployment."""
    try:
        print(f"[Git] Syncing reports for job {job_id}...")
        
        # 1. Add changes in docs/reports
        subprocess.run(["git", "add", "docs/reports/"], cwd=ROOT, check=True)
        
        # 2. Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("[Git] No changes to commit.")
            return True
            
        # 3. Commit
        commit_msg = f"Auto-deploy reports for job {job_id}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT, check=True)
        
        # 4. Push to origin (Targeting 'main' for GitHub Pages)
        subprocess.run(["git", "push", "origin", "master:main"], cwd=ROOT, check=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=ROOT, check=True)
        print(f"[Git] Successfully pushed reports for job {job_id} to both master and main branches.")
        return True
    except Exception as e:
        print(f"[Git Error] Failed to sync reports: {e}")
        return False

def publish_job(job_id: str) -> dict[str, Any]:
    """Publish generated outputs (Docs, Docx, HTML) for a specific job."""
    ensure_dirs()
    docs_service, drive_service = build_services()
    task = load_task(job_id)

    source = task.get("source", {})
    source_file_name = source.get("file_name", "unknown_source")
    source_file_link = source.get("web_view_link", "")

    published_docs: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    # 1. Publish standard Markdown to Google Docs
    for category, base_dir, title_suffix, is_required in DOC_SPECS:
        try:
            md_path = source_markdown_path(job_id, category, base_dir)
            if not md_path:
                if is_required:
                    raise FileNotFoundError(f"Missing REQUIRED markdown for {category} in {base_dir}")
                else:
                    print(f"[Publish] Skipping optional category: {category} (File not found)")
                    continue

            doc_info = publish_one(
                docs_service=docs_service,
                drive_service=drive_service,
                job_id=job_id,
                title_suffix=title_suffix,
                md_path=md_path,
                source_file_name=source_file_name,
                source_file_link=source_file_link,
            )
            published_docs.append(doc_info)
        except Exception as e:
            if is_required:
                failures.append({"category": category, "error": str(e)})
            else:
                print(f"[Publish] Warning: Failed to publish optional {category}: {e}")

    # 2. Upload any .docx or .html reports from outputs/03_final_reports/
    report_dir = OUTPUTS_DIR / "03_final_reports"
    docs_report_dir = ROOT / "docs" / "reports"
    docs_report_dir.mkdir(parents=True, exist_ok=True)
    
    if report_dir.exists():
        for file in report_dir.glob(f"{job_id}_*"):
            if file.suffix.lower() in [".docx", ".html", ".pptx"]:
                try:
                    # [V6.4] Copy to docs/ for GitHub Pages
                    import shutil
                    shutil.copy2(file, docs_report_dir / file.name)
                    
                    if file.suffix == ".docx":
                        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    elif file.suffix == ".pptx":
                        mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    else:
                        mime = "text/html"
                    
                    print(f"[Publish] Uploading binary report to Drive: {file.name}")
                    info = upload_binary_file(drive_service, file, OUTPUT_FOLDER_ID, mime)
                    
                    # [V6.4] Add Direct GitHub Pages Link if HTML
                    if file.suffix == ".html":
                        direct_url = f"https://meandfree23.github.io/auto-ot/reports/{file.name}"
                        info["direct_url"] = direct_url
                        print(f"[Publish] Direct URL generated: {direct_url}")
                    
                    published_docs.append(info)
                except Exception as e:
                    failures.append({"file": file.name, "error": str(e)})

    # [V16.0] New: Sync changes to GitHub for Pages deployment
    git_sync_reports(job_id)

    result = {
        "job_id": job_id,
        "source_file_id": source.get("file_id"),
        "source_file_link": source_file_link,
        "published_at": utc_now_iso(),
        "status": "partial_failure" if failures else "success",
        "published_docs": published_docs,
        "failures": failures,
    }

    log_path = LOG_DIR / f"{job_id}_publish.json"
    save_json(log_path, result)
    append_run_history(result)

    return result


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/publish_to_docs.py <job_id>")
        sys.exit(1)

    job_id = sys.argv[1]
    try:
        result = publish_job(job_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error publishing job {job_id}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
