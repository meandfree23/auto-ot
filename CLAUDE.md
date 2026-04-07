# 🛡️ CLAUDE Project Harness (V26.0)
# Optimization for Claude Token Efficiency & Strategic Intelligence

## 🎯 Project Overview
- **Name**: OT Automation Pipeline (오티 자동화)
- **Goal**: High-fidelity strategic analysis from client briefs (PDF/DOCX) to web-based HTML/PPTX reports.
- **Key Architect**: Antigravity Consultant Agent.

## 🏗️ Technical Harness (Directory Skeleton)
- `/scripts`: Core logic (Orchestrators, Engines, Connectors).
- `/templates`: HTML/PPT templates for rendering.
- `/skills`: Agentic capabilities (MCP-like modular tasks).
- `/outputs`: Final reports (Ignore in scans via `.claudeignore`).

## 🗝️ Core Rules (Token-Efficient Engineering)
> "모델이 멍청한 짓을 하지 않도록 시스템적으로 억제한다."

1. **Silence is Golden**: 
   - 불필요한 서술형 설명을 지양하고, 결과물(코드/분석) 중심으로 답변합니다. 
   - "알겠습니다", "작성을 시작하겠습니다"와 같은 채티(Chatty)한 문구를 최소화합니다.
2. **XML Tagging**: 
   - 중요한 지시나 컨텍스트 데이터는 `<task>`, `<context>`, `<rules>` 태그로 감싸서 전달합니다.
3. **Planning First**: 
   - 복잡한 작업은 반드시 `implementation_plan.md`를 통해 먼저 설계하고 승인 후 실행합니다.
4. **No Placeholders**: 
   - 가짜 데이터나 URL 대신, 실제 작동하는 이미지 라이브러리(Unsplash)나 검색 도구를 사용합니다.

## 📜 Development Standards
- **Python**: Modular, functional style. Use Pydantic or TypedDict for JSON returns.
- **LLM Engine**: Primary - `gemini-2.5-flash` (for high-speed ingestion), Specialist - `Claude 3.5 Sonnet` (for strategic reasoning).

## 💡 Token Management Hacks
- 대화가 길어질 경우: `/compact`를 사용하여 이전 컨텍스트를 압축하십시오.
- 새로운 대과업 시작 시: `/clear`를 통해 메모리 누적을 초기화하되, `CLAUDE.md`는 항상 유지됩니다.

---
© 2026 Antigravity | Strategic Harness Enabled.
