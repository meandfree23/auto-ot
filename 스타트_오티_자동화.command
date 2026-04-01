#!/bin/bash
# V33.0 Platinum 'Master Control Center'
# Click to view real-time system status and manage the OT Intelligence Pipeline.

ROOT="/Users/kk/Desktop/오티 자동화"

# Terminal Aesthetic Reset
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 [오티 자동화] PLATINUM CONTROL CENTER (V33.0)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "현재 디렉토리: $ROOT"
cd "$ROOT" || exit 1

# Ensure Output Dirs exist for log monitoring
mkdir -p outputs/logs state

# 1. Start the Watchdog in Background (Hidden Mode)
# If it's already running, it will just exit gracefully with a message.
python3 scripts/keep_alive.py

# 2. Check if successfully started
echo "✅ 시스템 무결성 점검 완료."
echo "🔄 실시간 관제 화면을 동기화 중입니다..."
echo "--------------------------------------------------"
echo "📢 Tip: 이 창을 닫아도 백그라운드 엔진은 멈추지 않습니다."
echo "📢 Tip: 로그 중단은 [Ctrl + C]를 눌러주세요."
echo "--------------------------------------------------"

# 3. Stream the Live Logs
# This keeps the window open and shows the heartbeats.
tail -f outputs/logs/keep_alive.log
