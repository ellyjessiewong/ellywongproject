---
name: rename-screenshots
description: Rename trading screenshots from OCR'd notes to Date_Trade X_Direction_Playbook_Green/Red.
disable-model-invocation: true
icon: image
color: blue
---

# Rename screenshots

## Source
Use `inbox/`, or the path in `config.md` if inbox is empty, or files the user `@`s.

## Do this
1. Read notes in each screenshot (date, trade #, direction, playbook, green/red, confluences).
2. Propose names as: `Date_Trade X_Direction_Playbook_Green/Red`
   - Example: `2026-09-28_Trade 1_Long_ORB_Green.png`
3. Show a simple table: old name → new name → confidence / needs input.
4. Wait for approval (unless user says auto-rename).
5. Save renamed copies into `renamed/`. Keep originals in `inbox/` unless asked otherwise.
6. If something is unreadable, mark `NEEDS INPUT` — do not guess.
