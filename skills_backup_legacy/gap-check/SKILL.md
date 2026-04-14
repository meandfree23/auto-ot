---
name: gap-check
description: Identify what is missing, contradictory, risky, or still undecided in the OT.
---

# Skill: gap-check

## Purpose
Identify what is missing, contradictory, risky, or still undecided in the OT.

This skill exists to protect decision quality by exposing gaps before solution generation.

## When to Use
Use this skill after `ot-intake` has produced a structured summary.

## Inputs
Expected inputs:
- task json
- `outputs/summaries/{job_id}_summary.md`
- original source text if needed
- optional project memory references

## Main Goals
Detect:
- missing facts
- contradictions
- vague requests
- risky assumptions
- approvals or dependencies
- internal decisions still needed
- client-side questions still needed

## Gap Categories
Check the OT against these categories:

### 1. Strategy
- problem definition
- target audience
- campaign objective
- success criteria

### 2. Creative
- tone and manner
- reference alignment
- message hierarchy
- narrative preference

### 3. Production
- budget
- schedule
- location
- cast / model
- asset availability
- deliverable specs

### 4. Stakeholder / Approval
- decision-maker
- review structure
- revision expectations
- sign-off points

## Thinking Rules
- Separate “missing fact” from “human choice”.
- Separate “unclear” from “impossible”.
- Rank questions by urgency.
- Focus on decision bottlenecks, not trivia.

## Output Format
Produce:

1. Critical questions for client
2. Internal decisions needed
3. Risk list
4. Assumptions currently being made
5. Recommended clarification priority

## Output Files
Write:
- `outputs/questions/{job_id}_questions.md`

## Suggested Markdown Template
Use this structure:

# OT 핵심 질문

## 반드시 확인해야 할 질문
1.
2.
3.

## 내부에서 먼저 정해야 할 것
1.
2.
3.

## 현재 가정하고 있는 내용
1.
2.
3.

## 리스크
- high:
- medium:
- low:

## 우선 확인 순서
1.
2.
3.

## Quality Standard
This skill is complete only when:
- the human can immediately see what blocks progress,
- questions are ranked by importance,
- assumptions are clearly visible.

## Failure Handling
If information is too thin:
- state that the OT is underdefined,
- prioritize the minimum viable clarification set,
- do not over-invent missing data.
