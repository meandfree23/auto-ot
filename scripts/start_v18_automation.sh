#!/bin/bash

# V18.2 Master Orchestrator - Auto-OT Resilient Automation
# This script ensures the Telegram Bot and Pipeline Runner are always active.

WORKSPACE="/Users/kk/Desktop/오티 자동화"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.10/bin/python3"
LOG_DIR="${WORKSPACE}/outputs/logs"
MASTER_LOG="${LOG_DIR}/master_daemon.log"

# Ensure log dir exists
mkdir -p "${LOG_DIR}"

echo "[$(date)] Master Daemon: Starting V18.2 Resilient Suite..." >> "${MASTER_LOG}"

# 1. Load Credentials (Handling local env)
if [ -f "${WORKSPACE}/.env" ]; then
    export $(grep -v '^#' "${WORKSPACE}/.env" | xargs)
    echo "[$(date)] Environment variables loaded from .env" >> "${MASTER_LOG}"
fi

# 2. Cleanup existing processes to avoid port/resource conflicts
pkill -f "telegram_bot.py"
pkill -f "run_pipeline.py"
sleep 2

# 3. Boot Pipeline Runner (The brain that processes tasks and commands)
echo "[$(date)] Starting Pipeline Runner (all-in-one mode)..." >> "${MASTER_LOG}"
cd "${WORKSPACE}"
"${PYTHON}" "scripts/run_pipeline.py" all >> "${LOG_DIR}/run_pipeline.log" 2>&1 &

# 4. Boot Telegram Listener (The interface)
echo "[$(date)] Starting Telegram Bot Service..." >> "${MASTER_LOG}"
"${PYTHON}" "scripts/telegram_bot.py" >> "${LOG_DIR}/telegram_bot.log" 2>&1 &

echo "[$(date)] Master Daemon: Suite deployed in background." >> "${MASTER_LOG}"
