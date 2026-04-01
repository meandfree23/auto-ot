---
description: Pipeline for high-density 20-page PPT generation using NotebookLM-style research.
---

# /nlm-pptx-pipeline

This workflow transforms a standard orientation or brief into a 20-page "Precision Intelligence" PPT report with maximum content density.

## Flow
1. **Fact Extraction (NLM Context)**:
   - Identify 20 strategic pivots from the brief and deep research.
   - For each pivot, expand into a "Full Page" block (5-7 bullet points + 1 strategic label).
2. **Bridge Construction**:
   - Use `scripts/antigravity_bridge.py` to curate the 20-slide dataset.
   - Ensure the "Density" requirement is met by cross-referencing industry trends (Web Research).
3. **Engine Run (PPTX/HTML)**:
   - Invoke `scripts/ppt_engine_v4.py` to generate the 20P deck.
   - Target Directory: `outputs/03_final_reports/`.
4. **Publish & Notify**:
   - Run `scripts/publish_to_docs.py` for Drive upload and Direct URL generation.
   - Send Telegram "레퍼런스 페이지 완료" notification.

## Rules
- **density_first**: Each slide must contain at least 200 words of analyzed content or a dense data table.
- **precision_logic**: Use terms like "Macro Analysis", "Strategic Pivot", "Consumer Persona" for a premium feel.
