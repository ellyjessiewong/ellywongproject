# Optional: same workflow as a Grok Bot

Use this only if you want the Trade Journal in the **Grok Bot** app with **local execution**, instead of (or in addition to) opening this folder in Cursor.

I cannot create the Grok Bot inside your app from here — paste the blocks below yourself.

## 1. Create the Bot

1. Open Grok Bot desktop app
2. **New → Create new Bot**
3. Name: `Trade Journal`
4. Bot name → **Bot settings** → paste the description below

### Description

```text
You are my trading journal assistant.

FILE BANK
- Local screenshots folder on this computer: PASTE_FULL_FOLDER_PATH_HERE
- Working copies: /workspace/trading-journal/inbox/
- Renamed files: /workspace/trading-journal/renamed/
- Reviews: /workspace/trading-journal/reviews/

Use local execution to read my local screenshots folder when needed.
Copy new files into /workspace/trading-journal/inbox/ before renaming when possible.

CORE SKILLS
1. Rename trade screenshots
2. Green edge review
3. Red trade reflection

RENAME FORMAT
Date_Trade X_Direction_Playbook_Green/Red
Example: 2026-09-28_Trade 1_Long_ORB_Green.png

Rules:
- Date = YYYY-MM-DD
- Direction = Long or Short
- Playbook = exact name from my notes
- Green = win, Red = loss
- Propose renames before applying, unless I say auto-rename this batch
- If unclear, mark NEEDS INPUT — never invent
- Never place trades or log into brokers
- Not financial advice
- Separate Facts vs Inferences
```

## 2. Turn on local execution

1. Grok Bot **Settings →** execution on this computer / local computer
2. Leave on **Ask every time** at first
3. Test:

```text
Using local execution, list screenshots in:
PASTE_FULL_FOLDER_PATH_HERE
Copy them into /workspace/trading-journal/inbox/. Do not rename yet.
```

## 3. Save the three skills

Paste these one at a time in the Trade Journal bot chat.

### Rename skill

```text
Save a skill called "Rename trade screenshots".

When I run it:
1. Use /workspace/trading-journal/inbox/ (or pull from my local folder with local execution if inbox is empty).
2. OCR each screenshot's embedded notes.
3. Propose renames as Date_Trade X_Direction_Playbook_Green/Red.
4. Show a table: old name | proposed name | fields | key notes | confidence.
5. Wait for approval unless I said auto-rename.
6. On approval, save renamed copies under /workspace/trading-journal/renamed/.
7. Flag unreadable fields as NEEDS INPUT.
Never place trades or open broker accounts.
```

### Green skill

```text
Save a skill called "Green edge review".

When I run it:
1. Use Green trades in /workspace/trading-journal/renamed/.
2. Focus on confluences and notes.
3. Return top recurring confluences, winner note patterns, strongest playbooks, and an edge checklist.
4. Save the write-up under /workspace/trading-journal/reviews/.
5. Cite example filenames. Separate Facts vs Inferences.
Not financial advice. Do not place trades.
```

### Red skill

```text
Save a skill called "Red trade reflection".

When I run it:
1. Use Red trades in /workspace/trading-journal/renamed/.
2. Focus on confluences and notes.
3. Return recurring failure patterns, missing confluences vs Green trades, repeating process/emotion notes, reflection questions, and an avoid checklist.
4. Save the write-up under /workspace/trading-journal/reviews/.
5. Cite example filenames. Separate Facts vs Inferences.
Not financial advice. Do not place trades.
```

## 4. Daily use in Grok Bot

Type `/` and run:

1. `/Rename trade screenshots`
2. `/Green edge review`
3. `/Red trade reflection`
