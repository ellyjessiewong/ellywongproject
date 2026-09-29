# Trade Journal assistant

Cursor workspace for renaming trading screenshots and reviewing Green/Red patterns from your notes.

This is **not** a separate GitHub account or Grok Bot by itself. It is a folder inside `ellywongproject` that you open in Cursor. Your medical-writing assistant stays at the repo root; this trading assistant lives here.

## Quick start

1. Merge the PR that adds this folder (if it is not on `main` yet).
2. In Cursor: **File → Open Folder…**
3. Open the **`trading-journal`** folder (not necessarily the whole repo).
4. Put screenshots into `inbox/`  
   **or** paste your local screenshots folder path into `config.md`.
5. In Agent chat, type `/` and run:
   1. `/rename-trade-screenshots`
   2. `/green-edge-review`
   3. `/red-trade-reflection`

## Skills

| Skill | What it does |
| --- | --- |
| `/rename-trade-screenshots` | OCR notes → propose/apply `Date_Trade X_Direction_Playbook_Green/Red` |
| `/green-edge-review` | Commonalities across Green trades (confluences + notes) |
| `/red-trade-reflection` | Commonalities across Red trades for reflection |

## Rename format

`Date_Trade X_Direction_Playbook_Green/Red`  
Example: `2026-09-28_Trade 1_Long_ORB_Green.png`

## Local files (no Google Drive)

Best options:

1. **Drop files into `inbox/`** (simplest)
2. Put your Mac/PC folder path in `config.md` and ask the rename skill to use it
3. Prefer Grok Bot local execution? See `GROK_BOT_SETUP.md` for paste-ready Bot + skill text

## Folder map

```text
inbox/       raw screenshots
renamed/     renamed outputs
reviews/     green/red write-ups
config.md    optional local folder path
.cursor/     rules + skills
```
