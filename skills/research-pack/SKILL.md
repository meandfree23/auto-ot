---
name: research-pack
description: Collect only the research needed to reduce uncertainty and strengthen strategic or creative decisions.
---

# Skill: research-pack

## Purpose
Collect only the research needed to reduce uncertainty and strengthen strategic or creative decisions.

This skill should improve judgment, not merely gather information.

## When to Use
Use this skill after:
- `ot-intake`
- `gap-check`

Run research only when it helps answer a real uncertainty.

## Inputs
Expected inputs:
- task json
- summary file
- question file
- optional project memory
- optional browser / search access

## Research Scope
Research may include:
- market / category context
- competitor activity
- brand references
- cultural context
- technical or factual verification
- audience signals
- relevant case studies

## Research Classification
Every finding must be labeled as one of:
- **Verified Fact**
- **Grounded Inference**
- **Creative Inspiration**
- **Open Question**

## Rules
- Do not research everything.
- Research only what reduces ambiguity or improves direction quality.
- Preserve source links and evidence.
- If a claim is not verified, do not present it as fact.
- Distinguish “what exists” from “what might work”.

## Preferred Structure
Organize findings into:

1. Research goal
2. Market / category signals
3. Competitor / reference signals
4. Technical / factual verification
5. Audience / cultural observations
6. Key implications
7. Remaining unknowns
8. Sources

## Output Files
Write:
- `outputs/research/{job_id}_research.md`

## Suggested Markdown Template
Use this structure:

# 리서치 팩

## 리서치 목적
...

## 시장 / 카테고리
- [Verified Fact]
- [Grounded Inference]

## 경쟁사 / 레퍼런스
- [Verified Fact]
- [Creative Inspiration]

## 기술 / 팩트 체크
- [Verified Fact]

## 타깃 / 문화 맥락
- [Grounded Inference]

## 핵심 시사점
1.
2.
3.

## 아직 남아 있는 의문
1.
2.
3.

## 참고 출처
- source:
- reason it matters:

## Quality Standard
This skill is complete only when:
- the research changes decision quality,
- findings are classified clearly,
- the human can tell fact from inspiration instantly.

## Failure Handling
If trustworthy sources are limited:
- say so clearly,
- reduce confidence,
- avoid overclaiming.
