#!/bin/bash
# 하네스 훅: PostToolUse (Edit|Write)
# 목적: Python 파일 수정 후 즉시 문법 검사 → Claude가 재확인 요청하는 토큰 절약

FILE_PATH=$(echo "$1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# stdin에서 읽기 (파이프로 받는 경우)
if [ -z "$FILE_PATH" ]; then
    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
fi

# Python 파일만 처리
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# 문법 검사
RESULT=$(python3 -m py_compile "$FILE_PATH" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    # 오류 발생 시 Claude에게 알림 (additionalContext로 주입)
    python3 -c "
import json, sys
msg = sys.stdin.read()
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PostToolUse',
        'additionalContext': f'[자동 문법 검사 실패] {msg.strip()}\n위 파일에 Python 문법 오류가 있습니다. 수정이 필요합니다.'
    }
}))
" <<< "$RESULT"
    exit 0
fi

# 성공 시 조용히 종료 (토큰 낭비 없음)
exit 0
