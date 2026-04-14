---
name: ot-intake
description: Read a newly uploaded OT, brief, note, or request document and convert it into a clean decision-ready intake structure.
---

# Skill: ot-intake

## Purpose
Read a newly uploaded OT, brief, note, or request document and convert it into a clean decision-ready intake structure.

This skill is responsible for:
- understanding the visible request,
- identifying the implied request,
- extracting core constraints,
- producing a one-page summary for fast human understanding.

## When to Use
Use this skill when:
- a new OT or briefing document has been uploaded,
- a raw PDF or Google Doc needs initial interpretation,
- a human needs a fast overview before detailed research begins.

## Inputs
Expected inputs:
- task json from `incoming_tasks/tasks/`
- source file metadata
- source document text or extracted OCR text
- optional references from `project_memory/`

## Required Extraction
Extract the following whenever available:
- client / brand / organization
- document type
- requested deliverables
- target audience
- schedule / deadlines
- production constraints
- assets already available
- explicit asks
- implied asks
- unclear or ambiguous parts

## Thinking Rules
- Do not just summarize line by line.
- Reconstruct the OT into a usable structure.
- Distinguish between:
  - what is stated,
  - what is implied,
  - what is uncertain.
- If OCR or text extraction looks incomplete, clearly say so.
- Avoid empty stylistic phrasing. Be practical and decision-oriented.

## Output Format
Create a one-page summary with the following structure:

1. Project one-line definition
2. Explicit client asks
3. Implied real problem
4. Deliverables requested
5. Constraints and conditions
6. Missing or unclear areas
7. Immediate judgment points

## Output Files
Write:
- `outputs/summaries/{job_id}_summary.md`
- `outputs/logs/{job_id}_intake.json`

## Suggested Markdown Template
Use this structure:

# OT 한장 요약

## 프로젝트 한 줄 정의
...

## 클라이언트의 명시적 요구
...

## 숨은 요구 / 실제 문제
...

## 요청 산출물
...

## 제약 조건
...

## 불명확하거나 비어 있는 부분
...

## 지금 바로 필요한 판단
...

## Extraction Confidence
- confidence level: high / medium / low
- reason:
- OCR issues, if any:

## Quality Standard
This skill is complete only when:
- a human can understand the OT in under 3 minutes,
- the real problem is clearer than in the original document,
- ambiguity is visible instead of being hidden.

## Failure Handling
If the source text is partial, messy, or broken:
- continue with best effort,
- mark missing sections clearly,
- do not pretend certainty.
