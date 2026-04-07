#!/bin/bash
# 하네스 훅: PreCompact
# 목적: 컨텍스트 압축 전 작업 상태 스냅샷 저장
# 효과: 압축 후 Claude가 상태 재파악하는 토큰 낭비 방지

ROOT="/Users/kk/Desktop/오티 자동화"
SNAPSHOT_FILE="$ROOT/state/compact_snapshot.txt"
cd "$ROOT" || exit 0

PENDING=$(ls incoming_tasks/tasks/*.json 2>/dev/null | wc -l | tr -d ' ')
PROCESSING=$(ls state/processing/*.json 2>/dev/null | wc -l | tr -d ' ')
DONE=$(ls state/done/*.json 2>/dev/null | wc -l | tr -d ' ')
FAILED=$(ls state/failed/*.json 2>/dev/null | wc -l | tr -d ' ')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 현재 진행 중인 job_id 수집
PROCESSING_JOBS=$(ls state/processing/*.json 2>/dev/null | xargs -I{} python3 -c "
import json, sys
try:
    d = json.load(open('{}'))
    print(d.get('job_id','?'))
except: pass
" 2>/dev/null | tr '\n' ', ')

cat > "$SNAPSHOT_FILE" <<EOF
[컴팩션 직전 스냅샷] $TIMESTAMP
작업 큐: 대기 ${PENDING} / 처리중 ${PROCESSING} / 완료 ${DONE} / 실패 ${FAILED}
처리중 Job: ${PROCESSING_JOBS:-없음}
EOF

# PreCompact는 additionalContext 미지원 → 파일 저장으로 다음 세션에 활용
exit 0
