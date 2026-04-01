import os
import sys
import time
import subprocess
import socket
from pathlib import Path
from datetime import datetime

# V23.0 High-Reliability Watchdog (macOS Optimized)
# Uses pgrep for accurate detection and google.com:443 for heartbeats.

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
WATCH_LOG = LOG_DIR / "keep_alive.log"
LOCK_FILE = ROOT / "state" / "keep_alive.lock"

SERVICES = {
    "poll_drive": {
        "script": "scripts/poll_drive_to_tasks.py",
        "log": "outputs/logs/poll_drive.log",
        "cmd": [sys.executable, str(ROOT / "scripts/poll_drive_to_tasks.py")],
        "backoff_minutes": 0,
        "last_failure": 0
    },
    "run_pipeline": {
        "script": "scripts/run_pipeline.py",
        "log": "outputs/logs/run_pipeline.log",
        "cmd": [sys.executable, str(ROOT / "scripts/run_pipeline.py"), "all"],
        "backoff_minutes": 0,
        "last_failure": 0
    },
    "telegram_bot": {
        "script": "scripts/telegram_bot.py",
        "log": "outputs/logs/telegram_bot.log",
        "cmd": [sys.executable, str(ROOT / "scripts/telegram_bot.py")],
        "backoff_minutes": 0,
        "last_failure": 0
    }
}

def log_event(message: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {message}\n"
    with open(WATCH_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(entry.strip())

def is_network_up() -> bool:
    """Check connectivity via HTTPS port (usually open even in corporate networks)."""
    try:
        socket.create_connection(("google.com", 443), timeout=5)
        return True
    except OSError:
        return False

def is_running(script_path: str) -> bool:
    """Use pgrep -f for robust macOS process detection."""
    try:
        # Use absolute path for matching to avoid duplicates or false positives
        cmd = ["/usr/bin/pgrep", "-f", script_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        pids = result.stdout.strip().split("\n") if result.stdout.strip() else []
        # Filter out our own PID if we are checking ourself
        my_pid = str(os.getpid())
        pids = [p for p in pids if p != my_pid]
        return len(pids) > 0
    except Exception as e:
        log_event(f"Error checking status: {e}")
        return True

def start_service(name: str, config: dict):
    log_path = ROOT / config["log"]
    import shlex
    cmd_str = " ".join(shlex.quote(str(arg)) for arg in config["cmd"])
    
    log_event(f"RESTARTING: {name} (Cmd: {cmd_str})")
    # Using 'nohup ... &' and ensuring log directory is writable
    nohup_cmd = f"nohup {cmd_str} > '{log_path}' 2>&1 &"
    subprocess.run(nohup_cmd, shell=True, cwd=str(ROOT))

def acquire_lock():
    pid = str(os.getpid())
    if LOCK_FILE.exists():
        try:
            old_pid = LOCK_FILE.read_text().strip()
            os.kill(int(old_pid), 0)
            print("\n" + "━"*50)
            print(f" 📡 [시스템 상태] 백그라운드에서 이미 안전하게 가동 중입니다 (PID {old_pid})")
            print(" 🔍 실시간 모니터링 화면으로 전환합니다...")
            print("━"*50 + "\n")
            sys.exit(0)
        except (ProcessLookupError, ValueError, OSError):
            log_event(f"🔄 이전 비정상 종료 기록 발견 (Stale lock PID {old_pid}). 시스템을 재정렬합니다.")
    
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(pid)

def main():
    acquire_lock()
    log_event("WATCHDOG V23.0 (macOS Optimised) STARTED.")
    
    while True:
        try:
            if not is_network_up():
                log_event("NETWORK DOWN: Heartbeat failed. Waiting...")
                time.sleep(30)
                continue

            current_time = time.time()
            for name, config in SERVICES.items():
                # Detect using the absolute path for reliability
                if not is_running(config["script"]):
                    if current_time < config["last_failure"] + (config["backoff_minutes"] * 10): # Shorter backoff
                        continue
                    
                    log_event(f"DOWN: {name} detected offline.")
                    start_service(name, config)
                    config["last_failure"] = current_time
                    config["backoff_minutes"] = min(config["backoff_minutes"] + 1, 30)
                else:
                    config["backoff_minutes"] = 0
            
        except Exception as e:
            log_event(f"Main loop error: {e}")
            
        time.sleep(60) # check once per minute for stability

if __name__ == "__main__":
    main()
