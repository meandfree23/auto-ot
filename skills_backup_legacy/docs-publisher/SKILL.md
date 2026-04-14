---
name: docs-publisher
description: Convert generated markdown outputs into human-reviewable published documents and save their publication record.
---

# Skill: docs-publisher

## Purpose
Convert generated markdown outputs (summary, questions, research, and solutions) into human-reviewable published documents and save their publication record.

## When to Use
Use this skill after:
- summary
- questions
- research
- solutions
have all been generated.

## Inputs
Expected inputs:
- task json
- summary markdown
- questions markdown
- research markdown
- solutions markdown
- access to Google Docs / Drive publishing layer

## Publishing Goals
Publish separate documents for:
1. one-page summary
2. critical questions
3. research pack
4. solution directions

## Naming Convention
Use these structured names:
- `{job_id}_01_OT_한장요약`
- `{job_id}_02_OT_핵심질문`
- `{job_id}_03_OT_리서치팩`
- `{job_id}_04_OT_해결방향3안`

## Rules
- Keep each document separate.
- Preserve headings and readability.
- Add created timestamp.
- Add source file link.
- Add source / evidence section where relevant.
- Do not publish as external communication.
- Do not auto-send to client.

## Output Files
Write:
- `outputs/logs/{job_id}_publish.json`
- update `state/run_history.json`

## Publish Log Format
Track:
- job_id
- source file id
- source file link
- published document names
- published document ids or urls
- published_at
- status

## Suggested Completion Note
Include a short completion note:
- what was published
- any uncertainty
- any missing source text
- whether human review is strongly recommended

## Quality Standard
This skill is complete only when:
- documents are easy to open and read on mobile or desktop,
- naming is consistent,
- source traceability is preserved.

## Failure Handling
If one document fails to publish:
- publish the remaining documents if possible,
- record the failure clearly,
- do not silently skip missing outputs.
