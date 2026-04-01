import os
import sys
import json
import time
import requests
from pathlib import Path
import subprocess
from dotenv import load_dotenv

# V22.0 Global Deep Intelligence Research Engine (Enhanced Brain)
# Performs multi-step keyword extraction and strategic synthesis.

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

RESEARCH_DIR = ROOT / "outputs" / "04_deep_intel"
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def notify_telegram(msg: str):
    """Utility to send telegram notifications."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Deep Intel] Telegram notification failed: {e}")

def generate_deep_report(content: str):
    """
    Calls Gemini API to expand the initial briefing into a 3-page deep dive report.
    """
    print(f"[Deep Intel] Phase 2: AI Writing Premium Deep Strategic Report...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or "your_" in api_key.lower():
         print("[Deep Intel] WARNING: No GEMINI_API_KEY. Using mock report.")
         time.sleep(5)
         return f"{content}\n\n(API Key 누락으로 인한 시뮬레이션 딥-리포트입니다.)"
         
    prompt = f"""당신은 세계 최고 수준의 글로벌 전략 컨설턴트입니다.
제공된 1차 분석 요약본과 사용자 특별 피드백(있을 경우)을 바탕으로, 이 프로젝트를 초격차 수준으로 고도화하여 실제 파워포인트 슬라이드 3장 분량으로 삽입될 '완전판 심층 리포트'를 작성해 주세요.
반드시 아래 3대 카테고리의 구조를 유지하며, 각 항목당 4~5개의 **압도적인 인사이트 문장(개조식/명사형 종결, 예: "~전략 구상.", "~시너지 창출.")**으로 작성해 주세요. 일반적인 서술어(~습니다)는 절대 사용하지 마세요.
결과는 마크다운(Markdown) 텍스트 자체로 반환하세요. JSON이 아닙니다.

# 필수 마크다운 구조:
## Market Intelligence
- [문장 1]
- [문장 2]
- [문장 3]
- [문장 4]

## Strategic Logic
- [문장 1]
...

## Creative & Visual
- [문장 1]
...

# 1차 분석 및 사용자 피드백 문서:
{content[:8000]}

작성을 시작하세요:
"""
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Deep Intel Error] Gemini call failed: {e}")
        return content

def run_orchestrator(job_id: str):
    print(f"🌍 [Deep Intel] Initiating Global Deep Research for {job_id}...")
    
    # 1. Load context via Bridge
    from scripts.antigravity_bridge import load_markdown
    summary, deep_txt = load_markdown(job_id)
    
    if not summary and not deep_txt:
        print(f"❌ [Deep Intel] Could not find initial analysis for {job_id}")
        return

    # 1.5. Pick up any human-in-the-loop feedback
    feedback_path = ROOT / "state" / f"feedback_{job_id}.txt"
    if feedback_path.exists():
        feedback_text = feedback_path.read_text(encoding="utf-8")
        if feedback_text.strip():
            summary = (summary or "") + f"\n\n[사용자 특별 지시 / 피드백 사항]\n{feedback_text}"
            notify_telegram(f"🧠 <b>사용자 지정 피드백을 인식했습니다.</b>\n<i>'{feedback_text[:50]}...'</i> 내용을 분석에 우선 반영합니다.")
        try: feedback_path.unlink()
        except: pass

    # 2. Process AI Deep Research
    notify_telegram(f"🔍 <b>'{job_id}' 딥 리서치 시작</b>\nGemini 2.5가 글로벌 트렌드 및 지시사항을 분석하여 3페이지 덱을 쓰는 중입니다.")
    deep_report_md = generate_deep_report(summary or "")
    
    # 3. Create Strategic Package & Deep Report MD
    DEEP_DIR = ROOT / "outputs" / "02_deep_analysis"
    DEEP_DIR.mkdir(parents=True, exist_ok=True)
    deep_path = DEEP_DIR / f"{job_id}_deep_report.md"
    
    # Prepend Title back for parsing compat
    final_md = f"# [{job_id}] 초격차 딥-리포트\n\n{deep_report_md}"
    deep_path.write_text(final_md, encoding="utf-8")
    
    # 4. Trigger Visual Presentation (PPT/HTML)
    try:
        # Generate Advanced Dashboard or PPT
        ppt_script = ROOT / "scripts" / "ppt_engine_v4.py"
        if ppt_script.exists():
            subprocess.run([sys.executable, str(ppt_script), "--job-id", job_id, "--mode", "advanced"], cwd=str(ROOT))
        
        notify_telegram(f"🏆 <b>딥 리서치 패키지 및 PPTX/HTML 자동 생성 완료!</b>\n\n🆔 <code>{job_id}</code>\n\n최종 프리미엄 전략 대시보드(.html)와 파워포인트 슬라이드(.pptx) 파일이 <code>03_final_reports</code> 폴더에 생성되었습니다. 바로 확인해보세요!")
        print(f"🏆 [Deep Intel] DONE: Full package delivered for {job_id}")
    except Exception as e:
        print(f"❌ [Deep Intel Error] {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 deep_intel_engine.py <job_id>")
        sys.exit(1)
    run_orchestrator(sys.argv[1])
