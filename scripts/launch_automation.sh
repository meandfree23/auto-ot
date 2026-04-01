#!/bin/bash

# V21.0 macOS Master Automation Launcher
# Ensures the OT Automation pipeline starts and stays alive.

ROOT="/Users/kk/Desktop/오티 자동화"
cd "$ROOT"

# Optional: Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the master daemon
exec /Library/Frameworks/Python.framework/Versions/3.10/Resources/Python.app/Contents/MacOS/Python scripts/keep_alive.py >> outputs/logs/launch_agent.log 2>&1
