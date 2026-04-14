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
제공된 1차 분석 요약본과 사용자 피드백(있을 경우)을 바탕으로, 이 프로젝트를 초격차 수준으로 고도화하여 '완전판 심층 리포트'를 작성해 주세요.
결과는 순수 마크다운(Markdown) 텍스트로만 반환하세요.

[핵심 지시사항: 리치 미디어(Rich Media) 시각 자료 적극 활용]
단순 텍스트(불릿) 나열은 금지합니다. 트렌드를 증명하는 **풍부한 시각적 근거**를 각 카테고리마다 반드시 삽입하세요!
1. **뉴스/SNS 인용구 (`>`)**: 핵심 트렌드 멘트, 뉴스 요약, 또는 강렬한 전략적 선언은 반드시 마크다운 블록 인용구(`>`)로 강조하세요.
2. **트렌드 이미지 (`![alt](url)`)**: 상황을 가장 잘 묘사하는 저작권 무료(Unsplash 등) 이미지 URL을 각 카테고리에 최소 1장씩 꼭 삽입하세요. (예: `![market trend](https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80)`)
3. **데이터 표 (`| | |`)**: 시장 규모, 경쟁사 비교, 전략 마일스톤, 파급 효과 등은 반드시 깔끔한 마크다운 데이터 표(Table)로 요약하세요. (각 단원별 минимум 1개 표 포함)

# 필수 마크다운 구조 가이드 (반드시 아래 구조와 풍부한 미디어를 유지할 것):
## Market Intelligence
> [해당 시장의 가장 중요한 뉴스 기사나 SNS 트렌드 인용구]
![market reference image](https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80)
- [시장 현황 분석 문장 1]
- [시장 현황 분석 문장 2]
| 구분 | 현황 | 트렌드 지수 |

## Strategic Logic
> [우리의 전략을 관통하는 한 줄의 핵심 선언]
![strategy concept image](https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80)
- [전략 전개 문장 1]
- [전략 전개 문장 2]
| 전략 Phase | 세부 Action Plan | 핵심 KPI |

## Creative & Visual
> [이번 크리에이티브의 핵심 컨셉 인용]
![creative reference image](https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&q=80)
- [크리에이티브 구현 방안 1]
- [크리에이티브 구현 방안 2]
| 장면(Scene) | 연출 의도 | 시각적 톤앤매너 |

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
            config=types.GenerateContentConfig(
                temperature=0.7,
                tools=[{"google_search": {}}]
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Deep Intel Error] Gemini call failed: {e}")
        return content

def run_orchestrator(job_id: str):
    print(f"🌍 [Deep Intel] Initiating Global Deep Research for {job_id}...")
    
    # 1. Load context via Bridge
    from scripts.antigravity_bridge import load_markdown
    summary, deep_txt, _ = load_markdown(job_id)
    
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
    
    # 3. Save Deep Intel Report to its own directory (never overwrites brain_engine output)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    deep_intel_path = RESEARCH_DIR / f"{job_id}_deep_intel_report.md"

    final_md = f"# [{job_id}] 초격차 딥-리포트\n\n{deep_report_md}"
    deep_intel_path.write_text(final_md, encoding="utf-8")
    
    # 4. Generate Deep Intel HTML report
    try:
        ppt_script = ROOT / "scripts" / "ppt_engine_v4.py"
        if ppt_script.exists():
            subprocess.run(
                [sys.executable, str(ppt_script), "--job-id", job_id, "--report-type", "deep-intel"],
                cwd=str(ROOT), capture_output=True
            )

        # 5. Publish to GitHub Pages
        notify_telegram(f"🌐 <b>리포트 2 배포 중...</b>")
        publish_script = ROOT / "scripts" / "publish_to_docs.py"
        if publish_script.exists():
            subprocess.run(
                [sys.executable, str(publish_script), job_id],
                cwd=str(ROOT), capture_output=True
            )

        # 6. Construct URL directly and ask for archive upload approval
        base_url = os.environ.get("GITHUB_PAGES_URL", "").rstrip("/")
        if base_url:
            deep_intel_url = f"{base_url}/reports/{job_id}_deep_intel_report.html"
            report_link = f"\n🌐 <a href='{deep_intel_url}'>딥 인텔 리포트 바로보기</a>"
        else:
            report_link = ""

        final_msg = (
            f"🏆 <b>딥 인텔 리포트 완성 — 리포트 2</b>\n\n"
            f"🆔 <code>{job_id}</code>"
            f"{report_link}\n\n"
            f"<i>Gemini 2.5 + Google Search 기반 글로벌 확장 분석</i>"
        )
        notify_telegram(final_msg)

        # 7. Ask for archive upload approval
        archive_msg = (
            f"📁 <b>Strategic Research Archive 업로드</b>\n\n"
            f"안티그래비티 마스터 허브 및 리서치 아카이브에\n"
            f"딥 인텔 리포트를 등록하시겠습니까?"
        )
        reply_markup = {
            "inline_keyboard": [
                [{"text": "✅ 업로드 승인", "callback_data": f"publish_archive|{job_id}|deep-intel"}],
                [{"text": "❌ 건너뜀", "callback_data": f"skip_publish|{job_id}"}],
            ]
        }
        notify_telegram(archive_msg, reply_markup=reply_markup)
        print(f"🏆 [Deep Intel] DONE for {job_id}")
    except Exception as e:
        print(f"❌ [Deep Intel Error] {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 deep_intel_engine.py <job_id>")
        sys.exit(1)
    run_orchestrator(sys.argv[1])
