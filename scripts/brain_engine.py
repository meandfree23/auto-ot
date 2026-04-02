import os
import sys
import json
import re
from pathlib import Path
from docx import Document
import pypdf
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# V20.0 Contextual Intelligence Engine (High-Fidelity Analysis)
# Powered by Google Gemini API for true semantic extraction

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

SUMMARY_DIR = ROOT / "outputs" / "01_summaries"
DEEP_DIR = ROOT / "outputs" / "02_deep_analysis"
SUMMARY_DIR = ROOT / "outputs" / "01_summaries"
DEEP_DIR = ROOT / "outputs" / "02_deep_analysis"

for d in [SUMMARY_DIR, DEEP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def extract_text_from_docx(docx_path: Path) -> str:
    """Extract all text from a docx file."""
    if not docx_path.exists():
        return ""
    try:
        doc = Document(str(docx_path))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"[Brain] Error reading docx: {e}")
        return ""

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from a PDF file."""
    if not pdf_path.exists():
        return ""
    text = []
    try:
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception as e:
        print(f"[Brain] Error reading PDF: {e}")
        return ""

def extract_content(file_path: Path) -> str:
    """Detect file type and extract content."""
    suffix = file_path.suffix.lower()
    if suffix == ".docx":
        return extract_text_from_docx(file_path)
    elif suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    elif suffix in [".txt", ".md"]:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    return ""

def identify_strategic_intent(content: str):
    """
    V21.0: Real Intelligence Integration.
    Calls Gemini API to deeply understand and extract core intents.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or "your_" in api_key.lower():
        print("[Brain] WARNING: GEMINI_API_KEY not set. Using legacy keyword extraction.")
        return _legacy_identify_intent(content)
        
    prompt = f"""당신은 최고급 브랜드 컨설턴트 및 글로벌 제안 전략가입니다.
다음 제공된 클라이언트 OT 문서를 심층 분석하여, 최고급 컨설팅 보고서 형식(개조식, 명사형 종결, 예: "~함.", "~구축 전략.")으로 3페이지 분량의 기획 뼈대를 잡아주세요.
결과는 반드시 JSON 형식으로 반환해야 하며, 아래 3대 핵심 카테고리 배열에 각각 4~5개의 **날카롭고 인사이트 넘치는 핵심 전략 문장**을 담아주세요.

# 출력 JSON 스키마:
{{
  "Market Intelligence": ["시장 트렌드, 타겟 소비자의 핵심 결핍(Pain-point), 경쟁 현황 등 분석 문장 배열"],
  "Strategic Logic": ["본 캠페인의 프로젝트 돌파 전략, 논리적 해결 방향, 단기/장기 목표 문장 배열"],
  "Creative & Visual": ["전략을 실현할 구체적 크리에이티브 시안, 핵심 메시지, 모델 활용, 비주얼 연출안 문장 배열"]
}}

# 문서 원본 요약:
{content[:8000]}
"""
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", 
                temperature=0.3,
                tools=[{"google_search": {}}]
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"[Brain Error] Gemini API failed: {e}. Falling back to legacy.")
        return _legacy_identify_intent(content)

def _legacy_identify_intent(content: str):
    """Fallback legacy logic if API fails"""
    lines = content.split("\n")
    sections = {"Market Intelligence": [], "Strategic Logic": [], "Creative & Visual": []}
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5: continue
        lower = line.lower()
        if any(k in lower for k in ["문제", "시장", "타겟", "결핍"]): sections["Market Intelligence"].append(line)
        elif any(k in lower for k in ["전략", "솔루션", "방안", "아이디어"]): sections["Strategic Logic"].append(line)
        elif any(k in lower for k in ["크리에이티브", "컨셉", "비주얼", "연출"]): sections["Creative & Visual"].append(line)
    return sections

def generate_reports(job_id: str, content: str, file_name: str):
    """
    V20.0 High-Fidelity Synthesis.
    Generates 'News-worthy' strategy and deep OT analysis.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = file_name.replace(".docx", "").replace(".pdf", "")
    
    intent = identify_strategic_intent(content)
    
    # Fallback to general insights if empty
    def clean_line(l):
        return re.sub(r'^[\s\•\-\*]+', '', l).strip()

    mi = [clean_line(l) for l in intent.get("Market Intelligence", []) if len(clean_line(l)) > 5]
    sl = [clean_line(l) for l in intent.get("Strategic Logic", []) if len(clean_line(l)) > 5]
    cv = [clean_line(l) for l in intent.get("Creative & Visual", []) if len(clean_line(l)) > 5]

    mi = mi if mi else ["시장 트렌드 변화 및 프리미엄 타겟 니즈 분석."]
    sl = sl if sl else ["데이터 기반 타겟팅 최적화 및 신규 어젠다 선점 전략."]
    cv = cv if cv else ["핵심 인플루언서 연계 숏폼 비주얼 기획안 도출."]

    mi_str = "\n".join([f"- {l}" for l in mi[:5]])
    sl_str = "\n".join([f"- {l}" for l in sl[:5]])
    cv_str = "\n".join([f"- {l}" for l in cv[:5]])
    keywords_list = re.findall(r'\b\w{2,}\b', content)[:5]
    keywords_str = ', '.join(keywords_list)

    # 1. Authentic Consultant Summary Report
    summary_md = f"""# [{title}] OT 분석 기획안 (1차)

## 1. 프로젝트 메타 인텔리전스
- **수집 ID**: `{job_id}`
- **분석 코어**: Antigravity V25.0 (Consultant Model)
- **키 필터링**: {keywords_str}

## Market Intelligence
{mi_str}

## Strategic Logic
{sl_str}

## Creative & Visual
{cv_str}

---
© 2026 Antigravity | 1차 브리핑 데이터 추출 완료. 
(이 파일을 기반으로 2차 딥-리서치가 PPTX를 생성합니다.)
"""

    # 5. Write Files (Only Summary in Phase 1)
    summary_path = SUMMARY_DIR / f"{job_id}_summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")
    
    print(f"[Brain] Generated: {summary_path.name}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        job_id = sys.argv[1]
        # Standalone test call
        generate_reports(job_id, "Sample content with bullets • Target goal: Win the market.", "Standalone_Test")
