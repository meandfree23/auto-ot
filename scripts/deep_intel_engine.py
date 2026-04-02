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

def notify_telegram(msg: str, reply_markup: dict = None):
    """Utility to send telegram notifications."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
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
        ppt_script = ROOT / "scripts" / "ppt_engine_v4.py"
        if ppt_script.exists():
            subprocess.run([sys.executable, str(ppt_script), "--job-id", job_id, "--mode", "advanced"], cwd=str(ROOT))
        
        # 5. Auto-Publish & Grab Links
        notify_telegram(f"🌐 <b>결과물 클라우드 배포 중...</b>\n웹 대시보드와 PPTX를 연동하고 있습니다.")
        
        publish_script = ROOT / "scripts" / "publish_to_docs.py"
        html_link = "생성 중 오류 발생"
        pptx_link = "생성 중 오류 발생"
        
        if publish_script.exists():
            # Run the publish script and capture stdout
            pub_res = subprocess.run([sys.executable, str(publish_script), job_id], cwd=str(ROOT), capture_output=True, text=True)
            try:
                # Parse JSON output from the script (it prints formatted json at the end)
                # Find the last valid JSON block
                output_str = pub_res.stdout.strip()
                # Find the start of the JSON block (usually {)
                start_idx = output_str.find('{')
                if start_idx != -1:
                    json_str = output_str[start_idx:]
                    pub_data = json.loads(json_str)
                    
                    if "published_docs" in pub_data:
                        for doc in pub_data["published_docs"]:
                            if doc["title"].endswith(".html") and "direct_url" in doc:
                                html_link = doc["direct_url"]
                            elif doc["title"].endswith(".pptx"):
                                pptx_link = doc["url"]
            except Exception as e:
                print(f"[Deep Intel] Publish JSON parse error: {e}\nRaw output: {pub_res.stdout}")

        final_msg = (
            f"🏆 <b>딥 리서치 패키지 완성!</b>\n\n"
            f"🆔 <code>{job_id}</code>\n\n"
            f"<b>[결과물 바로보기 링크]</b>\n"
            f"🌐 <a href='{html_link}'>1. 최고급 웹 대시보드 (스마트폰 즉시 열람)</a>\n\n"
            f"📊 <a href='{pptx_link}'>2. 전략 파워포인트 문서 (드라이브 뷰어/다운로드)</a>\n\n"
            f"<i>* 아래 버튼을 눌러 언제든 즉시 수정을 지시할 수 있습니다.</i>"
        )
        
        reply_markup = {
            "inline_keyboard": [
                [{"text": "📝 피드백/수정 지시 추가하기", "callback_data": f"request_edit|{job_id}"}]
            ]
        }
        
        notify_telegram(final_msg, reply_markup=reply_markup)
        print(f"🏆 [Deep Intel] DONE: Full package delivered with URLs for {job_id}")
    except Exception as e:
        print(f"❌ [Deep Intel Error] {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 deep_intel_engine.py <job_id>")
        sys.exit(1)
    run_orchestrator(sys.argv[1])
