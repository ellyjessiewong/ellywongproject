# Trade Journal assistant

This workspace helps process trading screenshots and journal notes.

## Jobs

1. **Rename screenshots** from OCR'd notes to: `Date_Trade X_Direction_Playbook_Green/Red`
2. **Green edge review** — commonalities in confluences/notes on winning trades
3. **Red reflection** — commonalities on losing trades for process review

## Folders

| Path | Purpose |
| --- | --- |
| `inbox/` | Drop raw screenshots here |
| `renamed/` | Renamed screenshots after approval |
| `reviews/` | Green/Red analysis write-ups |
| `config.md` | Optional path to a local screenshot folder on your computer |

## Skills (type `/` in Agent chat)

- `/rename-trade-screenshots`
- `/green-edge-review`
- `/red-trade-reflection`

## Hard rules

- Do not invent prices, fills, playbooks, or results if the screenshot is unreadable
- Propose renames before applying them, unless the user says to auto-rename
- Separate Facts (from images/notes) from Inferences
- Journaling/analysis only — not financial advice; never place trades or open broker accounts
