from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# V21.0 Global Deep Research & Automation Pipeline
# Orchestrates task processing, document generation, and Deep Intel agent dispatch.

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
INCOMING_DIR = ROOT / "incoming_tasks" / "tasks"
PROCESSING_DIR = ROOT / "state" / "processing"
DONE_DIR = ROOT / "state" / "done"
FAILED_DIR = ROOT / "state" / "failed"
LOG_DIR = ROOT / "outputs" / "logs"
# Telegram Config
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Configuration
POLL_SECONDS = int(os.environ.get("PIPELINE_POLL_SECONDS", "30"))
# FIXED: Added 'process' keyword and explicit flags for bridge CLI
ANTIGRAVITY_PROCESS_CMD = os.environ.get("ANTIGRAVITY_PROCESS_CMD", "python3 scripts/antigravity_bridge.py process --task \"{task_path}\" --job-id \"{job_id}\"")

def ensure_dirs() -> None:
    """Create necessary directories if they don't exist."""
    for d in [INCOMING_DIR, PROCESSING_DIR, DONE_DIR, FAILED_DIR, LOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def save_json(path: Path, data: dict[str, Any]) -> None:
    """Save dictionary to JSON file."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def list_pending_tasks() -> list[Path]:
    """Get list of JSON tasks in the incoming directory."""
    return sorted(list(INCOMING_DIR.glob("*.json")))


def mark_processing(task_path: Path) -> Path:
    """Move task to the processing directory."""
    new_path = PROCESSING_DIR / task_path.name
    shutil.move(str(task_path), str(new_path))
    return new_path


def write_step_log(job_id: str, step: str, payload: dict[str, Any]) -> None:
    """Write a step-specific log entry."""
    path = LOG_DIR / f"{job_id}_{step}.json"
    save_json(path, payload)


def run_subprocess(command: str, *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a shell command and capture its output."""
    return subprocess.run(
        command,
        shell=True,
        cwd=str(cwd or ROOT),
        text=True,
        capture_output=True,
    )


def run_antigravity(task_path: Path, job_id: str) -> dict[str, Any]:
    """Execute the core analysis via the configured command with retry logic for API limits."""
    cmd = ANTIGRAVITY_PROCESS_CMD.format(task_path=str(task_path), job_id=job_id)
    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        started_at = now_iso()
        print(f"[{job_id}] Running analysis (Attempt {attempt}/{max_retries})")
        # Log command for debugging
        write_step_log(job_id, "antigravity_cmd", {"cmd": cmd})
        
        result = run_subprocess(cmd, cwd=ROOT)
        finished_at = now_iso()

        if result.returncode == 0:
            return {
                "status": "success",
                "attempt": attempt,
                "output": result.stdout,
                "finished_at": finished_at
            }
        
        # Check for specific quota errors
        if "quota" in result.stdout.lower() or "quota" in result.stderr.lower():
            print(f"[{job_id}] Quota exceeded. Waiting 60s...")
            time.sleep(60)
        else:
            # Fatal error
            print(f"[{job_id}] Analysis failed with returncode {result.returncode}")
            print(f"Stderr: {result.stderr}")
            break
            
    return {
        "status": "failed",
        "returncode": result.returncode,
        "stderr": result.stderr,
        "stdout": result.stdout
    }


def send_telegram_notification(job_id: str, file_name: str):
    """OT 원문 분석 완료 알림 — 고도화 방식 선택 버튼 제공."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    msg = (
        f"✅ <b>OT 원문 분석 완료</b>\n\n"
        f"📄 <b>파일</b>: {file_name}\n"
        f"🆔 <b>Job ID</b>: <code>{job_id}</code>\n\n"
        f"고도화 방식을 선택해주세요."
    )

    reply_markup = {
        "inline_keyboard": [
            [{"text": "📊 Claude 고도화 해줘", "callback_data": f"claude_upgrade|{job_id}"}],
            [{"text": "🔬 딥 인텔 고도화 해줘", "callback_data": f"deep_research|{job_id}"}],
        ]
    }

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "reply_markup": reply_markup,
        "disable_web_page_preview": False,
    }
    try:
        import requests
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Pipeline] Telegram notification failed: {e}")

def send_telegram_error_notification(job_id: str, file_name: str, error_msg: str):
    """Send a failure notification to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    msg = f"🚨 <b>파이프라인 오류 발생</b>\n\n📄 <b>파일명</b>: {file_name}\n🆔 <b>작업 ID</b>: <code>{job_id}</code>\n\n작업이 실패하여 <code>state/failed</code> 폴더로 이동되었습니다.\n\n<b>오류 내용:</b>\n<code>{error_msg}</code>"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        import requests
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Pipeline] Telegram error notification failed: {e}")

def process_task(task_path: Path) -> None:
    """Orchestrate the full analysis pipeline for a single task."""
    job_id, file_name = "Unknown", "Unknown File"
    try:
        task_data = json.loads(task_path.read_text(encoding="utf-8"))
        job_id = task_data.get("job_id", "Unknown")
        file_name = task_data.get("source", {}).get("file_name", "Unknown File")
        
        print(f"\n🚀 [Pipeline] Starting Job: {job_id}")
        
        # 1. Antigravity Core Analysis
        res = run_antigravity(task_path, job_id)
        if res["status"] != "success":
            raise RuntimeError(f"Antigravity failed: {res.get('stderr', 'unknown') or res.get('stdout', 'unknown')}")
        
        # Finalize
        shutil.move(str(task_path), str(DONE_DIR / task_path.name))
        print(f"✅ [Pipeline] Job {job_id} Completed Successfully.")
        
        # Notify
        send_telegram_notification(job_id, file_name)
        
    except Exception as e:
        print(f"❌ [Pipeline] Job Failed: {e}")
        shutil.move(str(task_path), str(FAILED_DIR / task_path.name))
        send_telegram_error_notification(job_id, file_name, str(e))


def run_all() -> None:
    """Run both Drive polling and task processing in the same process."""
    ensure_dirs()
    print("[pipeline] Starting V21.0 Global Automation Pipeline...")
    
    drive_script = ROOT / "scripts" / "poll_drive_to_tasks.py"
    
    while True:
        try:
            # 0. Check for commands (Deep Research)
            command_dir = ROOT / "state" / "commands"
            if command_dir.exists():
                for cmd_file in command_dir.glob("*.json"):
                    try:
                        cmd_data = json.loads(cmd_file.read_text(encoding="utf-8"))
                        if cmd_data.get("command") == "deep_research":
                            jid = cmd_data.get("job_id")
                            if jid:
                                engine = ROOT / "scripts" / "deep_intel_engine.py"
                                # ASYNC Dispatch
                                subprocess.Popen([sys.executable, str(engine), jid], 
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                                               start_new_session=True)
                                print(f"[Pipeline] Deep Intel dispatched in background for {jid}")
                        cmd_file.unlink()
                    except: pass

            # 1. Poll Drive
            print("\n--- Checking Drive ---")
            run_subprocess(f'{sys.executable} "{drive_script}" --once', cwd=ROOT)
            
            # 2. Process tasks
            tasks = list_pending_tasks()
            for t in tasks:
                p = mark_processing(t)
                process_task(p)
                
            time.sleep(POLL_SECONDS)
        except Exception as e:
            print(f"Pipeline Loop Error: {e}")
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run_all()
