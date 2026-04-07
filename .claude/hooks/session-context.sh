#!/bin/bash
# 하네스 훅: SessionStart
# 목적: 세션 시작 시 프로젝트 상태를 Claude 컨텍스트에 자동 주입
# 효과: Claude가 run_history.json, incoming_tasks/ 등을 직접 읽는 토큰 절약

ROOT="/Users/kk/Desktop/오티 자동화"
cd "$ROOT" || exit 0

# 상태 수집
PENDING=$(ls incoming_tasks/tasks/*.json 2>/dev/null | wc -l | tr -d ' ')
PROCESSING=$(ls state/processing/*.json 2>/dev/null | wc -l | tr -d ' ')
DONE=$(ls state/done/*.json 2>/dev/null | wc -l | tr -d ' ')
FAILED=$(ls state/failed/*.json 2>/dev/null | wc -l | tr -d ' ')

# 최근 3건 이력
RECENT_HISTORY=$(python3 - <<'PYEOF' 2>/dev/null
import json
from pathlib import Path
p = Path("state/run_history.json")
if not p.exists():
    print("(이력 없음)")
else:
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        recent = data[-3:] if isinstance(data, list) else []
        for item in reversed(recent):
            jid = item.get("job_id", "?")[:20]
            ts  = item.get("published_at", "?")[:16]
            st  = item.get("status", "?")
            print(f"  {ts} [{jid}] {st}")
    except:
        print("(파싱 실패)")
PYEOF
)

# 실행 중인 서비스 확인
SVC_STATUS=""
for SCRIPT in keep_alive.py poll_drive_to_tasks.py run_pipeline.py telegram_bot.py; do
    if /usr/bin/pgrep -f "$SCRIPT" > /dev/null 2>&1; then
        SVC_STATUS="${SVC_STATUS}  ● ${SCRIPT}\n"
    else
        SVC_STATUS="${SVC_STATUS}  ○ ${SCRIPT} (중단됨)\n"
    fi
done

# Claude 컨텍스트에 주입할 요약 생성
CONTEXT="[오티 자동화 프로젝트 현재 상태]
작업 큐: 대기 ${PENDING}건 / 처리중 ${PROCESSING}건 / 완료 ${DONE}건 / 실패 ${FAILED}건
최근 이력:
${RECENT_HISTORY}
서비스 상태:
$(echo -e "$SVC_STATUS")
핵심 스크립트: scripts/run_pipeline.py (파이프라인), scripts/brain_engine.py (AI분석), scripts/antigravity_bridge.py (브릿지), scripts/publish_to_docs.py (발행)"

# JSON 출력 (additionalContext로 모델에 주입)
python3 -c "
import json, sys
ctx = sys.stdin.read()
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': ctx
    }
}))
" <<< "$CONTEXT"
