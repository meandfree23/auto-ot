import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import html

# Load environment variables
load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_message(text: str):
    if not TOKEN or not CHAT_ID:
        print("[Telegram] Missing TOKEN or CHAT_ID in .env. Skipping notification.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        print(f"[Telegram] Notification sent successfully.")
    except Exception as e:
        print(f"[Telegram] Failed to send message: {e}")

def format_notification(job_id: str, log_path: Path, status: str = "finished", file_name: str = None, data: dict = None) -> str:
    display_name = file_name or job_id
    
    if status == "accepted":
        return (
            f"📥 <b>문서 수락 알림</b>\n\n"
            f"📄 <b>파일명:</b> {html.escape(display_name)}\n"
            f"📌 <b>작업 ID:</b> <code>{job_id}</code>\n\n"
            f"문서를 정상적으로 수락했습니다. 현재 3페이지 분량의 <b>전략 심층 보고서</b>를 생성 중입니다. 잠시만 기다려 주세요!"
        )

        msg = f"<b>✅ 전략 심층 보고서(3P) 분석 완료!</b>\n\n"
        msg += f"📄 <b>파일명:</b> {html.escape(display_name)}\n"
        msg += f"📌 <b>작업 ID:</b> <code>{job_id}</code>\n\n"
        msg += "프로젝트의 핵심 목표와 전문 전략을 담은 심층 보고서 분석이 완료되었습니다.\n\n"
        
        msg += "💡 <b>추가 작업 안내:</b>\n"
        msg += "20페이지 분량의 <b>프리젠테이션 슬라이드 리포트</b>가 필요하시다면 <b>'고도화 해줘'</b>라고 메시지를 보내주세요."
        return msg

    if status == "COMPLETED_V5" or status == "ADVANCED_DONE":
        html_url = data.get("html_url") if data else ""
        direct_link = ""
        
        # [V16.0] Resolve GitHub Pages Direct Link
        if log_path.exists():
            try:
                log_data = json.loads(log_path.read_text(encoding="utf-8"))
                docs = log_data.get("published_docs", [])
                for d in docs:
                    if d.get('direct_url'):
                        direct_link = d['direct_url']
                        break
            except: pass
        
        if not direct_link and html_url:
            direct_link = html_url

        msg = f"<b>🏆 딥 인텔리전스 고도화 완료 (V16.0)</b>\n\n"
        msg += f"📄 <b>파일명:</b> {html.escape(display_name)}\n"
        msg += f"📌 <b>작업 ID:</b> <code>{job_id}</code>\n\n"
        msg += "전 세계 시장 데이터와 경쟁사 분석을 포함한 20P+ 심층 인텔리전스 리포트 생성을 완료했습니다.\n\n"
        
        if direct_link:
            msg += f"🚀 <b>다이렉트 감상:</b> <a href='{direct_link}'>여기를 클릭하여 슬라이드 열기 (추천)</a>\n\n"
        
        msg += "━━━━━━━━━━━━━━━━━━\n"
        msg += "감사합니다. 모든 고도화 작업이 성공적으로 완료되었습니다."
        return msg

    return f"<b>✅ 작업 상태 업데이트 ({status})</b>\nID: {job_id}"

def run_telegram_notification(job_id: str, status: str = "finished", file_name: str = None, data: dict = None):
    """Programmatic entry point for other scripts."""
    root = Path(__file__).resolve().parents[1]
    log_path = root / "outputs" / "logs" / f"{job_id}_publish.json"
    message = format_notification(job_id, log_path, status, file_name, data)
    send_message(message)

def main():
    if len(sys.argv) < 2: return
    job_id = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) >= 3 else "finished"
    file_name = sys.argv[3] if len(sys.argv) >= 4 else None
    
    run_telegram_notification(job_id, status, file_name)

if __name__ == "__main__":
    main()
