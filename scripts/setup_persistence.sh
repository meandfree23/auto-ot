#!/bin/bash

# V20.0 Persistence Setup Script for macOS
# Installs and starts the LaunchAgent to ensure 24/7 reliability.

PROJECT_ROOT="/Users/kk/Desktop/오티 자동화"
PLIST_NAME="com.antigravity.ot_automation.plist"
PLIST_SOURCE="$PROJECT_ROOT/scripts/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "-----------------------------------------------"
echo "🚀 Antigravity OT Automation: Persistence Setup"
echo "-----------------------------------------------"

# 1. Ensure logs directory exists
mkdir -p "$PROJECT_ROOT/outputs/logs"

# 2. Stop existing service if any
echo "[-] Stopping existing service (if any)..."
launchctl unload "$PLIST_DEST" 2>/dev/null

# 3. Copy Plist to LaunchAgents
echo "[+] Installing LaunchAgent to $PLIST_DEST..."
cp "$PLIST_SOURCE" "$PLIST_DEST"

# 4. Fix permissions
chmod 644 "$PLIST_DEST"

# 5. Load and start the service
echo "[+] Starting service via launchctl..."
launchctl load "$PLIST_DEST"

echo "-----------------------------------------------"
echo "✅ Persistence Setup Complete!"
echo "Status: The watchdog is now running in the background."
echo "Check logs: tail -f '$PROJECT_ROOT/outputs/logs/keep_alive.log'"
echo "-----------------------------------------------"
