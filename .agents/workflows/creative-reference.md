---
description: Automated workflow for gathering mood-boards, visual cues, and competitor captures for the Web Report.
---

# /creative-reference

This workflow is used to deepen the "Visual IQ" of the high-fidelity dashboard. It prioritizes mood-boards, competitor captures, and Tone & Manner analysis.

## Flow
1. **Visual Research (Web Search)**: 
   - Search for current industry UI trends for the specific brand sector.
   - Gather 3-5 "Tone & Manner" keywords (e.g., 'Silent Luxury', 'Minimalism', 'Industrial Raw').
2. **Asset Collection**: 
   - Pull at least 4-8 high-quality reference images for **Mood-boards**.
   - Capture at least 3 competitor UI screens for **Browser Mockups**.
3. **Bridge Integration (Creative Mode)**: 
   - Call `scripts/antigravity_bridge.py` with `mode="creative"`.
   - Ensure the "Visual Section" (Sections 02-05) is populated with rich media lists.
4. **HTML Rendering**: 
   - Invoke `scripts/ppt_engine_v4.py` V12.0.
   - Verify the **Bento Grid** correctly highlights the creative assets as "Critical".

## Rules
- **mood_board_density**: At least 4 slides must be dedicated to "Visual Mood-boards" (4 images per grid).
- **capture_integrity**: Browser frames must be used for any third-party UI to avoid confusion with the project's own designs.
- **source_mandatory**: Every visual reference MUST have an attribution label (`source`).
- **high_def**: All image URLs should be high-resolution (Pref: Unsplash, Pexels, or official brand assets).
