---
name: rename-trade-screenshots
description: OCR trading screenshots, extract notes, and rename files to Date_Trade X_Direction_Playbook_Green/Red. Use when organizing trade screenshot banks.
disable-model-invocation: true
icon: image
color: blue
---

# Rename trade screenshots

Read embedded notes in trading screenshots and rename files using the house nomenclature.

## Source of files

Use the first available source:

1. Image files in `inbox/`
2. If `inbox/` is empty, the local folder path in `config.md`
3. Any folder/files the user `@` mentions in chat

## Process

1. List candidate screenshot files.
2. For each image, OCR / read embedded notes. Prioritize confluences, direction, playbook, result (win/loss), date, and trade number.
3. Build a proposed filename:

`Date_Trade X_Direction_Playbook_Green/Red`

Field rules:
- **Date:** `YYYY-MM-DD` from the note/screenshot
- **Trade X:** `Trade 1`, `Trade 2`, ... for that date (ask if unclear)
- **Direction:** `Long` or `Short`
- **Playbook:** exact playbook name from notes (do not invent)
- **Green/Red:** Green = win, Red = loss
- Keep the original extension (`.png`, `.jpg`, etc.)

4. Show a proposal table **before** renaming:

| Old name | Proposed name | Date | Trade # | Direction | Playbook | Green/Red | Key confluences/notes | Confidence | Needs input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

5. Wait for approval, unless the user said `auto-rename this batch`.
6. On approval:
   - Save renamed copies into `renamed/`
   - Prefer keeping originals in `inbox/` unless the user asks to replace/move them
7. Mark unreadable fields as `NEEDS INPUT` instead of guessing.

## Output after renaming

- Summary count: renamed / needs input / skipped
- List of final paths under `renamed/`
- Any open questions for the user
