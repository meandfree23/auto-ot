# 🚀 OT Automation Pipeline (V10.0 HTML-First)

High-fidelity strategic intelligence engine for automated presentation and reporting.

## 🌟 Core Features
- **NLM High-Density Analysis**: Processes document briefs into 20-page interactive strategic reports.
- **HTML-First Delivery**: Premium, animated web-based reporting via GitHub Pages (Superceding static PPTX).
- **GitHub Pages Integration**: Automated deployment and live-link sharing.
- **Telegram Command Control**: Real-time interaction for deep analysis triggers.

## 🏗️ System Architecture (V10.0)

### 1. Reception & Basic Analysis
- `scripts/telegram_bot.py`: Main entry point for file reception.
- `scripts/run_pipeline.py`: Orchestrates the initial 3P 심층리포트 (Word) generation.
- `scripts/generate_word.py`: Renders professional Word documents from markdown analysis.

### 2. High-Density Advancement ("고도화")
- `scripts/advanced_analysis.py`: Advanced orchestrator triggered by "고도화 해줘".
- `scripts/ppt_engine_v4.py`: **V10.0 Intelligence Engine**. Generates high-density, interactive HTML reports.
- `scripts/publish_to_docs.py`: Synchronizes results to Google Drive and pushes to GitHub Pages for instant web availability.

### 3. Notification & UI
- `scripts/send_telegram.py`: Handles rich HTML notifications and direct web links.

## 📦 Directory Structure
- `/docs/reports/`: Publicly accessible HTML reports (GitHub Pages root).
- `/outputs/`: Raw markdown, summaries, and final binary reports.
- `/state/`: Process tracking and job history.

## 🛠️ Requirements
- Google Drive API (Credentials/Token)
- Telegram Bot API (Token/Chat ID)
- GitHub Repository with Pages enabled (Serving from `/docs` folder on `main` branch).

---
© 2026 OT Automation Team. Optimized for Professional Strategic Consulting.
