#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# V10.0 Canonical Telegram Bot Listener
# Handles "고도화 해줘", "수정/보완", and provides instant acknowledgment.

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ROOT_DIR = Path(__file__).resolve().parents[1]

def send_telegram_direct(msg: str, reply_markup: dict = None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try: 
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Bot Error] Failed to send message: {e}")

BOT_MEMORY_FILE = ROOT_DIR / "state" / "bot_memory.json"

def set_state(cid, state_data):
    BOT_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    memory = {}
    if BOT_MEMORY_FILE.exists():
        try: memory = json.loads(BOT_MEMORY_FILE.read_text())
        except: pass
    memory[str(cid)] = state_data
    BOT_MEMORY_FILE.write_text(json.dumps(memory), encoding="utf-8")

def get_state(cid):
    if BOT_MEMORY_FILE.exists():
        try: return json.loads(BOT_MEMORY_FILE.read_text()).get(str(cid))
        except: return None
    return None

def clear_state(cid):
    if BOT_MEMORY_FILE.exists():
        try: 
            memory = json.loads(BOT_MEMORY_FILE.read_text())
            if str(cid) in memory:
                del memory[str(cid)]
                BOT_MEMORY_FILE.write_text(json.dumps(memory), encoding="utf-8")
        except: pass

def answer_callback(cb_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery"
    try: requests.post(url, json={"callback_query_id": cb_id, "text": text}, timeout=10)
    except: pass

def get_last_job_id():
    """Retrieve the most recent job ID from outputs/01_summaries or state/done."""
    # 1. Check generated summaries first (robust against manual runs)
    summary_dir = ROOT_DIR / "outputs" / "01_summaries"
    if summary_dir.exists():
        summary_files = sorted(list(summary_dir.glob("*_summary.md")), key=os.path.getmtime, reverse=True)
        if summary_files:
            return summary_files[0].name.replace("_summary.md", "")
            
    # 2. Fallback to state/done
    done_dir = ROOT_DIR / "state" / "done"
    if done_dir.exists():
        log_files = sorted(list(done_dir.glob("*.json")), key=os.path.getmtime, reverse=True)
        if log_files:
            try:
                data = json.loads(log_files[0].read_text())
                return data.get("job_id")
            except:
                return log_files[0].stem.split("_")[-1] if "_" in log_files[0].stem else log_files[0].stem
    return None

def process_callback(cb_id, cid, data):
    print(f"[Bot] Callback received: {data}")
    if "|" not in data:
        answer_callback(cb_id, "잘못된 요청입니다.")
        return
        
    action, job_id = data.split("|", 1)
    
    if action == "deep_research":
        answer_callback(cb_id, "🚀 심층 리서치 고도화를 시작합니다 (약 2~3분 소요)")
        send_telegram_direct(f"🔍 <b>딥 인텔리전스 에이전트를 파견합니다. (작업 ID: {job_id})</b>\n전 세계 시장 트렌드와 경쟁사를 분석하여 20P+ 정밀 리포트를 생성합니다.")
        try:
            cmd_dir = ROOT_DIR / "state" / "commands"
            cmd_dir.mkdir(parents=True, exist_ok=True)
            cmd_file = cmd_dir / f"cmd_{job_id}_{int(time.time())}.json"
            
            cmd_payload = {"command": "deep_research", "job_id": job_id, "timestamp": time.time()}
            cmd_file.write_text(json.dumps(cmd_payload), encoding="utf-8")
        except Exception as e:
            send_telegram_direct(f"❌ 작업 요청 중 파일 시스템 오류 발생: {e}")
            
    elif action == "request_edit":
        answer_callback(cb_id, "📝 수정/피드백 모드로 전환되었습니다.")
        set_state(cid, {"job_id": job_id, "expecting": "feedback"})
        send_telegram_direct(f"📝 <b>[수정/피드백 입력 예약]</b>\n작업 ID <code>{job_id}</code>에 반영할 피드백이나 특별한 수정 지시사항을 방 안에 적어주세요.\n(예: 주현영 모델 대신 김연아 모델 중심의 타켓층 설정으로 수정해줘)")

def process_command(text: str, cid: str):
    print(f"[Bot] Processing: {text}")
    
    # 0. Check Session State for Feedbacks
    state = get_state(cid)
    if state and state.get("expecting") == "feedback":
        job_id = state.get("job_id")
        feedback_path = ROOT_DIR / "state" / f"feedback_{job_id}.txt"
        feedback_path.parent.mkdir(parents=True, exist_ok=True)
        feedback_path.write_text(text, encoding="utf-8")
        
        clear_state(cid)
        reply_markup = {
            "inline_keyboard": [
                [{"text": f"🚀 피드백({job_id}) 반영 딥-리서치 강제 트리거", "callback_data": f"deep_research|{job_id}"}]
            ]
        }
        send_telegram_direct(f"✅ <b>피드백이 안전하게 저장되었습니다.</b>\n\n내용: <i>{text}</i>\n해당 피드백을 반영하여 심층 분석을 이어서 진행하시겠습니까?", reply_markup)
        return
        
    # 1. '고도화 해줘' - Trigger V16.0 Deep Research Intelligence Engine
    if "고도화" in text or "고도화 해줘" in text:
        # Instant Acknowledgment
        send_telegram_direct("🔍 <b>딥 인텔리전스 에이전트를 파견합니다.</b>\n전 세계 시장 트렌드와 경쟁사를 분석하여 20P+ 정밀 리포트를 생성합니다. (심층 추론으로 인해 수 분이 소요될 수 있습니다.)")
        
        job_id = get_last_job_id()
        if not job_id:
            send_telegram_direct("❌ 최근 작업 기록을 찾을 수 없습니다.")
            return
            
        try:
            # Issue a deep_research command to the pipeline
            cmd_dir = ROOT_DIR / "state" / "commands"
            cmd_dir.mkdir(parents=True, exist_ok=True)
            cmd_file = cmd_dir / f"cmd_{job_id}_{int(time.time())}.json"
            
            cmd_payload = {
                "command": "deep_research",
                "job_id": job_id,
                "timestamp": time.time()
            }
            cmd_file.write_text(json.dumps(cmd_payload), encoding="utf-8")
            print(f"[Bot] Successfully issued deep_research command for {job_id}")
            # Verification: ensure file exists
            if cmd_file.exists():
                print(f"[Bot] Command file verified: {cmd_file.name}")
        except Exception as e:
            error_msg = f"❌ 작업 요청 중 파일 시스템 오류 발생: {e}"
            print(f"[Bot Error] {error_msg}")
            send_telegram_direct(error_msg)

    # 2. '수정' 또는 '보완' 요청
    elif "수정" in text or "보완" in text:
        feedback_path = ROOT_DIR / "state" / "last_feedback.txt"
        feedback_path.parent.mkdir(parents=True, exist_ok=True)
        feedback_path.write_text(text, encoding="utf-8")
        
        send_telegram_direct(f"📝 <b>수정 요청이 접수되었습니다.</b>\n내용: <i>{text}</i>\n다음 '고도화' 시 이 내용을 반영하여 분석을 강화합니다.")
        
        # Auto-trigger if urgent keywords present
        if any(k in text for k in ["다시", "하면", "직후", "바로", "해줘"]):
            job_id = get_last_job_id()
            if job_id:
                subprocess.Popen([sys.executable, str(ROOT_DIR / "scripts" / "advanced_analysis.py"), job_id], cwd=str(ROOT_DIR))

    else:
        # Implicit acknowledgment for other messages
        send_telegram_direct("✅ <b>메시지를 확인했습니다.</b> 분석 대기 중입니다.\n\n💡 <b>명령어 가이드:</b>\n- '고도화 해줘' (20P 리포트 생성)\n- '[내용] 보완해줘' (피드백 반영)")

def run_bot_listener():
    if not TOKEN or not CHAT_ID:
        print("[Bot] Missing TOKEN or CHAT_ID in .env. Listener disabled.")
        return

    print(f"[Bot] Starting V10.0 Telegram Listener (Polling)...")
    last_update_id = 0
    url_base = f"https://api.telegram.org/bot{TOKEN}"
    
    while True:
        try:
            url = f"{url_base}/getUpdates?offset={last_update_id + 1}&timeout=30"
            resp = requests.get(url, timeout=35).json()
            
            if not resp.get("ok"): 
                time.sleep(5)
                continue
                
            for update in resp.get("result", []):
                last_update_id = update["update_id"]
                
                # Check for callback_query (Inline Keyboard)
                if "callback_query" in update:
                    cb = update["callback_query"]
                    cid = str(cb.get("message", {}).get("chat", {}).get("id"))
                    data = cb.get("data", "")
                    cb_id = cb.get("id")
                    
                    if CHAT_ID and cid != CHAT_ID: continue
                    process_callback(cb_id, cid, data)
                    continue
                
                msg = update.get("message")
                if not msg: continue
                
                cid = str(msg.get("chat", {}).get("id"))
                text = msg.get("text", "")
                
                # Security Check: Filter by allowed CHAT_ID
                if CHAT_ID and cid != CHAT_ID:
                    print(f"[Bot] Unauthorized access attempts from {cid}")
                    continue
                
                if text:
                    process_command(text, cid)
                
        except Exception as e:
            print(f"[Bot] Listener Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot_listener()
