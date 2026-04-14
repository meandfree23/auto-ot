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

BOT_MEMORY_FILE  = ROOT_DIR / "state" / "bot_memory.json"
RESEARCH_ARCHIVE = Path(os.environ.get("RESEARCH_ARCHIVE_PATH", "/Users/kk/research-output/index.html"))
GITHUB_PAGES_URL = os.environ.get("GITHUB_PAGES_URL", "").rstrip("/")
if not GITHUB_PAGES_URL:
    print("[Bot] WARNING: GITHUB_PAGES_URL is not set — report links will not be generated.")

# ── Archive helpers ────────────────────────────────────────────────────────────
def check_upload_status(job_id: str) -> dict:
    """마스터 허브(docs/reports)와 리서치 아카이브 등록 여부 확인."""
    hub_uploaded = any(
        (ROOT_DIR / "docs" / "reports").glob(f"{job_id}_*.html")
    )
    archive_registered = False
    if RESEARCH_ARCHIVE.exists():
        archive_registered = job_id in RESEARCH_ARCHIVE.read_text(encoding="utf-8")
    return {"hub": hub_uploaded, "archive": archive_registered}


def add_to_research_archive(job_id: str, report_type: str, title: str) -> bool:
    """research-output/index.html에 OT 리포트 카드 삽입."""
    if not RESEARCH_ARCHIVE.exists():
        return False
    if report_type == "deep-intel":
        filename  = f"{job_id}_deep_intel_report.html"
        badge_txt = "딥 인텔"
        emoji     = "🔬"
        grad      = "linear-gradient(135deg,#1e3a5f 0%,#0ea5e9 60%,#38bdf8 100%)"
    else:
        filename  = f"{job_id}_precision_report.html"
        badge_txt = "전략 분석"
        emoji     = "📊"
        grad      = "linear-gradient(135deg,#14532d 0%,#10b981 60%,#6ee7b7 100%)"

    report_url = f"{GITHUB_PAGES_URL}/reports/{filename}" if GITHUB_PAGES_URL else f"#{filename}"
    from datetime import datetime
    date_str = datetime.now().strftime("%Y년 %-m월 %-d일")
    card_html = f"""
<!-- CARD: {title} ({badge_txt}) -->
<a class="project-card animate"
   href="{report_url}"
   target="_blank"
   data-category="report"
   data-tags="OT분석,전략,{badge_txt}"
   data-title="{title}"
   aria-label="{title} 열기">
  <div class="card-thumb" style="background:{grad}">
    <div class="card-thumb-inner">{emoji}</div>
    <span class="card-thumb-label">OT 리포트</span>
  </div>
  <div class="card-body">
    <div class="card-tags">
      <span class="tag blue">OT분석</span>
      <span class="tag purple">{badge_txt}</span>
    </div>
    <h3 class="card-title">{title}</h3>
    <p class="card-desc">AI 전략 분석 리포트 — {badge_txt}</p>
    <div class="card-footer">
      <span class="card-date">{date_str} · v1.0</span>
      <div style="display:flex;align-items:center;gap:8px;">
        <span class="card-status status-done">완료</span>
        <div class="card-arrow" aria-hidden="true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" stroke-width="2.5"><path d="M7 17L17 7M17 7H7M17 7v10"/></svg>
        </div>
      </div>
    </div>
  </div>
</a>"""

    content = RESEARCH_ARCHIVE.read_text(encoding="utf-8")
    hint = "<!-- 리포트 추가 힌트 -->"
    if hint not in content:
        return False

    # 카드 삽입
    content = content.replace(hint, card_html + "\n" + hint)

    # 카운트 +1
    import re
    def inc_count(m):
        n = int(m.group(1))
        return m.group(0).replace(str(n), str(n + 1))
    content = re.sub(r'(<span class="section-meta" id="reportMeta">)(\d+)(개</span>)', inc_count, content)

    RESEARCH_ARCHIVE.write_text(content, encoding="utf-8")
    return True

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

    parts = data.split("|")
    action  = parts[0]
    job_id  = parts[1] if len(parts) > 1 else ""
    
    # ── Claude 고도화 ───────────────────────────────────────────
    if action == "claude_upgrade":
        answer_callback(cb_id, "📊 Claude 리포트 생성 중... (약 30초 소요)")
        send_telegram_direct(f"📊 <b>Claude 리포트 생성 중...</b>\n🆔 <code>{job_id}</code>")

        import threading as _th
        def _run_claude():
            try:
                import subprocess as _sp
                ppt = ROOT_DIR / "scripts" / "ppt_engine_v4.py"
                out = ROOT_DIR / "outputs" / "03_final_reports"
                r = _sp.run(
                    [sys.executable, str(ppt), "--job-id", job_id,
                     "--output", str(out), "--report-type", "standard"],
                    cwd=str(ROOT_DIR), capture_output=True, text=True
                )
                if r.returncode != 0:
                    send_telegram_direct(f"❌ Claude 리포트 생성 실패\n<code>{r.stderr[:200]}</code>")
                    return

                base = os.environ.get("GITHUB_PAGES_URL", "").rstrip("/")
                link = f"\n🌐 <a href='{base}/reports/{job_id}_precision_report.html'>Claude 리포트 바로보기</a>" if base else ""
                send_telegram_direct(
                    f"📊 <b>Claude 리포트 완성 — 리포트 1</b>\n\n"
                    f"🆔 <code>{job_id}</code>{link}"
                )

                # 업로드 상태 확인
                send_telegram_direct(
                    f"📁 <b>웹 허브 배포 확인</b>\n\n"
                    f"안티그래비티 마스터 허브(Web)에 배포하시겠습니까?",
                    reply_markup={
                        "inline_keyboard": [
                            [{"text": "🚀 웹 사이트 즉시 배포", "callback_data": f"publish_archive|{job_id}|standard"}],
                            [{"text": "❌ 건너뜀",    "callback_data": f"skip_publish|{job_id}"}],
                        ]
                    }
                )
            except Exception as e:
                send_telegram_direct(f"❌ Claude 고도화 오류: {e}")

        _th.Thread(target=_run_claude, daemon=True).start()

    # ── 아카이브 업로드 승인 ─────────────────────────────────────
    elif action == "publish_archive":
        report_type = data.split("|")[2] if data.count("|") >= 2 else "standard"
        answer_callback(cb_id, "⏳ 웹 허브 배포 중...")
        send_telegram_direct(f"⏳ <b>웹 허브 배포 중...</b>\n🆔 <code>{job_id}</code>")
        try:
            import subprocess as _sp, threading as _th

            def _do_publish():
                # GitHub Pages 배포 (Drive 업로드는 스크립트 내부에서 이미 제거됨)
                pub = ROOT_DIR / "scripts" / "publish_to_docs.py"
                _sp.run([sys.executable, str(pub), job_id],
                        cwd=str(ROOT_DIR), capture_output=True)

                label = "딥 인텔 리포트" if report_type == "deep-intel" else "Claude 리포트"
                send_telegram_direct(
                    f"✅ <b>배포 완료</b>\n\n"
                    f"📌 {label}: <code>{job_id}</code>\n"
                    f"🌐 <b>마스터 허브:</b> GitHub Pages 배포 완료"
                )

            _th.Thread(target=_do_publish, daemon=True).start()
        except Exception as e:
            send_telegram_direct(f"❌ 배포 오류: {e}")

    # ── 업로드 건너뜀 ────────────────────────────────────────────
    elif action == "skip_publish":
        answer_callback(cb_id, "건너뜀")
        send_telegram_direct(f"↩️ 업로드를 건너뜁니다. (<code>{job_id}</code>)")

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
        send_telegram_direct(f"✅ <b>피드백이 저장되었습니다.</b>\n\n내용: <i>{text}</i>\n다음 리포트 생성 시 자동 반영됩니다.")
        return
        
    # 1. '수정' 또는 '보완' 요청
    if "수정" in text or "보완" in text:
        feedback_path = ROOT_DIR / "state" / "last_feedback.txt"
        feedback_path.parent.mkdir(parents=True, exist_ok=True)
        feedback_path.write_text(text, encoding="utf-8")
        
        send_telegram_direct(f"📝 <b>수정 요청이 접수되었습니다.</b>\n내용: <i>{text}</i>\n다음 리포트 생성 시 이 내용을 반영하여 분석을 강화합니다.")
        
        # Auto-trigger if urgent keywords present
        if any(k in text for k in ["다시", "하면", "직후", "바로", "해줘"]):
            job_id = get_last_job_id()
            if job_id:
                subprocess.Popen([sys.executable, str(ROOT_DIR / "scripts" / "advanced_analysis.py"), job_id], cwd=str(ROOT_DIR))

    else:
        send_telegram_direct(
            "✅ <b>메시지를 확인했습니다.</b>\n\n"
            "💡 <b>명령어 가이드</b>\n"
            "• <b>[내용] 보완해줘</b> — 피드백 반영 후 재분석\n\n"
            "리포트(Claude)는 OT 업로드 시 자동 생성됩니다."
        )

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
