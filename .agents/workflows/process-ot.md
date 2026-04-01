---
description: Process a newly arrived OT/brief and generate a decision-ready package.
---

# /process-ot

When given a task JSON from `incoming_tasks/`, do the following:

1. **Read Task JSON**: Read the task JSON completely from `incoming_tasks/tasks/`.
2. **Identify Metadata**: Identify the source file path, file URL, project type, language, and required outputs.
3. **Inspect Document**: Open and inspect the source document (e.g., from `incoming_tasks/raw_docs/`).
4. **Produce Deliverables**:
   - one-page summary (using `templates/summary_template.md`)
   - critical questions (using `templates/questions_template.md`)
   - research pack (using `templates/research_template.md`)
   - three solution directions (using `templates/solution_template.md`)
5. **Follow Rules**: Adhere strictly to the workspace rule `.agents/rules/ot-auto-orchestrator.md`.
6. **Separate Perspectives**: Explicitly separate verified facts, assumptions, interpretation, and recommendation.
7. **Save Outputs**:
   - `outputs/summaries/`
   - `outputs/questions/`
   - `outputs/research/`
   - `outputs/solutions/`
8. **Log Completion**: Add a short completion log into `outputs/logs/`.
9. **No External Send**: Do not send anything externally (messages, emails, etc.).
10. **Handle Partial Data**: If the source text extraction looks partial or broken, state the uncertainty clearly and continue with best-effort structural analysis.
