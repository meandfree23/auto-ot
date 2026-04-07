#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ANTIGRAVITY OT AUTOMATION — MASTER CONTROL CENTER (V34.0)
#  통합 지휘 센터: 서비스 관리 · 작업 현황 · 로그 모니터링
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROOT="/Users/kk/Desktop/오티 자동화"
cd "$ROOT" || { echo "❌ 디렉토리 진입 실패: $ROOT"; exit 1; }

# ── 색상 팔레트 ───────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'
DIM='\033[2m'

# ── 헬퍼 함수 ────────────────────────────────────────────────────────
header() {
    clear
    echo -e "${BOLD}${CYAN}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   🚀  ANTIGRAVITY OT AUTOMATION  ·  MASTER CONTROL (V34.0)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${RESET}"
}

is_running() {
    /usr/bin/pgrep -f "$1" > /dev/null 2>&1
}

service_badge() {
    if is_running "$1"; then
        echo -e "${GREEN}● RUNNING${RESET}"
    else
        echo -e "${RED}○ STOPPED${RESET}"
    fi
}

section() { echo -e "\n${BOLD}${BLUE}▸ $1${RESET}"; }

# ── 상태 대시보드 ────────────────────────────────────────────────────
show_status() {
    header
    section "서비스 상태"
    printf "  %-28s %s\n" "Keep-Alive Watchdog"  "$(service_badge 'keep_alive.py')"
    printf "  %-28s %s\n" "Drive Poller"          "$(service_badge 'poll_drive_to_tasks.py')"
    printf "  %-28s %s\n" "Pipeline Runner"       "$(service_badge 'run_pipeline.py')"
    printf "  %-28s %s\n" "Telegram Bot"          "$(service_badge 'telegram_bot.py')"

    section "환경 변수 점검"
    for VAR in GEMINI_API_KEY TELEGRAM_BOT_TOKEN TELEGRAM_CHAT_ID OUTPUT_FOLDER_ID; do
        VAL=$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); v=os.environ.get('$VAR',''); print('SET' if v else 'MISSING')" 2>/dev/null)
        if [ "$VAL" = "SET" ]; then
            printf "  %-28s ${GREEN}✓ SET${RESET}\n" "$VAR"
        else
            printf "  %-28s ${RED}✗ MISSING${RESET}\n" "$VAR"
        fi
    done

    section "최근 작업 이력 (최대 5건)"
    if [ -f "state/run_history.json" ]; then
        python3 - <<'PYEOF'
import json
from pathlib import Path
history_path = Path("state/run_history.json")
try:
    data = json.loads(history_path.read_text(encoding="utf-8"))
    recent = data[-5:] if isinstance(data, list) else []
    if not recent:
        print("  (기록 없음)")
    for item in reversed(recent):
        jid = item.get("job_id", "?")[:28]
        ts  = item.get("published_at", item.get("created_at", "?"))[:19]
        st  = item.get("status", "?")
        icon = "✅" if "success" in st else "⚠️" if "partial" in st else "❌"
        print(f"  {icon}  {ts}  [{jid}]  {st}")
except Exception as e:
    print(f"  (파싱 실패: {e})")
PYEOF
    else
        echo -e "  ${DIM}(state/run_history.json 없음)${RESET}"
    fi

    section "작업 큐 현황"
    PENDING=$(ls incoming_tasks/tasks/*.json 2>/dev/null | wc -l | tr -d ' ')
    PROCESSING=$(ls state/processing/*.json 2>/dev/null | wc -l | tr -d ' ')
    DONE=$(ls state/done/*.json 2>/dev/null | wc -l | tr -d ' ')
    FAILED=$(ls state/failed/*.json 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  대기: ${YELLOW}${PENDING}${RESET}  처리중: ${CYAN}${PROCESSING}${RESET}  완료: ${GREEN}${DONE}${RESET}  실패: ${RED}${FAILED}${RESET}"
}

# ── 서비스 시작 ──────────────────────────────────────────────────────
start_all() {
    section "시스템 시작"
    mkdir -p outputs/logs state

    if is_running "keep_alive.py"; then
        echo -e "  ${YELLOW}Keep-Alive 이미 실행 중입니다.${RESET}"
        echo -e "  ${DIM}(Watchdog이 모든 서비스를 자동 관리합니다)${RESET}"
    else
        echo -n "  Keep-Alive Watchdog 시작 중..."
        nohup python3 scripts/keep_alive.py > outputs/logs/keep_alive.log 2>&1 &
        sleep 2
        if is_running "keep_alive.py"; then
            echo -e " ${GREEN}완료${RESET}"
            echo -e "  ${DIM}(Drive Poller · Pipeline · Telegram Bot 자동 시작 대기 중...)${RESET}"
        else
            echo -e " ${RED}실패 — outputs/logs/keep_alive.log 확인 필요${RESET}"
        fi
    fi
}

# ── 서비스 중단 ──────────────────────────────────────────────────────
stop_all() {
    section "시스템 중단"
    for SCRIPT in keep_alive.py poll_drive_to_tasks.py run_pipeline.py telegram_bot.py; do
        echo -n "  $SCRIPT 종료 중..."
        /usr/bin/pkill -f "$SCRIPT" 2>/dev/null && echo -e " ${GREEN}완료${RESET}" || echo -e " ${DIM}실행 중 아님${RESET}"
    done
    rm -f state/keep_alive.lock
    echo -e "\n  ${GREEN}모든 서비스 중단 완료.${RESET}"
}

# ── 로그 뷰어 ────────────────────────────────────────────────────────
view_logs() {
    echo ""
    echo "  [1] Keep-Alive 워치독 로그"
    echo "  [2] Drive Poller 로그"
    echo "  [3] Pipeline Runner 로그"
    echo "  [4] Telegram Bot 로그"
    echo "  [5] 최근 publish 결과 (JSON)"
    echo ""
    read -rp "  선택 (1-5): " LCHOICE
    case $LCHOICE in
        1) tail -f outputs/logs/keep_alive.log ;;
        2) tail -f outputs/logs/poll_drive.log ;;
        3) tail -f outputs/logs/run_pipeline.log ;;
        4) tail -f outputs/logs/telegram_bot.log ;;
        5)
            LATEST=$(ls -t outputs/logs/*_publish.json 2>/dev/null | head -1)
            if [ -n "$LATEST" ]; then
                python3 -c "import json; d=json.load(open('$LATEST')); print(json.dumps(d,indent=2,ensure_ascii=False))"
            else
                echo "  (publish 로그 없음)"
            fi
            echo ""; read -rp "  계속하려면 Enter..." ;;
        *) echo "  취소." ;;
    esac
}

# ── 수동 파이프라인 트리거 ──────────────────────────────────────────
manual_trigger() {
    section "수동 파이프라인 실행"
    echo -e "  ${CYAN}Drive 새 파일 즉시 폴링...${RESET}"
    python3 scripts/poll_drive_to_tasks.py --once 2>&1 | tail -5
    echo ""

    PENDING=$(ls incoming_tasks/tasks/*.json 2>/dev/null | wc -l | tr -d ' ')
    if [ "$PENDING" -gt 0 ]; then
        echo -e "  ${YELLOW}대기 작업 ${PENDING}건 발견 — 파이프라인 즉시 실행 중...${RESET}"
        python3 scripts/run_pipeline.py 2>&1 | tail -20
    else
        echo -e "  ${DIM}대기 중인 작업 없음.${RESET}"
    fi
}

# ── 재발행 (Republish) ──────────────────────────────────────────────
republish() {
    section "Job 재발행"
    echo -n "  Job ID 입력: "
    read -r JID
    if [ -z "$JID" ]; then echo "  취소."; return; fi
    echo -e "  ${CYAN}${JID}${RESET} 재발행 중..."
    python3 scripts/publish_to_docs.py "$JID" 2>&1 | tail -15
    echo ""
    echo -n "  Telegram 알림 전송 중..."
    python3 scripts/send_telegram.py "$JID" finished && echo -e " ${GREEN}완료${RESET}" || echo -e " ${RED}실패${RESET}"
}

# ── 메인 메뉴 ────────────────────────────────────────────────────────
main_menu() {
    show_status
    echo ""
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo "  [1] 시스템 시작 (Start All)"
    echo "  [2] 시스템 중단 (Stop All)"
    echo "  [3] 재시작 (Stop → Start)"
    echo "  [4] 수동 파이프라인 실행"
    echo "  [5] 실시간 로그 보기"
    echo "  [6] Job 재발행 (Republish)"
    echo "  [7] 상태 새로고침"
    echo "  [q] 종료 (엔진은 백그라운드 유지)"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    read -rp "  선택: " CHOICE

    case $CHOICE in
        1) start_all;  echo ""; read -rp "  계속하려면 Enter..." ;;
        2) stop_all;   echo ""; read -rp "  계속하려면 Enter..." ;;
        3) stop_all; sleep 2; start_all; echo ""; read -rp "  계속하려면 Enter..." ;;
        4) manual_trigger; echo ""; read -rp "  계속하려면 Enter..." ;;
        5) view_logs ;;
        6) republish;  echo ""; read -rp "  계속하려면 Enter..." ;;
        7) ;; # 루프 재진입 → show_status 자동 재실행
        q|Q) echo -e "\n  ${DIM}백그라운드 엔진은 계속 실행됩니다. 창을 닫으셔도 됩니다.${RESET}\n"; exit 0 ;;
        *) echo -e "  ${RED}알 수 없는 선택.${RESET}"; sleep 1 ;;
    esac
}

# ── 진입점 ───────────────────────────────────────────────────────────
while true; do
    main_menu
done
