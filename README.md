# Elly's Cursor assistants

This repo holds two separate assistants:

| Assistant | Open this folder | Skills |
| --- | --- | --- |
| **Medical writing** | repo root (`ellywongproject`) | `/copy-deck`, `/fact-check`, `/reference-claims`, `/editorial-pass` |
| **Trade journal** | `trading-journal/` | `/rename-screenshots`, `/green-reviews`, `/red-reviews` |

For trading screenshots, see [`trading-journal/README.md`](trading-journal/README.md).

---

# Work assistant — medical writing

Cursor workspace for pharmaceutical marketing medical writing: copy decks, fact checking, referencing, and editorial passes.

## Quick start

1. Open this folder in Cursor (**File → Open Folder**).
2. Replace the sample rows in:
   - `claims/claim-bank.md`
   - `references/reference-library.md`
   - `style/style-guide.md`
3. Copy `drafts/brief-template.md` for a new piece and fill it in.
4. In Agent chat, type `/` and run one of the skills below. `@` your brief/draft and claim bank.

## Skills

| Skill | Use it for |
| --- | --- |
| `/copy-deck` | Build a structured copy deck from a brief + approved claims |
| `/fact-check` | Verify draft wording against the claim bank |
| `/reference-claims` | Attach footnotes/refs from the claim bank + reference library |
| `/editorial-pass` | Style/clarity edits without changing approved claim meaning |

These skills are **manual** (`/` only) so they do not auto-run on unrelated chats.

## Folder map

```text
claims/          Approved claim data bank
references/      Approved reference library
style/           House style guide
drafts/          Briefs and working copy
decks/           Copy deck outputs
.cursor/skills/  The four reusable workflows
.cursor/rules/   Always-on compliance rules
AGENTS.md        How this work assistant behaves
```

## Suggested daily flow

1. `/copy-deck` + `@drafts/your-brief.md` + `@claims/claim-bank.md`
2. `/fact-check` on the draft
3. `/reference-claims` to attach citations
4. `/editorial-pass` for final polish

## Compliance reminder

Only use approved claims and references from this workspace. The assistant should mark unsupported copy instead of inventing medical language or citations.
