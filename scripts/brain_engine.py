import os
import sys
from pathlib import Path
from docx import Document
import pypdf
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

SUMMARY_DIR = ROOT / "outputs" / "01_summaries"
DEEP_DIR = ROOT / "outputs" / "02_deep_analysis"

for d in [SUMMARY_DIR, DEEP_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def extract_text_from_docx(docx_path: Path) -> str:
    if not docx_path.exists():
        return ""
    try:
        doc = Document(str(docx_path))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"[Brain] Error reading docx: {e}")
        return ""


def extract_text_from_pdf(pdf_path: Path) -> str:
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
    suffix = file_path.suffix.lower()
    if suffix == ".docx":
        return extract_text_from_docx(file_path)
    elif suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    elif suffix in [".txt", ".md"]:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    return ""


ANALYSIS_PROMPT = """\
당신은 대한민국 최고 수준의 광고/브랜드 전략 컨설턴트입니다.
아래 클라이언트 OT 원문을 분석하여, 실무 기획팀이 바로 활용할 수 있는 전략 리포트를 작성하세요.

# 절대 준수 규칙:
1. 반드시 원문에 실제로 있는 내용을 근거로 작성할 것 (없는 내용 창작 금지)
2. "브랜드 인지도 향상", "타겟 확장", "소통 강화" 같은 클리셰 표현 사용 금지
3. 각 섹션마다 원문의 구체적인 내용(수치, 키워드, 상황)을 직접 인용하거나 반영할 것
4. 불릿 3개 이상, 표 1개 이상 필수 포함

# 출력 형식 (아래 마크다운 구조 그대로 유지):

## Market Intelligence
> [원문에서 도출한 시장/과제의 핵심 상황 한 줄]
- [시장 현황 또는 경쟁 환경 — 원문 근거 포함]
- [타겟 소비자 특성 또는 Pain-point — 원문 근거 포함]
- [주목해야 할 트렌드 또는 기회 — 원문 근거 포함]
| 구분 | 현황 | 전략적 시사점 |
|------|------|--------------|
| (항목1) | (원문 기반 현황) | (대응 방향) |
| (항목2) | (원문 기반 현황) | (대응 방향) |

## Strategic Logic
> [이번 프로젝트의 핵심 전략 방향 한 줄 선언]
- [주요 전략 1 — 구체적 실행 방안 포함]
- [주요 전략 2 — 차별화 포인트 포함]
- [주요 전략 3 — 기대 효과 포함]
| Phase | 핵심 Action | 기대 KPI |
|-------|------------|---------|
| 1단계 | (구체적 행동) | (측정 지표) |
| 2단계 | (구체적 행동) | (측정 지표) |

## Creative & Visual
> [이번 캠페인 크리에이티브 컨셉 한 줄]
- [크리에이티브 방향 1 — 포맷/채널 명시]
- [크리에이티브 방향 2 — 핵심 메시지/카피 방향]
- [크리에이티브 방향 3 — 비주얼 톤앤매너]
| 포맷 | 연출 의도 | 톤앤매너 |
|------|----------|---------|
| (형식) | (연출 방향) | (분위기) |
| (형식) | (연출 방향) | (분위기) |

## Gap Check
- [OT에서 불명확하거나 추가 확인이 필요한 사항 1]
- [OT에서 불명확하거나 추가 확인이 필요한 사항 2]
- [잠재적 리스크 또는 주의 포인트]

---
# 분석할 OT 원문 ({title}):
{content}

위 원문을 반드시 반영하여 작성하세요:"""


def analyze_with_claude(content: str, file_name: str) -> str:
    """
    Claude API로 OT 문서 분석. Anthropic API 키 사용.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[Brain] ANTHROPIC_API_KEY 없음. Gemini로 시도.")
        return analyze_with_gemini(content, file_name)

    title = file_name.replace(".docx", "").replace(".pdf", "").strip()
    prompt = ANALYSIS_PROMPT.format(title=title, content=content[:12000])

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        result = message.content[0].text.strip()
        print("[Brain] Claude 분석 완료.")
        return result
    except Exception as e:
        print(f"[Brain Error] Claude API 실패: {e}. Gemini로 시도.")
        return analyze_with_gemini(content, file_name)


def analyze_with_gemini(content: str, file_name: str) -> str:
    """
    Gemini API 폴백. GEMINI_API_KEY 사용.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or "your_" in api_key.lower():
        return _fallback_report(content, file_name)

    title = file_name.replace(".docx", "").replace(".pdf", "").strip()
    prompt = ANALYSIS_PROMPT.format(title=title, content=content[:12000])

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        for model_id in ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.0-flash-lite']:
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.4)
                )
                print(f"[Brain] Gemini({model_id}) 분석 완료.")
                return response.text.strip()
            except Exception as model_err:
                if ('503' in str(model_err) or '429' in str(model_err)) and model_id != 'gemini-2.0-flash-lite':
                    print(f"[Brain] {model_id} 불가, 다음 모델 시도...")
                    continue
                raise model_err
    except Exception as e:
        print(f"[Brain Error] Gemini 실패: {e}.")
        return _fallback_report(content, file_name)


def _fallback_report(content: str, file_name: str) -> str:
    lines = [l.strip() for l in content.split("\n") if l.strip() and len(l.strip()) > 10]
    bullets = "\n".join([f"- {l}" for l in lines[:5]]) or "- 원문 내용 추출 실패"
    return f"""## Market Intelligence
> API 미연결 — 원문 발췌 기반 임시 리포트
{bullets}
| 구분 | 내용 |
|------|------|
| 원문 | {file_name} |

## Strategic Logic
> API 키 설정 후 재분석 필요
- ANTHROPIC_API_KEY 또는 GEMINI_API_KEY를 .env에 설정하세요.

## Creative & Visual
> API 키 설정 후 재분석 필요
- 설정 후 파일을 재업로드하거나 재실행하세요.

## Gap Check
- API 키 미설정 상태입니다."""


def generate_reports(job_id: str, content: str, file_name: str) -> bool:
    """
    Claude(우선) → Gemini(폴백) 순서로 분석.
    deep_report.md와 summary.md를 저장.
    """
    print(f"[Brain] 분석 시작: {file_name} ({len(content)}자)")
    title = file_name.replace(".docx", "").replace(".pdf", "").strip()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    analysis_md = analyze_with_claude(content, file_name)

    deep_report = f"# {title}\n\n{analysis_md}\n"
    deep_path = DEEP_DIR / f"{job_id}_deep_report.md"
    deep_path.write_text(deep_report, encoding="utf-8")

    summary_md = f"""# {title} — OT 분석 요약
- **Job ID**: `{job_id}`
- **분석 일시**: {date_str}
- **원본 파일**: {file_name}
- **원문 길이**: {len(content):,}자

{analysis_md}
"""
    summary_path = SUMMARY_DIR / f"{job_id}_summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")

    print(f"[Brain] 완료: {deep_path.name}")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 2:
        job_id = sys.argv[1]
        content = Path(sys.argv[2]).read_text(encoding="utf-8")
        generate_reports(job_id, content, Path(sys.argv[2]).name)
