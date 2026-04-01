---
name: solution-directions
description: Turn the OT, gap map, and research pack into three differentiated solution paths.
---

# Skill: solution-directions

## Purpose
Turn the OT, gap map, and research pack into three differentiated solution paths (Strategic, Creative, Execution).

This skill is responsible for generating directions that are useful for real decision-making.

## When to Use
Use this skill after:
- `ot-intake`
- `gap-check`
- `research-pack`

## Inputs
Expected inputs:
- task json
- summary file
- questions file
- research file
- optional project memory references

## Required Directions
Produce at least three directions:

1. **Strategic Direction**: Core logic, business alignment, and high-level strategy.
2. **Creative / Narrative Direction**: Emotional hook, story, and creative framing.
3. **Execution / Production Direction**: Practical steps, feasibility, and production logic.

These may overlap, but each must have a distinct logic.

## Core Rule
**Do not make three versions of the same idea.**
Each direction must differ in:
- problem framing
- message hierarchy
- emotional tone
- structure
- execution implication

## Evaluation Lenses
Review each direction through:
- **Scene**: what is visible or concretely implied
- **Emotion**: what feeling or tone is being created (factual/descriptive)
- **Structure**: why the sequence or framing makes sense
- **Consumer/Public Insight**: why this matters to the everyday user and their daily life

## Required Fields for Each Direction
For each direction include:
- title
- one-line concept
- problem framing
- core message
- emotional tone
- visual / scene implication
- structure
- strengths
- risks
- what must be confirmed next

## Output Files
Write to:
- `outputs/02_deep_analysis/{job_id}_deep_report.md`

## Suggested Markdown Template
Use this structure:

# 해결 방향 3안

## 방향 A — [제목]
### 한 줄 정의
...

### 문제 정의
...

### 핵심 메시지
...

### 감정 톤
...

### 장면 / 비주얼 함의
...

### 구조
...

### 장점
...

### 리스크
...

### 추가 확인 필요
...

## 방향 B — [제목]
...

## 방향 C — [제목]
...

## 비교 메모
- A가 유리한 상황:
- B가 유리한 상황:
- 가장 추천하는 방향:
- 추천 이유:

## Quality Standard
This skill is complete only when:
- the three directions are meaningfully different,
- each direction can be discussed in a meeting,
- one recommended path is clearly identified without hiding trade-offs.

## Failure Handling
If research is weak or OT is too vague:
- still provide three directions,
- reduce certainty,
- explicitly note which parts are provisional.
